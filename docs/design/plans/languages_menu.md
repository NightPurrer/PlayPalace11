# Standardizing the language menu.
server/core/server.py: line 1684

Move this menu to server/ui/common_flows.py

Some of these features are already in the language menu, but are not configurable.

Notes:
The existing language menu manually calls self._show_options_menu. However since this menu is being modified to be run from anywhere, it should call the user's last menu instead.
If the user's current locale is not in the list of languages, put focus at the first item. Otherwise, put focus on their locale.
The localization warmup guard should always be checked before showing the menu. If warmup is active, notify the user and return False.

Menu ID: always uses the static ID "language_menu".

Return value: bool
Returns False if the menu could not be shown (e.g. localization warmup active). Returns True if the menu was displayed successfully.

# Parameters:

## Positional

user:
The user requesting this menu

highlight_active_locale: bool = True
Indicates the user's current locale with a "*" character in front of the respective menu item.

include_native_names: bool = False
Displays the native name for each language after the user's localized name.
If the highlight_active_locale flag is enabled, this setting is ignored for the menu item of the user's locale.
Appends the text " ({name})".
Default is False because most callers show a filtered subset of languages the user already knows (e.g. their fluent languages or assigned transcriber languages). Native names are mainly useful when the user is browsing unfamiliar languages, like when switching their locale.

## Keyword only

lang_codes: list[str] | None = None
If provided, only show these language codes. If None, show all languages.
The caller does any filtering logic before calling the menu.

status_labels: dict[str, str] | None = None
A dictionary mapping lang code to a suffix string.
The caller controls the exact format of the suffix (e.g. "(4 users)", "on", "2026-01-15").
Appends the text " {suffix}" -- the caller includes any delimiters like parentheses or semicolons.

on_select: Callable[[NetworkUser, str], Awaitable[None]]
Called when the user selects a language. Receives the user and the selected lang code.
The callback is stored in user state so the single language_menu handler in _dispatch_menu_selection can retrieve and call it.

on_back: Callable[[NetworkUser], Awaitable[None]]
Called when the user presses back/escape or selects the back item.
If not provided, defaults to restoring the user's previous menu.

# Examples:

## Switching locale (options menu)
-- all languages, native names shown
show_language_menu(
    user, include_native_names=True,
    on_select=self._apply_locale_change,
)

## View transcribers by language
-- all languages with user counts
counts = {code: f"({n} users)" for code, n in transcriber_counts.items()}
show_language_menu(
    user, highlight_active_locale=False,
    status_labels=counts,
    on_select=self._show_transcribers_for_language,
)

## Add translation
-- only untranslated languages the transcriber is assigned to
available = [c for c in assigned_langs if c not in existing_translations]
show_language_menu(
    user,
    lang_codes=available,
    on_select=self._begin_add_translation,
)

## Manage visibility
-- document languages with on/off toggles
labels = {code: "on" if meta["public"] else "off" for code, meta in doc_locales.items()}
show_language_menu(
    user, highlight_active_locale=False,
    lang_codes=list(doc_locales),
    status_labels=labels,
    on_select=self._toggle_locale_visibility,
)
