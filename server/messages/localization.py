"""Localization system using Mozilla Fluent."""

import builtins
import hashlib
import os
import pickle
import sys
from pathlib import Path

from babel import Locale, plural
from babel.core import UnknownLocaleError
from babel.lists import format_list
from fluent_compiler import runtime
from fluent_compiler.bundle import FluentBundle
from fluent_compiler.compiler import (
    LOCALE_NAME,
    PLURAL_FORM_FOR_NUMBER_NAME,
    compile_messages,
)
from fluent_compiler.resource import FtlResource


class Localization:
    """
    Localization system using Mozilla Fluent via fluent-compiler.

    Loads .ftl files from the locales directory and provides message
    rendering with variable substitution.
    """

    _bundles: dict[str, FluentBundle] = {}
    _locales_dir: Path | None = None
    _cache_dir: Path | None = None
    _cache_enabled: bool = True
    _CACHE_VERSION = "1"
    _CACHE_DISABLE_ENV = "PLAYPALACE_DISABLE_LOCALE_CACHE"
    _CACHE_DIR_ENV = "PLAYPALACE_LOCALE_CACHE_DIR"

    @classmethod
    def init(cls, locales_dir: Path | str) -> None:
        """Initialize the localization system with a locales directory."""
        cls._locales_dir = Path(locales_dir)
        cls._bundles = {}
        disable_cache = os.environ.get(cls._CACHE_DISABLE_ENV, "").strip().lower()
        cls._cache_enabled = disable_cache not in {"1", "true", "yes", "on"}
        cls._cache_dir = None

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

        payloads, fingerprint = cls._load_locale_payloads(locale_dir, actual_locale)
        bundle = cls._load_bundle_from_cache(actual_locale, fingerprint)
        if bundle is None:
            bundle = cls._compile_bundle(actual_locale, payloads, fingerprint)
        cls._bundles[locale] = bundle
        return bundle

    @classmethod
    def _load_locale_payloads(cls, locale_dir: Path, actual_locale: str) -> tuple[list[str], str]:
        """Read locale files and compute a content fingerprint."""
        ftl_files = sorted(locale_dir.glob("*.ftl"))
        if not ftl_files:
            print(
                f"ERROR: No .ftl localization files found in {locale_dir}.",
                file=sys.stderr,
            )
            raise SystemExit(1)

        digest = hashlib.sha256()
        digest.update(cls._CACHE_VERSION.encode("utf-8"))
        digest.update(actual_locale.encode("utf-8"))

        payloads: list[str] = []
        for ftl_file in ftl_files:
            text = ftl_file.read_text(encoding="utf-8")
            payloads.append(text)
            encoded = text.encode("utf-8")
            digest.update(ftl_file.name.encode("utf-8"))
            digest.update(len(encoded).to_bytes(8, "big", signed=False))
            digest.update(hashlib.sha256(encoded).digest())

        return payloads, digest.hexdigest()

    @classmethod
    def _load_bundle_from_cache(cls, actual_locale: str, fingerprint: str) -> FluentBundle | None:
        """Load a cached bundle when available."""
        cache_root = cls._resolve_cache_dir()
        if cache_root is None:
            return None

        cache_path = cache_root / actual_locale / f"{fingerprint}.pkl"
        if not cache_path.exists():
            return None

        try:
            with cache_path.open("rb") as fh:
                payload = pickle.load(fh)
            if payload.get("version") != cls._CACHE_VERSION:
                raise ValueError("Cache version mismatch")
            module_ast = payload["module_ast"]
            function_names = payload["function_names"]
            errors = payload.get("errors", [])
            compiled_messages = cls._rebuild_compiled_messages(actual_locale, module_ast, function_names)
        except Exception:
            try:
                cache_path.unlink()
            except FileNotFoundError:
                pass
            return None

        bundle = object.__new__(FluentBundle)
        bundle.locale = actual_locale
        bundle._compiled_messages = compiled_messages
        bundle._compilation_errors = errors
        return bundle

    @classmethod
    def _rebuild_compiled_messages(
        cls,
        actual_locale: str,
        module_ast,
        function_names: dict[str, str],
    ) -> dict[str, object]:
        """Rebuild compiled message functions from cached AST."""
        module_globals = cls._build_module_globals(actual_locale)
        code_obj = compile(module_ast, f"<fluent:{actual_locale}>", "exec")
        exec(code_obj, module_globals)
        compiled_messages: dict[str, object] = {}
        for message_id, function_name in function_names.items():
            func = module_globals.get(function_name)
            if func is None:
                raise RuntimeError(f"Missing cached function '{function_name}' for locale '{actual_locale}'.")
            compiled_messages[message_id] = func
        return compiled_messages

    @classmethod
    def _compile_bundle(cls, actual_locale: str, payloads: list[str], fingerprint: str) -> FluentBundle:
        """Compile locale files and persist cache entry."""
        resources = [FtlResource.from_string(text) for text in payloads]
        compiled = compile_messages(actual_locale, resources)
        bundle = object.__new__(FluentBundle)
        bundle.locale = actual_locale
        bundle._compiled_messages = compiled.message_functions
        bundle._compilation_errors = compiled.errors
        cls._write_cache_entry(actual_locale, fingerprint, compiled)
        return bundle

    @classmethod
    def _resolve_cache_dir(cls) -> Path | None:
        """Resolve (or create) the cache directory."""
        if not cls._cache_enabled:
            return None
        if cls._cache_dir is not None:
            return cls._cache_dir
        base = os.environ.get(cls._CACHE_DIR_ENV)
        if base:
            path = Path(base)
        elif cls._locales_dir is not None:
            path = cls._locales_dir.parent / ".cache" / "locales"
        else:
            return None
        path.mkdir(parents=True, exist_ok=True)
        cls._cache_dir = path
        return cls._cache_dir

    @classmethod
    def _write_cache_entry(cls, actual_locale: str, fingerprint: str, compiled) -> None:
        """Persist compiled bundle artifacts for reuse."""
        if compiled.module_ast is None:
            return
        cache_root = cls._resolve_cache_dir()
        if cache_root is None:
            return
        entry_dir = cache_root / actual_locale
        entry_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": cls._CACHE_VERSION,
            "fingerprint": fingerprint,
            "locale": actual_locale,
            "function_names": {msg_id: func.__name__ for msg_id, func in compiled.message_functions.items()},
            "module_ast": compiled.module_ast,
            "errors": compiled.errors,
        }
        tmp_path = entry_dir / f"{fingerprint}.tmp"
        final_path = entry_dir / f"{fingerprint}.pkl"
        with tmp_path.open("wb") as fh:
            pickle.dump(payload, fh)
        os.replace(tmp_path, final_path)
        for cached in entry_dir.glob("*.pkl"):
            if cached == final_path:
                continue
            try:
                cached.unlink()
            except OSError:
                pass

    @classmethod
    def _build_module_globals(cls, locale_name: str) -> dict[str, object]:
        """Recreate the runtime globals used by fluent_compiler."""
        module_globals = {name: getattr(runtime, name) for name in runtime.__all__}
        module_globals.update(builtins.__dict__)
        module_globals["__builtins__"] = builtins.__dict__
        babel_locale = cls._parse_locale(locale_name)
        plural_func = plural.to_python(babel_locale.plural_form)

        def plural_form_for_number(number):
            try:
                return plural_func(number)
            except TypeError:
                return None

        module_globals[PLURAL_FORM_FOR_NUMBER_NAME] = plural_form_for_number
        module_globals[LOCALE_NAME] = babel_locale
        module_globals["__name__"] = f"fluent_cache_{locale_name}"
        module_globals["__package__"] = None
        return module_globals

    @staticmethod
    def _parse_locale(locale_name: str) -> Locale:
        """Parse a locale string, defaulting to English on error."""
        normalized = locale_name.replace("-", "_")
        try:
            return Locale.parse(normalized)
        except (ValueError, UnknownLocaleError):
            return Locale.parse("en")

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
