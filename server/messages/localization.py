"""Localization system using Mozilla Fluent."""

import sys
from pathlib import Path

from fluent_compiler.bundle import FluentBundle
from babel.lists import format_list


class Localization:
    """
    Localization system using Mozilla Fluent via fluent-compiler.

    Loads .ftl files from the locales directory and provides message
    rendering with variable substitution.
    """

    _bundles: dict[str, FluentBundle] = {}
    _locales_dir: Path | None = None

    @classmethod
    def init(cls, locales_dir: Path | str) -> None:
        """Initialize the localization system with a locales directory."""
        cls._locales_dir = Path(locales_dir)
        cls._bundles = {}

    @classmethod
    def preload_bundles(cls) -> None:
        """Pre-load all locale bundles at startup."""
        if cls._locales_dir is None:
            print("ERROR: Localization directory is not configured.", file=sys.stderr)
            raise SystemExit(1)

        if not cls._locales_dir.exists() or not cls._locales_dir.is_dir():
            print(
                f"ERROR: Localization directory '{cls._locales_dir}' is missing or not a directory.",
                file=sys.stderr,
            )
            raise SystemExit(1)

        found_locale = False
        for locale_dir in cls._locales_dir.iterdir():
            if not locale_dir.is_dir():
                continue
            found_locale = True
            try:
                cls._get_bundle(locale_dir.name)
            except RuntimeError as exc:
                print(
                    f"ERROR: Failed to load localization bundle for '{locale_dir.name}': {exc}",
                    file=sys.stderr,
                )
                raise SystemExit(1) from exc

        if not found_locale:
            print(
                f"ERROR: Localization directory '{cls._locales_dir}' does not contain any locale bundles.",
                file=sys.stderr,
            )
            raise SystemExit(1)

    @classmethod
    def _get_bundle(cls, locale: str) -> FluentBundle:
        """Get or create a bundle for a locale."""
        if locale in cls._bundles:
            return cls._bundles[locale]

        if cls._locales_dir is None:
            print("ERROR: Localization directory is not configured.", file=sys.stderr)
            raise SystemExit(1)

        locale_dir = cls._locales_dir / locale
        actual_locale = locale
        if not locale_dir.exists():
            # Fall back to English
            locale_dir = cls._locales_dir / "en"
            actual_locale = "en"
            if not locale_dir.exists():
                print(
                    f"ERROR: No localization files found for '{locale}' or fallback 'en'.",
                    file=sys.stderr,
                )
                raise SystemExit(1)

        # Load all .ftl files in the locale directory
        ftl_content = []
        for ftl_file in locale_dir.glob("*.ftl"):
            ftl_content.append(ftl_file.read_text(encoding="utf-8"))

        if not ftl_content:
            print(
                f"ERROR: No .ftl localization files found in {locale_dir}.",
                file=sys.stderr,
            )
            raise SystemExit(1)

        # Compile messages - join all content (use actual locale for bundle)
        bundle = FluentBundle.from_string(actual_locale, "\n".join(ftl_content))
        cls._bundles[locale] = bundle
        return bundle

    # Unicode bidi isolation characters that Fluent adds around variables
    _BIDI_CHARS = "\u2068\u2069"  # FIRST STRONG ISOLATE, POP DIRECTIONAL ISOLATE

    @classmethod
    def get(cls, locale: str, message_id: str, **kwargs) -> str:
        """
        Get a localized message.

        Args:
            locale: The locale code (e.g., 'en', 'es').
            message_id: The message ID from the .ftl file.
            **kwargs: Variables to substitute into the message.

        Returns:
            The formatted message string.
        """
        try:
            bundle = cls._get_bundle(locale)
            result, errors = bundle.format(message_id, kwargs)
            # Strip Unicode bidi isolation characters that Fluent adds
            for char in cls._BIDI_CHARS:
                result = result.replace(char, "")
            return result
        except Exception:
            # Return the message ID as fallback
            return message_id

    @classmethod
    def format_list_and(cls, locale: str, items: list[str]) -> str:
        """
        Format a list with 'and' conjunction using Babel.

        Args:
            locale: The locale code.
            items: List of items to format.

        Returns:
            Formatted list string (e.g., "A, B, and C").
        """
        return format_list(items, style="standard", locale=locale)

    @classmethod
    def format_list_or(cls, locale: str, items: list[str]) -> str:
        """
        Format a list with 'or' conjunction using Babel.

        Args:
            locale: The locale code.
            items: List of items to format.

        Returns:
            Formatted list string (e.g., "A, B, or C").
        """
        return format_list(items, style="or", locale=locale)

    @classmethod
    def get_available_languages(
        cls, display_language: str = "", *, fallback: str = "en"
    ) -> dict[str, str]:
        """
        Get a dictionary of available languages.

        Args:
            display_language: The locale to use for displaying language names.
                              If empty, each language name is shown in its own
                              language (e.g., "English" for en, "中文" for zh).
            fallback: The locale to use if a language name is not found
                             in the display language. Defaults to "en".

        Returns:
            Dictionary mapping language codes to language names.
        """
        if cls._locales_dir is None:
            raise RuntimeError(
                "Localization not initialized. Call Localization.init() first."
            )

        result = {}

        # Get list of valid locale directories
        locales = [
            locale_dir.name
            for locale_dir in cls._locales_dir.iterdir()
            if locale_dir.is_dir()
        ]

        for locale_code in sorted(locales):
            message_id = f"language-{locale_code}"
            if display_language:
                # Use the display language's bundle for all names
                name = cls.get(display_language, message_id)
            else:
                # Use each locale's own bundle for its name
                name = cls.get(locale_code, message_id)

            # If translation not found, try fallback locale
            if name == message_id  and fallback != display_language:
                name = cls.get(fallback, message_id)

            # If fallback is not "en" and still not found, try "en"
            if name == message_id and fallback != "en":
                name = cls.get("en", message_id)

            result[locale_code] = name

        return result


def get_message(locale: str, message_id: str, **kwargs) -> str:
    """Convenience function to get a localized message."""
    return Localization.get(locale, message_id, **kwargs)
