"""
Declarative Options System for PlayPalace Games.

This module provides a way to define game options declaratively, reducing
boilerplate code for option handling, validation, and UI generation.

Usage:
    @dataclass
    class MyGameOptions(GameOptions):
        target_score: int = option_field(
            IntOption(default=50, min_val=10, max_val=1000,
                      label="game-set-target-score",
                      prompt="game-enter-target-score",
                      change_msg="game-option-changed-target"))
        team_mode: str = option_field(
            MenuOption(default="individual",
                       choices=["individual", "2v2"],
                       label="game-set-team-mode",
                       prompt="game-select-team-mode",
                       change_msg="game-option-changed-team"))
        show_hints: bool = option_field(
            BoolOption(default=False,
                       label="my-game-toggle-hints",
                       change_msg="my-game-option-changed-hints"))
"""

from dataclasses import dataclass, field, fields
from typing import Any, Callable, TYPE_CHECKING

from mashumaro.mixins.json import DataClassJSONMixin

from .actions import Action, ActionSet, EditboxInput, MenuInput
from ..messages.localization import Localization

if TYPE_CHECKING:
    from ..games.base import Game, Player


@dataclass
class OptionMeta:
    """Base metadata for a game option.

    Attributes:
        default: Default option value.
        label: Localization key for the option label.
        change_msg: Localization key for change announcements.
        prompt: Localization key for input prompt (if applicable).
    """

    default: Any
    label: str  # Localization key for the option label
    change_msg: str  # Localization key for the change announcement
    prompt: str = ""  # Localization key for input prompt (if applicable)

    def get_label(self, locale: str, value: Any) -> str:
        """Get the localized label with current value interpolated."""
        raise NotImplementedError

    def get_label_kwargs(self, value: Any) -> dict[str, Any]:
        """Get kwargs for label localization."""
        raise NotImplementedError

    def get_change_kwargs(self, value: Any) -> dict[str, Any]:
        """Get kwargs for change message localization."""
        raise NotImplementedError

    def create_action(
        self,
        option_name: str,
        game: "Game",
        player: "Player",
        current_value: Any,
        locale: str,
    ) -> Action:
        """Create an Action for this option."""
        raise NotImplementedError

    def validate_and_convert(self, value: str) -> tuple[bool, Any]:
        """Validate and convert input string to the option's type.

        Returns (success, converted_value). If success is False, converted_value
        is the original string.
        """
        raise NotImplementedError


@dataclass
class IntOption(OptionMeta):
    """Integer option with min/max validation.

    Attributes:
        min_val: Minimum value (inclusive).
        max_val: Maximum value (inclusive).
        value_key: Localization placeholder key for the value.
    """

    min_val: int = 0
    max_val: int = 100
    value_key: str = (
        "score"  # Key used in localization (e.g., "score", "points", "sides")
    )

    def get_label_kwargs(self, value: Any) -> dict[str, Any]:
        """Return label formatting kwargs for the current value."""
        return {self.value_key: value}

    def get_change_kwargs(self, value: Any) -> dict[str, Any]:
        """Return change-message kwargs for the current value."""
        return {self.value_key: value}

    def create_action(
        self,
        option_name: str,
        game: "Game",
        player: "Player",
        current_value: Any,
        locale: str,
    ) -> Action:
        """Create an editbox action for setting an integer option."""
        label = Localization.get(
            locale, self.label, **self.get_label_kwargs(current_value)
        )
        return Action(
            id=f"set_{option_name}",
            label=label,
            handler="_action_set_option",  # Generic handler extracts option_name from action_id
            is_enabled="_is_option_enabled",
            is_hidden="_is_option_hidden",
            show_in_actions_menu=False,
            input_request=EditboxInput(
                prompt=self.prompt,
                default=str(current_value),
            ),
        )

    def validate_and_convert(self, value: str) -> tuple[bool, Any]:
        """Validate and clamp integer input."""
        try:
            int_val = int(value)
            int_val = max(self.min_val, min(self.max_val, int_val))
            return True, int_val
        except ValueError:
            return False, value


@dataclass
class FloatOption(OptionMeta):
    """Float option with min/max validation and rounding.

    Attributes:
        min_val: Minimum value (inclusive).
        max_val: Maximum value (inclusive).
        decimal_places: Decimal places to round to.
        value_key: Localization placeholder key for the value.
    """

    min_val: float = 0.0
    max_val: float = 100.0
    decimal_places: int = 1  # Round to this many decimal places
    value_key: str = (
        "value"  # Key used in localization (e.g., "value", "amount", "rate")
    )

    def get_label_kwargs(self, value: Any) -> dict[str, Any]:
        """Return label formatting kwargs for the current value."""
        return {self.value_key: value}

    def get_change_kwargs(self, value: Any) -> dict[str, Any]:
        """Return change-message kwargs for the current value."""
        return {self.value_key: value}

    def create_action(
        self,
        option_name: str,
        game: "Game",
        player: "Player",
        current_value: Any,
        locale: str,
    ) -> Action:
        """Create an editbox action for setting a float option."""
        label = Localization.get(
            locale, self.label, **self.get_label_kwargs(current_value)
        )
        return Action(
            id=f"set_{option_name}",
            label=label,
            handler="_action_set_option",  # Generic handler extracts option_name from action_id
            is_enabled="_is_option_enabled",
            is_hidden="_is_option_hidden",
            show_in_actions_menu=False,
            input_request=EditboxInput(
                prompt=self.prompt,
                default=str(current_value),
            ),
        )

    def validate_and_convert(self, value: str) -> tuple[bool, Any]:
        """Validate and clamp float input."""
        try:
            float_val = float(value)
            float_val = max(self.min_val, min(self.max_val, float_val))
            float_val = round(float_val, self.decimal_places)
            return True, float_val
        except ValueError:
            return False, value


@dataclass
class MenuOption(OptionMeta):
    """Menu selection option.

    Attributes:
        choices: Static list or callable to provide choices.
        value_key: Localization placeholder key for the value.
        choice_labels: Optional mapping of choice -> localization key.
    """

    choices: list[str] | Callable[["Game", "Player"], list[str]] = field(
        default_factory=list
    )
    value_key: str = "mode"  # Key used in localization
    # Map choice values to localization keys for display
    # If not provided, raw choice values are displayed
    choice_labels: dict[str, str] | None = None

    def get_localized_choice(self, value: str, locale: str) -> str:
        """Get the localized display text for a choice value."""
        if self.choice_labels and value in self.choice_labels:
            return Localization.get(locale, self.choice_labels[value])
        return value

    def get_label_kwargs(self, value: Any) -> dict[str, Any]:
        """Return label formatting kwargs for the current value."""
        return {self.value_key: value}

    def get_label_kwargs_localized(self, value: Any, locale: str) -> dict[str, Any]:
        """Get kwargs with localized choice value."""
        display_value = self.get_localized_choice(value, locale)
        return {self.value_key: display_value}

    def get_change_kwargs(self, value: Any) -> dict[str, Any]:
        """Return change-message kwargs for the current value."""
        return {self.value_key: value}

    def get_change_kwargs_localized(self, value: Any, locale: str) -> dict[str, Any]:
        """Get kwargs with localized choice value for change message."""
        display_value = self.get_localized_choice(value, locale)
        return {self.value_key: display_value}

    def create_action(
        self,
        option_name: str,
        game: "Game",
        player: "Player",
        current_value: Any,
        locale: str,
    ) -> Action:
        """Create a menu action for selecting a value from choices."""
        # Use localized choice value in the label
        label = Localization.get(
            locale, self.label, **self.get_label_kwargs_localized(current_value, locale)
        )

        return Action(
            id=f"set_{option_name}",
            label=label,
            handler="_action_set_option",  # Generic handler extracts option_name from action_id
            is_enabled="_is_option_enabled",
            is_hidden="_is_option_hidden",
            show_in_actions_menu=False,
            input_request=MenuInput(
                prompt=self.prompt,
                options=f"_options_for_{option_name}",
            ),
        )

    def validate_and_convert(self, value: str) -> tuple[bool, Any]:
        """Validate a menu option selection."""
        # For menu options, the value comes from a predefined list, so it's valid
        return True, value

    def get_choices(self, game: "Game", player: "Player") -> list[str]:
        """Get the list of choices for this option."""
        if callable(self.choices):
            return self.choices(game, player)
        return list(self.choices)


@dataclass
class TeamModeOption(MenuOption):
    """Menu option specialized for team modes.

    Stores team modes in internal format ("individual", "2v2", "2v2v2") but
    displays them in localized format ("Individual", "2 teams of 2").
    """

    def get_localized_choice(self, value: str, locale: str) -> str:
        """Convert internal team mode format to localized display format."""
        from .teams import TeamManager

        return TeamManager.format_team_mode_for_display(value, locale)


@dataclass
class BoolOption(OptionMeta):
    """Boolean toggle option.

    Attributes:
        value_key: Localization placeholder key for the value.
    """

    value_key: str = "enabled"  # Key used in localization

    def __post_init__(self):
        """Disable prompts for boolean toggles."""
        # Bool options don't need a prompt - they just toggle
        self.prompt = ""

    def get_label_kwargs(self, value: Any) -> dict[str, Any]:
        """Return label formatting kwargs for the current value."""
        return {self.value_key: "on" if value else "off"}

    def get_change_kwargs(self, value: Any) -> dict[str, Any]:
        """Return change-message kwargs for the current value."""
        return {self.value_key: "on" if value else "off"}

    def create_action(
        self,
        option_name: str,
        game: "Game",
        player: "Player",
        current_value: Any,
        locale: str,
    ) -> Action:
        """Create a toggle action for boolean options."""
        # Get localized on/off value
        on_off_key = "option-on" if current_value else "option-off"
        on_off = Localization.get(locale, on_off_key)
        label = Localization.get(locale, self.label, **{self.value_key: on_off})
        return Action(
            id=f"toggle_{option_name}",
            label=label,
            handler="_action_toggle_option",  # Generic handler extracts option_name from action_id
            is_enabled="_is_option_enabled",
            is_hidden="_is_option_hidden",
            show_in_actions_menu=False,
            # No input_request - toggles directly
        )

    def validate_and_convert(self, value: str) -> tuple[bool, Any]:
        """Validate a boolean input value."""
        # For bool options, we just flip the value
        return True, value.lower() in ("true", "1", "yes")


@dataclass
class OptionGroupMeta:
    """Metadata for an option group (sub-menu of options).

    Attributes:
        label: Localization key for the group header label.
    """

    label: str

    def create_action(
        self,
        group_name: str,
        game: "Game",
        player: "Player",
        locale: str,
    ) -> Action:
        """Create an action that opens this option group's sub-menu."""
        label = Localization.get(locale, self.label)
        return Action(
            id=f"group_{group_name}",
            label=label,
            handler="_action_open_option_group",
            is_enabled="_is_option_enabled",
            is_hidden="_is_option_hidden",
            show_in_actions_menu=False,
        )


@dataclass
class MultiSelectOption(OptionMeta):
    """Multi-select option where multiple choices can be toggled on/off.

    Stores a list of selected choice strings. Displayed as a sub-menu of
    boolean toggles.

    Attributes:
        choices: Static list or no-arg callable returning available choices.
        min_selected: Minimum number of choices that must be selected.
        max_selected: Maximum number of choices that can be selected (0 = no limit).
        choice_labels: Optional mapping of choice -> localization key for display.
        show_bulk_actions: If True, show "Select all" / "Deselect all" in the toggle list.
        groups: Optional grouping of choices. When set, the top-level multi-select
            shows group names as navigable sub-menus instead of individual choices.
            Dict maps group name -> list of choice strings in that group.
    """

    choices: list[str] | Callable[[], list[str]] = field(default_factory=list)
    min_selected: int = 1
    max_selected: int = 0  # 0 = no limit (all choices can be selected)
    choice_labels: dict[str, str] | None = None
    show_bulk_actions: bool = False
    groups: dict[str, list[str]] | Callable[[], dict[str, list[str]]] | None = None

    def get_choices(self) -> list[str]:
        """Get the list of available choices."""
        if callable(self.choices):
            return self.choices()
        return list(self.choices)

    def get_groups(self) -> dict[str, list[str]] | None:
        """Get the group mapping, if any."""
        if self.groups is None:
            return None
        if callable(self.groups):
            return self.groups()
        return dict(self.groups)

    def get_localized_choice(self, value: str, locale: str) -> str:
        """Get the localized display text for a choice value."""
        if self.choice_labels and value in self.choice_labels:
            return Localization.get(locale, self.choice_labels[value])
        return value

    def get_label_kwargs(self, value: Any) -> dict[str, Any]:
        """Return label formatting kwargs for the current value (list)."""
        return {
            "count": len(value) if isinstance(value, list) else 0,
            "total": len(self.get_choices()),
        }

    def get_change_kwargs(self, value: Any) -> dict[str, Any]:
        """Return change-message kwargs for the current value."""
        return {
            "count": len(value) if isinstance(value, list) else 0,
            "total": len(self.get_choices()),
        }

    def create_action(
        self,
        option_name: str,
        game: "Game",
        player: "Player",
        current_value: Any,
        locale: str,
    ) -> Action:
        """Create an action that opens the multi-select sub-menu."""
        count = len(current_value) if isinstance(current_value, list) else 0
        label = Localization.get(
            locale, self.label, **self.get_label_kwargs(current_value)
        )
        return Action(
            id=f"multiselect_{option_name}",
            label=label,
            handler="_action_open_multiselect",
            is_enabled="_is_option_enabled",
            is_hidden="_is_option_hidden",
            show_in_actions_menu=False,
        )

    def validate_and_convert(self, value: str) -> tuple[bool, Any]:
        """Not used for multi-select (toggles are handled individually)."""
        return True, value


def option_group(label: str) -> Any:
    """Create a dataclass field for an option group (sub-menu header).

    Args:
        label: Localization key for the group label.

    Returns:
        Dataclass field with OptionGroupMeta in metadata.
    """
    meta = OptionGroupMeta(label=label)
    return field(default=None, metadata={"option_group_meta": meta})


def multi_select_field(meta: MultiSelectOption) -> Any:
    """Create a dataclass field for a multi-select option.

    Args:
        meta: MultiSelectOption metadata instance.

    Returns:
        Dataclass field configured for multi-select options.
    """
    default_val = list(meta.default) if isinstance(meta.default, list) else []
    return field(
        default_factory=lambda d=default_val: list(d),
        metadata={"option_meta": meta},
    )


def option_field(
    meta: OptionMeta,
    *,
    group: str | None = None,
    visible_when: tuple[str, Callable[[Any], bool]] | None = None,
) -> Any:
    """Create a dataclass field with option metadata attached.

    Args:
        meta: Option metadata instance.
        group: Name of the parent option group (None = top level).
        visible_when: Tuple of (option_name, predicate). The option is hidden
            when the predicate returns False for the referenced option's value.

    Returns:
        Dataclass field configured for declarative options.
    """
    metadata = {"option_meta": meta}
    if group is not None:
        metadata["option_group"] = group
    if visible_when is not None:
        metadata["visible_when"] = visible_when
    return field(default=meta.default, metadata=metadata)


def get_option_meta(options_class: type, field_name: str) -> OptionMeta | None:
    """Get OptionMeta for a field, if present."""
    for f in fields(options_class):
        if f.name == field_name:
            return f.metadata.get("option_meta")
    return None


def get_all_option_metas(options_class: type) -> dict[str, OptionMeta]:
    """Get all OptionMeta instances from an options class."""
    result = {}
    for f in fields(options_class):
        meta = f.metadata.get("option_meta")
        if meta is not None:
            result[f.name] = meta
    return result


def get_all_option_group_metas(options_class: type) -> dict[str, OptionGroupMeta]:
    """Get all OptionGroupMeta instances from an options class."""
    result = {}
    for f in fields(options_class):
        meta = f.metadata.get("option_group_meta")
        if meta is not None:
            result[f.name] = meta
    return result


def get_option_field_group(options_class: type, field_name: str) -> str | None:
    """Get the group name for an option field, if assigned to a group."""
    for f in fields(options_class):
        if f.name == field_name:
            return f.metadata.get("option_group")
    return None


def get_visibility_condition(
    options_class: type, field_name: str
) -> tuple[str, Callable[[Any], bool]] | None:
    """Get the visible_when condition for an option field, if present."""
    for f in fields(options_class):
        if f.name == field_name:
            return f.metadata.get("visible_when")
    return None


@dataclass
class GameOptions(DataClassJSONMixin):
    """Base class for declarative game options.

    Subclasses should use option_field() for options that need auto-generated
    UI and handlers.
    """

    def get_option_metas(self) -> dict[str, OptionMeta]:
        """Get all option metadata for this options instance."""
        return get_all_option_metas(type(self))

    def get_option_group_metas(self) -> dict[str, OptionGroupMeta]:
        """Get all option group metadata for this options instance."""
        return get_all_option_group_metas(type(self))

    def _is_option_visible(self, name: str) -> bool:
        """Check if an option passes its visible_when condition."""
        condition = get_visibility_condition(type(self), name)
        if condition is None:
            return True
        ref_name, predicate = condition
        ref_value = getattr(self, ref_name, None)
        return predicate(ref_value)

    def _get_options_path(self, game: "Game", player: "Player") -> list[str]:
        """Get the current options navigation path for a player."""
        if hasattr(game, "_options_path"):
            return game._options_path.get(player.id, [])
        return []

    def _populate_action_set(
        self, action_set: ActionSet, game: "Game", player: "Player", locale: str
    ) -> None:
        """Populate an action set with options for the player's current path."""
        path = self._get_options_path(game, player)
        options_class = type(self)

        if path:
            current_level = path[-1]

            # Check if we're inside a group of a MultiSelectOption
            # Path pattern: [..., "option_name", "group:GroupName"]
            if current_level.startswith("group:") and len(path) >= 2:
                option_name = path[-2]
                group_name = current_level.removeprefix("group:")
                meta = get_option_meta(options_class, option_name)
                if meta and isinstance(meta, MultiSelectOption):
                    groups = meta.get_groups()
                    if groups and group_name in groups:
                        group_choices = groups[group_name]
                        current_selections = getattr(self, option_name, [])
                        for choice in group_choices:
                            selected = choice in current_selections
                            on_off_key = "option-on" if selected else "option-off"
                            on_off = Localization.get(locale, on_off_key)
                            display = meta.get_localized_choice(choice, locale)
                            label = f"{display}: {on_off}"
                            action_set.add(Action(
                                id=f"mstoggle_{option_name}_{choice}",
                                label=label,
                                handler="_action_toggle_multiselect",
                                is_enabled="_is_option_enabled",
                                is_hidden="_is_option_hidden",
                                show_in_actions_menu=False,
                            ))
                        # Bulk actions scoped to this group
                        if meta.show_bulk_actions:
                            action_set.add(Action(
                                id=f"mselectall_{option_name}",
                                label=Localization.get(locale, "option-select-all"),
                                handler="_action_select_all_multiselect",
                                is_enabled="_is_option_enabled",
                                is_hidden="_is_option_hidden",
                                show_in_actions_menu=False,
                            ))
                            action_set.add(Action(
                                id=f"mdeselectall_{option_name}",
                                label=Localization.get(locale, "option-deselect-all"),
                                handler="_action_deselect_all_multiselect",
                                is_enabled="_is_option_enabled",
                                is_hidden="_is_option_hidden",
                                show_in_actions_menu=False,
                            ))
                        # Back action
                        back_label = Localization.get(locale, "option-back")
                        action_set.add(Action(
                            id="options_back",
                            label=back_label,
                            handler="_action_options_back",
                            is_enabled="_is_option_enabled",
                            is_hidden="_is_option_hidden",
                            show_in_actions_menu=False,
                        ))
                        return

            # Check if current level is a MultiSelectOption
            meta = get_option_meta(options_class, current_level)
            if meta and isinstance(meta, MultiSelectOption):
                current_selections = getattr(self, current_level, [])
                groups = meta.get_groups()

                if groups:
                    # Show group names as navigable sub-menus
                    for group_name, group_choices in groups.items():
                        selected_count = sum(
                            1 for c in group_choices if c in current_selections
                        )
                        total_count = len(group_choices)
                        label = f"{group_name} ({selected_count} of {total_count} selected)"
                        action_set.add(Action(
                            id=f"msgroup_{current_level}_{group_name}",
                            label=label,
                            handler="_action_open_ms_group",
                            is_enabled="_is_option_enabled",
                            is_hidden="_is_option_hidden",
                            show_in_actions_menu=False,
                        ))
                else:
                    # Show toggle actions for each choice
                    choices = meta.get_choices()
                    for choice in choices:
                        selected = choice in current_selections
                        on_off_key = "option-on" if selected else "option-off"
                        on_off = Localization.get(locale, on_off_key)
                        display = meta.get_localized_choice(choice, locale)
                        label = f"{display}: {on_off}"
                        action_set.add(Action(
                            id=f"mstoggle_{current_level}_{choice}",
                            label=label,
                            handler="_action_toggle_multiselect",
                            is_enabled="_is_option_enabled",
                            is_hidden="_is_option_hidden",
                            show_in_actions_menu=False,
                        ))
                    # Bulk actions (non-grouped)
                    if meta.show_bulk_actions:
                        action_set.add(Action(
                            id=f"mselectall_{current_level}",
                            label=Localization.get(locale, "option-select-all"),
                            handler="_action_select_all_multiselect",
                            is_enabled="_is_option_enabled",
                            is_hidden="_is_option_hidden",
                            show_in_actions_menu=False,
                        ))
                        action_set.add(Action(
                            id=f"mdeselectall_{current_level}",
                            label=Localization.get(locale, "option-deselect-all"),
                            handler="_action_deselect_all_multiselect",
                            is_enabled="_is_option_enabled",
                            is_hidden="_is_option_hidden",
                            show_in_actions_menu=False,
                        ))

                # Back action (with validation)
                back_label = Localization.get(locale, "option-back")
                action_set.add(Action(
                    id="options_back",
                    label=back_label,
                    handler="_action_options_back_multiselect",
                    is_enabled="_is_option_enabled",
                    is_hidden="_is_option_hidden",
                    show_in_actions_menu=False,
                ))
                return

            # Inside an option group — show children of this group + back
            target_group = current_level
        else:
            # Top level — show ungrouped options + group headers
            target_group = None

        # Add option group headers at this level
        for group_name, group_meta in self.get_option_group_metas().items():
            # Groups are top-level only if they have no group assignment themselves
            group_parent = get_option_field_group(options_class, group_name)
            if group_parent == target_group:
                action = group_meta.create_action(group_name, game, player, locale)
                action_set.add(action)

        # Add regular options at this level
        for name, meta in self.get_option_metas().items():
            option_group_name = get_option_field_group(options_class, name)
            if option_group_name != target_group:
                continue
            # Check linked visibility
            if not self._is_option_visible(name):
                continue
            current_value = getattr(self, name)
            action = meta.create_action(name, game, player, current_value, locale)
            action_set.add(action)

        # Add back action if inside a group
        if path:
            back_label = Localization.get(locale, "option-back")
            action_set.add(Action(
                id="options_back",
                label=back_label,
                handler="_action_options_back",
                is_enabled="_is_option_enabled",
                is_hidden="_is_option_hidden",
                show_in_actions_menu=False,
            ))

    def create_options_action_set(self, game: "Game", player: "Player") -> ActionSet:
        """Create an ActionSet with options for the player's current navigation level."""
        user = game.get_user(player)
        locale = user.locale if user else "en"
        action_set = ActionSet(name="options")
        self._populate_action_set(action_set, game, player, locale)
        return action_set

    def update_options_labels(self, game: "Game") -> None:
        """Update options action sets for all players to reflect current values.

        Updates the existing action set in-place to avoid duplicates.
        """
        for player in game.players:
            existing_set = game.get_action_set(player, "options")
            if existing_set:
                existing_set._actions.clear()
                existing_set._order.clear()
                user = game.get_user(player)
                locale = user.locale if user else "en"
                self._populate_action_set(existing_set, game, player, locale)
            else:
                new_options_set = self.create_options_action_set(game, player)
                game.add_action_set(player, new_options_set)


class OptionsHandlerMixin:
    """Handle declarative options for games.

    Expected Game attributes:
        options: GameOptions instance.
        get_user(player) -> User | None.
        rebuild_all_menus().
        _options_path: dict[str, list[str]] (player_id -> navigation stack).
    """

    def _is_in_options_submenu(self, player: "Player") -> bool:
        """Check if a player is navigated into an options sub-menu."""
        if hasattr(self, "_options_path"):
            return bool(self._options_path.get(player.id))
        return False

    def get_all_visible_actions(self, player: "Player") -> list:
        """Get visible actions, filtering to only options when in a sub-menu.

        When a player is inside an options group or multi-select, only the
        options action set is shown (no lobby/turn actions cluttering the menu).
        """
        if self._is_in_options_submenu(player):
            options_set = self.get_action_set(player, "options")
            if options_set:
                return options_set.get_visible_actions(self, player)
            return []
        return super().get_all_visible_actions(player)

    def create_options_action_set(self, player: "Player") -> ActionSet:
        """Create the options action set for a player.

        If the game's options class uses declarative options (option_field),
        this will auto-generate the action set. Otherwise, subclasses should
        override this method.
        """
        if hasattr(self.options, "create_options_action_set"):
            return self.options.create_options_action_set(self, player)
        # Fallback for non-declarative options
        return ActionSet(name="options")

    def _handle_option_change(self, option_name: str, value: str) -> None:
        """Handle a declarative option change (int/menu options)."""
        meta = get_option_meta(type(self.options), option_name)
        if not meta:
            return

        success, converted = meta.validate_and_convert(value)
        if not success:
            return

        # Set the option value
        setattr(self.options, option_name, converted)

        # Update labels and rebuild menus
        if hasattr(self.options, "update_options_labels"):
            self.options.update_options_labels(self)
        self.rebuild_all_menus()

    def _handle_option_toggle(self, option_name: str) -> None:
        """Handle a declarative boolean option toggle."""
        meta = get_option_meta(type(self.options), option_name)
        if not meta:
            return

        # Toggle the value
        current = getattr(self.options, option_name)
        new_value = not current
        setattr(self.options, option_name, new_value)

        # Update labels and rebuild menus
        if hasattr(self.options, "update_options_labels"):
            self.options.update_options_labels(self)
        self.rebuild_all_menus()

    # Generic option action handlers (extract option_name from action_id)

    def _action_set_option(self, player: "Player", value: str, action_id: str) -> None:
        """Generic handler for setting an option value.

        Extracts the option name from action_id (e.g., "set_total_rounds" -> "total_rounds")
        and delegates to _handle_option_change.
        """
        option_name = action_id.removeprefix("set_")
        self._handle_option_change(option_name, value)

    def _action_toggle_option(self, player: "Player", action_id: str) -> None:
        """Generic handler for toggling a boolean option.

        Extracts the option name from action_id (e.g., "toggle_show_hints" -> "show_hints")
        and delegates to _handle_option_toggle.
        """
        option_name = action_id.removeprefix("toggle_")
        self._handle_option_toggle(option_name)

    # Navigation handlers for option groups and multi-select

    def _action_open_option_group(self, player: "Player", action_id: str) -> None:
        """Open an option group's sub-menu.

        Pushes the group name onto the player's options path and rebuilds menus.
        """
        group_name = action_id.removeprefix("group_")
        if not hasattr(self, "_options_path"):
            self._options_path = {}
        path = self._options_path.setdefault(player.id, [])
        path.append(group_name)
        # Rebuild options action set for this player
        if hasattr(self.options, "update_options_labels"):
            self.options.update_options_labels(self)
        self.rebuild_all_menus()

    def _action_open_multiselect(self, player: "Player", action_id: str) -> None:
        """Open a multi-select option's sub-menu.

        Pushes the option name onto the player's options path and rebuilds menus.
        """
        option_name = action_id.removeprefix("multiselect_")
        if not hasattr(self, "_options_path"):
            self._options_path = {}
        path = self._options_path.setdefault(player.id, [])
        path.append(option_name)
        if hasattr(self.options, "update_options_labels"):
            self.options.update_options_labels(self)
        self.rebuild_all_menus()

    def _action_options_back(self, player: "Player", action_id: str) -> None:
        """Go back one level in the options navigation.

        Pops the last group from the player's options path and rebuilds menus.
        """
        if hasattr(self, "_options_path"):
            path = self._options_path.get(player.id, [])
            if path:
                path.pop()
        if hasattr(self.options, "update_options_labels"):
            self.options.update_options_labels(self)
        self.rebuild_all_menus()

    def _action_open_ms_group(self, player: "Player", action_id: str) -> None:
        """Open a multi-select group's sub-menu.

        Action ID format: msgroup_{option_name}_{group_name}
        Pushes 'group:{name}' onto the player's options path.
        """
        remainder = action_id.removeprefix("msgroup_")
        # Find which option this belongs to
        for name, meta in self.options.get_option_metas().items():
            if isinstance(meta, MultiSelectOption) and remainder.startswith(name + "_"):
                group_name = remainder[len(name) + 1:]
                if not hasattr(self, "_options_path"):
                    self._options_path = {}
                path = self._options_path.setdefault(player.id, [])
                path.append(f"group:{group_name}")
                if hasattr(self.options, "update_options_labels"):
                    self.options.update_options_labels(self)
                self.rebuild_all_menus()
                return

    def _action_select_all_multiselect(self, player: "Player", action_id: str) -> None:
        """Select all choices in the current multi-select view.

        Scoped to current group if inside one. Announces how many were added.
        """
        option_name = action_id.removeprefix("mselectall_")
        meta = get_option_meta(type(self.options), option_name)
        if not meta or not isinstance(meta, MultiSelectOption):
            return

        current_list = list(getattr(self.options, option_name, []))
        choices = self._get_scoped_choices(player, option_name, meta)

        added = 0
        for choice in choices:
            if choice not in current_list:
                current_list.append(choice)
                added += 1

        setattr(self.options, option_name, current_list)

        if added > 0:
            user = self.get_user(player)
            if user:
                user.speak_l("option-selected-count", count=added)

        if hasattr(self.options, "update_options_labels"):
            self.options.update_options_labels(self)
        self.rebuild_all_menus()

    def _action_deselect_all_multiselect(self, player: "Player", action_id: str) -> None:
        """Deselect all choices in the current multi-select view.

        Scoped to current group if inside one. Announces how many were removed.
        """
        option_name = action_id.removeprefix("mdeselectall_")
        meta = get_option_meta(type(self.options), option_name)
        if not meta or not isinstance(meta, MultiSelectOption):
            return

        current_list = list(getattr(self.options, option_name, []))
        choices = self._get_scoped_choices(player, option_name, meta)

        removed = 0
        for choice in choices:
            if choice in current_list:
                current_list.remove(choice)
                removed += 1

        setattr(self.options, option_name, current_list)

        if removed > 0:
            user = self.get_user(player)
            if user:
                user.speak_l("option-deselected-count", count=removed)

        if hasattr(self.options, "update_options_labels"):
            self.options.update_options_labels(self)
        self.rebuild_all_menus()

    def _get_scoped_choices(
        self, player: "Player", option_name: str, meta: "MultiSelectOption"
    ) -> list[str]:
        """Get the choices scoped to the current view (group or all).

        If the player is inside a group, returns only that group's choices.
        Otherwise returns all choices.
        """
        if hasattr(self, "_options_path"):
            path = self._options_path.get(player.id, [])
            if path and path[-1].startswith("group:"):
                group_name = path[-1].removeprefix("group:")
                groups = meta.get_groups()
                if groups and group_name in groups:
                    return groups[group_name]
        return meta.get_choices()

    def _action_options_back_multiselect(self, player: "Player", action_id: str) -> None:
        """Go back from a multi-select menu, validating selection count."""
        if hasattr(self, "_options_path"):
            path = self._options_path.get(player.id, [])
            if path:
                current = path[-1]
                # If going back from group level, just pop the group
                if current.startswith("group:"):
                    path.pop()
                    if hasattr(self.options, "update_options_labels"):
                        self.options.update_options_labels(self)
                    self.rebuild_all_menus()
                    return
                # Going back from option level — validate selection count
                meta = get_option_meta(type(self.options), current)
                if meta and isinstance(meta, MultiSelectOption):
                    current_list = getattr(self.options, current, [])
                    if len(current_list) < meta.min_selected:
                        user = self.get_user(player)
                        if user:
                            user.speak_l("option-min-selected", count=meta.min_selected)
                        return
                    if meta.max_selected > 0 and len(current_list) > meta.max_selected:
                        user = self.get_user(player)
                        if user:
                            user.speak_l("option-max-selected", count=meta.max_selected)
                        return
                path.pop()
        if hasattr(self.options, "update_options_labels"):
            self.options.update_options_labels(self)
        self.rebuild_all_menus()

    def _action_toggle_multiselect(self, player: "Player", action_id: str) -> None:
        """Toggle a choice in a multi-select option.

        Action ID format: mstoggle_{option_name}_{choice}
        """
        # Parse: remove "mstoggle_" prefix, then split on first "_" after option name
        remainder = action_id.removeprefix("mstoggle_")
        # We need to find the option name. Look through options to find a match.
        options_class = type(self.options)
        option_name = None
        choice = None
        for name, meta in self.options.get_option_metas().items():
            if isinstance(meta, MultiSelectOption) and remainder.startswith(name + "_"):
                option_name = name
                choice = remainder[len(name) + 1:]
                break
        if not option_name or choice is None:
            return

        meta = get_option_meta(options_class, option_name)
        if not meta or not isinstance(meta, MultiSelectOption):
            return

        current_list = list(getattr(self.options, option_name, []))
        if choice in current_list:
            current_list.remove(choice)
        else:
            current_list.append(choice)

        setattr(self.options, option_name, current_list)

        if hasattr(self.options, "update_options_labels"):
            self.options.update_options_labels(self)
        self.rebuild_all_menus()
