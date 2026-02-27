"""Reusable menu flows shared across server features.

Usage examples::

    # Switching locale (options menu) — all languages, native names shown
    show_language_menu(
        user, include_native_names=True,
        on_select=self._apply_locale_change,
        on_back=lambda u: self._show_options_menu(u),
    )

    # Filtered subset with status labels
    counts = {code: f"({n} users)" for code, n in transcriber_counts.items()}
    show_language_menu(
        user, highlight_active_locale=False,
        status_labels=counts,
        on_select=self._show_transcribers_for_language,
    )

    # Only specific language codes
    available = [c for c in assigned if c not in existing]
    show_language_menu(
        user, lang_codes=available,
        on_select=self._begin_add_translation,
    )
"""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from ...messages.localization import Localization
from ..users.base import MenuItem, EscapeBehavior

if TYPE_CHECKING:
    from ..users.network_user import NetworkUser

# Per-user callback storage keyed by username.
_language_menu_callbacks: dict[
    str,
    tuple[
        Callable[[NetworkUser, str], Awaitable[None]] | None,
        Callable[[NetworkUser], Awaitable[None]] | None,
    ],
] = {}


def show_language_menu(
    user: NetworkUser,
    highlight_active_locale: bool = True,
    include_native_names: bool = False,
    *,
    lang_codes: list[str] | None = None,
    status_labels: dict[str, str] | None = None,
    on_select: Callable[[NetworkUser, str], Awaitable[None]] | None = None,
    on_back: Callable[[NetworkUser], Awaitable[None]] | None = None,
) -> bool:
    """Show a language selection menu.

    Returns ``True`` if the menu was displayed, ``False`` if it could not be
    shown (e.g. localization warmup still running).
    """
    if Localization.is_warmup_active():
        user.speak_l("localization-in-progress-try-again", buffer="misc")
        return False

    # Native names (each language in its own script)
    native_names = Localization.get_available_languages(fallback=user.locale)
    # Localized names (all names in the user's locale)
    localized_names = Localization.get_available_languages(
        user.locale, fallback=user.locale
    )

    # Filter to requested codes, preserving the full-dict order.
    if lang_codes is not None:
        codes_set = set(lang_codes)
        native_names = {c: n for c, n in native_names.items() if c in codes_set}

    items: list[MenuItem] = []
    selected_position = 1
    for index, (lang_code, native) in enumerate(native_names.items(), start=1):
        is_active = highlight_active_locale and lang_code == user.locale
        prefix = "* " if is_active else ""
        localized = localized_names.get(lang_code, native)
        display = f"{prefix}{localized}"
        # Append native name when it differs and this isn't the highlighted item
        if include_native_names and native != localized and not is_active:
            display = f"{display} ({native})"
        # Append caller-supplied status label
        if status_labels and lang_code in status_labels:
            display = f"{display} {status_labels[lang_code]}"
        items.append(MenuItem(text=display, id=f"lang_{lang_code}"))
        if lang_code == user.locale:
            selected_position = index

    items.append(
        MenuItem(text=Localization.get(user.locale, "back"), id="back")
    )

    _language_menu_callbacks[user.username] = (on_select, on_back)

    user.show_menu(
        "language_menu",
        items,
        multiletter=True,
        escape_behavior=EscapeBehavior.SELECT_LAST,
        position=selected_position,
    )
    return True


async def handle_language_menu_selection(
    user: NetworkUser, selection_id: str
) -> None:
    """Dispatch a language-menu selection to the stored callbacks."""
    on_select, on_back = _language_menu_callbacks.pop(user.username, (None, None))
    if selection_id.startswith("lang_"):
        lang_code = selection_id[5:]
        if on_select is not None:
            result = on_select(user, lang_code)
            if inspect.isawaitable(result):
                await result
    else:
        if on_back is not None:
            result = on_back(user)
            if inspect.isawaitable(result):
                await result
