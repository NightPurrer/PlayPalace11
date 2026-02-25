from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import random

from .base import Game, GameOptions, Player
from .registry import register_game
from ..game_utils.action_guard_mixin import ActionGuardMixin
from ..game_utils.actions import Action, ActionSet, MenuInput, Visibility
from ..game_utils.bot_helper import BotHelper
from ..game_utils.cards import Card, Deck, card_name
from ..game_utils.game_result import GameResult, PlayerResult
from ..messages.localization import Localization
from server.core.ui.keybinds import KeybindState


MODIFIER_RAISE_1 = "raise_1"
MODIFIER_RAISE_2 = "raise_2"
MODIFIER_RAISE_2_PLUS = "raise_2_plus"
MODIFIER_DRAW_2 = "draw_2"
MODIFIER_DRAW_3 = "draw_3"
MODIFIER_DRAW_4 = "draw_4"
MODIFIER_DRAW_5 = "draw_5"
MODIFIER_DRAW_6 = "draw_6"
MODIFIER_DRAW_7 = "draw_7"
MODIFIER_SCRAP = "scrap"
MODIFIER_RECYCLE = "recycle"
MODIFIER_SWAP_DRAW = "swap_draw"
MODIFIER_REDRAFT = "redraft"
MODIFIER_REDRAFT_PLUS = "redraft_plus"
MODIFIER_GUARD = "guard"
MODIFIER_GUARD_PLUS = "guard_plus"
MODIFIER_BREAK = "break_effect"
MODIFIER_BREAK_PLUS = "break_all"
MODIFIER_LOCKDOWN = "lockdown"
MODIFIER_PRECISION_DRAW = "precision_draw"
MODIFIER_PRECISION_DRAW_PLUS = "precision_draw_plus"
MODIFIER_PRIME_DRAW = "prime_draw"
MODIFIER_TARGET_17 = "target_17"
MODIFIER_TARGET_24 = "target_24"
MODIFIER_TARGET_27 = "target_27"
MODIFIER_SALVAGE = "salvage"
MODIFIER_AID_RIVAL = "aid_rival"

MODIFIER_POOL = (
    MODIFIER_RAISE_1,
    MODIFIER_RAISE_2,
    MODIFIER_RAISE_2_PLUS,
    MODIFIER_DRAW_2,
    MODIFIER_DRAW_3,
    MODIFIER_DRAW_4,
    MODIFIER_DRAW_5,
    MODIFIER_DRAW_6,
    MODIFIER_DRAW_7,
    MODIFIER_SCRAP,
    MODIFIER_RECYCLE,
    MODIFIER_SWAP_DRAW,
    MODIFIER_REDRAFT,
    MODIFIER_REDRAFT_PLUS,
    MODIFIER_GUARD,
    MODIFIER_GUARD_PLUS,
    MODIFIER_BREAK,
    MODIFIER_BREAK_PLUS,
    MODIFIER_LOCKDOWN,
    MODIFIER_PRECISION_DRAW,
    MODIFIER_PRECISION_DRAW_PLUS,
    MODIFIER_PRIME_DRAW,
    MODIFIER_TARGET_17,
    MODIFIER_TARGET_24,
    MODIFIER_TARGET_27,
    MODIFIER_SALVAGE,
    MODIFIER_AID_RIVAL,
)

MODIFIER_LABELS = {
    MODIFIER_RAISE_1: "Stake Raise 1",
    MODIFIER_RAISE_2: "Stake Raise 2",
    MODIFIER_RAISE_2_PLUS: "Stake Raise 2+",
    MODIFIER_DRAW_2: "Exact 2",
    MODIFIER_DRAW_3: "Exact 3",
    MODIFIER_DRAW_4: "Exact 4",
    MODIFIER_DRAW_5: "Exact 5",
    MODIFIER_DRAW_6: "Exact 6",
    MODIFIER_DRAW_7: "Exact 7",
    MODIFIER_SCRAP: "Scrap Card",
    MODIFIER_RECYCLE: "Recycle Card",
    MODIFIER_SWAP_DRAW: "Swap Draw",
    MODIFIER_REDRAFT: "Redraft",
    MODIFIER_REDRAFT_PLUS: "Redraft+",
    MODIFIER_GUARD: "Guard",
    MODIFIER_GUARD_PLUS: "Guard+",
    MODIFIER_BREAK: "Break Effect",
    MODIFIER_BREAK_PLUS: "Break All",
    MODIFIER_LOCKDOWN: "Lockdown",
    MODIFIER_PRECISION_DRAW: "Precision Draw",
    MODIFIER_PRECISION_DRAW_PLUS: "Precision Draw+",
    MODIFIER_PRIME_DRAW: "Prime Draw",
    MODIFIER_TARGET_17: "Target 17",
    MODIFIER_TARGET_24: "Target 24",
    MODIFIER_TARGET_27: "Target 27",
    MODIFIER_SALVAGE: "Salvage",
    MODIFIER_AID_RIVAL: "Aid Rival",
}
MODIFIER_HELP = [
    (MODIFIER_RAISE_1, "Increase opponent damage by 1. Gain 1 random modifier."),
    (MODIFIER_RAISE_2, "Increase opponent damage by 2. Gain 1 random modifier."),
    (
        MODIFIER_RAISE_2_PLUS,
        "Increase opponent damage by 2, return opponent last drawn card to top of deck, and gain 1 random modifier.",
    ),
    (MODIFIER_DRAW_2, "Draw an exact 2 from deck if available."),
    (MODIFIER_DRAW_3, "Draw an exact 3 from deck if available."),
    (MODIFIER_DRAW_4, "Draw an exact 4 from deck if available."),
    (MODIFIER_DRAW_5, "Draw an exact 5 from deck if available."),
    (MODIFIER_DRAW_6, "Draw an exact 6 from deck if available."),
    (MODIFIER_DRAW_7, "Draw an exact 7 from deck if available."),
    (MODIFIER_SCRAP, "Remove opponent last drawn face-up card and place it on top of deck."),
    (MODIFIER_RECYCLE, "Return opponent last drawn face-up card to top of deck."),
    (
        MODIFIER_SWAP_DRAW,
        "Both players return their own last drawn face-up card and each draw one new card.",
    ),
    (MODIFIER_REDRAFT, "Discard 2 random modifiers, then gain 3 random modifiers."),
    (MODIFIER_REDRAFT_PLUS, "Discard 1 random modifier, then gain 4 random modifiers."),
    (MODIFIER_GUARD, "Reduce incoming round damage by 1 while active."),
    (MODIFIER_GUARD_PLUS, "Reduce incoming round damage by 2 while active."),
    (MODIFIER_BREAK, "Destroy opponent newest table effect."),
    (MODIFIER_BREAK_PLUS, "Destroy all opponent table effects."),
    (
        MODIFIER_LOCKDOWN,
        "Clear opponent table effects and lock opponent from playing modifiers while active.",
    ),
    (MODIFIER_PRECISION_DRAW, "Draw the best available card for current target."),
    (
        MODIFIER_PRECISION_DRAW_PLUS,
        "Precision draw plus increase opponent damage by 5 while active.",
    ),
    (MODIFIER_PRIME_DRAW, "Precision draw and gain 2 random modifiers."),
    (MODIFIER_TARGET_17, "Set round target to 17."),
    (MODIFIER_TARGET_24, "Set round target to 24."),
    (MODIFIER_TARGET_27, "Set round target to 27."),
    (
        MODIFIER_SALVAGE,
        "Whenever any modifier is played, gain 1 random modifier while active.",
    ),
    (MODIFIER_AID_RIVAL, "Opponent draws their best available card for current target."),
]
MODIFIER_HELP_MAP = {modifier_id: desc for modifier_id, desc in MODIFIER_HELP}

TABLE_EFFECT_MODIFIERS = {
    MODIFIER_RAISE_1,
    MODIFIER_RAISE_2,
    MODIFIER_RAISE_2_PLUS,
    MODIFIER_GUARD,
    MODIFIER_GUARD_PLUS,
    MODIFIER_LOCKDOWN,
    MODIFIER_PRECISION_DRAW_PLUS,
    MODIFIER_TARGET_17,
    MODIFIER_TARGET_24,
    MODIFIER_TARGET_27,
    MODIFIER_SALVAGE,
}

TARGET_VALUE_MODIFIERS = {
    MODIFIER_TARGET_17: 17,
    MODIFIER_TARGET_24: 24,
    MODIFIER_TARGET_27: 27,
}

TABLE_EFFECT_LIMIT = 5


@dataclass
class TwentyOneOptions(GameOptions):
    """Survival 21 defaults for Play Palace PvP."""

    starting_health: int = 10
    base_bet: int = 1
    starting_modifiers_per_round: int = 1
    draw_modifier_chance_percent: int = 35
    deck_count: int = 1
    next_round_wait_ticks: int = 30


@dataclass
class TwentyOnePlayer(Player):
    """Player state for Survival 21."""

    hand: list[Card] = field(default_factory=list)
    hp: int = 0
    modifiers: list[str] = field(default_factory=list)
    table_modifiers: list[str] = field(default_factory=list)
    stand_pending: bool = False
    last_drawn_card_id: int | None = None


@dataclass
@register_game
class TwentyOneGame(ActionGuardMixin, Game):
    """Survival 21 ruleset with tactical modifier cards."""

    players: list[TwentyOnePlayer] = field(default_factory=list)
    options: TwentyOneOptions = field(default_factory=TwentyOneOptions)
    deck: Deck | None = None
    phase: str = "lobby"  # lobby, turns, between_rounds, finished
    round_number: int = 0
    round_starter_index: int = 0
    next_round_wait_ticks: int = 0
    modifier_used_since_last_stand_resolution: bool = False

    @classmethod
    def get_name(cls) -> str:
        return "21 (Survival Rules)"

    @classmethod
    def get_name_key(cls) -> str:
        return "21"

    @classmethod
    def get_type(cls) -> str:
        return "twentyone"

    @classmethod
    def get_category(cls) -> str:
        return "category-card-games"

    @classmethod
    def get_min_players(cls) -> int:
        return 2

    @classmethod
    def get_max_players(cls) -> int:
        return 2

    def create_player(self, player_id: str, name: str, is_bot: bool = False) -> TwentyOnePlayer:
        return TwentyOnePlayer(id=player_id, name=name, is_bot=is_bot)

    def _is_turn_action_enabled(self, player: Player) -> str | None:
        error = self.guard_turn_action_enabled(player)
        if error:
            return error
        if self.phase != "turns":
            return "action-not-available"
        return None

    def _is_turn_action_hidden(self, player: Player) -> Visibility:
        return self.turn_action_visibility(player, extra_condition=self.phase == "turns")

    def _is_play_modifier_enabled(self, player: Player) -> str | None:
        error = self._is_turn_action_enabled(player)
        if error:
            return error
        p = player if isinstance(player, TwentyOnePlayer) else None
        if not p:
            return "action-not-available"
        if self._modifiers_locked_for(p):
            return "action-not-available"
        if not p.modifiers:
            return "action-not-available"
        return None

    def _is_play_modifier_hidden(self, player: Player) -> Visibility:
        p = player if isinstance(player, TwentyOnePlayer) else None
        if not p or not p.modifiers:
            return Visibility.HIDDEN
        if self._modifiers_locked_for(p):
            return Visibility.HIDDEN
        return self._is_turn_action_hidden(player)

    def _is_check_enabled(self, player: Player) -> str | None:
        if self.status != "playing":
            return "action-not-playing"
        if player.is_spectator:
            return "action-spectator"
        return None

    def _is_check_hidden(self, player: Player) -> Visibility:
        if self.status != "playing" or player.is_spectator:
            return Visibility.HIDDEN
        return Visibility.VISIBLE

    def create_turn_action_set(self, player: TwentyOnePlayer) -> ActionSet:
        user = self.get_user(player)
        locale = user.locale if user else "en"

        action_set = ActionSet(name="turn")
        action_set.add(
            Action(
                id="hit",
                label=Localization.get(locale, "blackjack-hit"),
                handler="_action_hit",
                is_enabled="_is_turn_action_enabled",
                is_hidden="_is_turn_action_hidden",
            )
        )
        action_set.add(
            Action(
                id="stand",
                label=Localization.get(locale, "blackjack-stand"),
                handler="_action_stand",
                is_enabled="_is_turn_action_enabled",
                is_hidden="_is_turn_action_hidden",
            )
        )
        action_set.add(
            Action(
                id="play_modifier",
                label="Play Modifier",
                handler="_action_play_modifier",
                is_enabled="_is_play_modifier_enabled",
                is_hidden="_is_play_modifier_hidden",
                input_request=MenuInput(
                    prompt="twentyone-select-modifier",
                    options="_options_for_play_modifier",
                    bot_select="_bot_select_play_modifier",
                ),
            )
        )
        return action_set

    def create_standard_action_set(self, player: Player) -> ActionSet:
        action_set = super().create_standard_action_set(player)
        action_set.add(
            Action(
                id="check_21_status",
                label="Check 21 status",
                handler="_action_check_status",
                is_enabled="_is_check_enabled",
                is_hidden="_is_check_hidden",
            )
        )
        action_set.add(
            Action(
                id="modifier_guide",
                label="Modifier Guide",
                handler="_action_modifier_guide",
                is_enabled="_is_check_enabled",
                is_hidden="_is_check_hidden",
            )
        )
        action_set.add(
            Action(
                id="read_21_opponent_face_up",
                label="Read opponent face-up cards",
                handler="_action_read_opponent_face_up",
                is_enabled="_is_check_enabled",
                is_hidden="_is_always_hidden",
            )
        )
        action_set.add(
            Action(
                id="read_21_hand",
                label="Read current hand",
                handler="_action_read_current_hand",
                is_enabled="_is_check_enabled",
                is_hidden="_is_always_hidden",
            )
        )
        action_set.add(
            Action(
                id="read_21_bets",
                label="Read current bets",
                handler="_action_read_current_bets",
                is_enabled="_is_check_enabled",
                is_hidden="_is_always_hidden",
            )
        )
        action_set.add(
            Action(
                id="read_21_active_effects",
                label="Read active modifier effects",
                handler="_action_read_active_effects",
                is_enabled="_is_check_enabled",
                is_hidden="_is_always_hidden",
            )
        )
        return action_set

    def setup_keybinds(self) -> None:
        super().setup_keybinds()
        self.define_keybind("1", "Hit", ["hit"], state=KeybindState.ACTIVE)
        self.define_keybind("2", "Stand", ["stand"], state=KeybindState.ACTIVE)
        self.define_keybind("3", "Play Modifier", ["play_modifier"], state=KeybindState.ACTIVE)
        self.define_keybind("4", "Check 21 status", ["check_21_status"], state=KeybindState.ACTIVE)
        self.define_keybind("m", "Modifier Guide", ["modifier_guide"], state=KeybindState.ACTIVE)
        self.define_keybind("o", "Read opponent face-up cards", ["read_21_opponent_face_up"], state=KeybindState.ACTIVE)
        self.define_keybind("r", "Read current hand", ["read_21_hand"], state=KeybindState.ACTIVE)
        self.define_keybind("b", "Read current bets", ["read_21_bets"], state=KeybindState.ACTIVE)
        self.define_keybind("e", "Read active effects", ["read_21_active_effects"], state=KeybindState.ACTIVE)

    def _options_for_play_modifier(self, player: Player) -> list[str]:
        p = player if isinstance(player, TwentyOnePlayer) else None
        if not p:
            return []
        options: list[str] = []
        for index, modifier in enumerate(p.modifiers):
            label = MODIFIER_LABELS.get(modifier, modifier)
            description = MODIFIER_HELP_MAP.get(modifier, "")
            if description:
                options.append(f"{index}:{label} - {description}")
            else:
                options.append(f"{index}:{label}")
        return options

    def _bot_select_play_modifier(self, player: Player, options: list[str]) -> str | None:
        p = player if isinstance(player, TwentyOnePlayer) else None
        if not p:
            return None
        target = self._current_target()
        opponent = self._opponent_of(p)
        if not opponent:
            return options[0] if options else None

        my_total = self._hand_total(p)
        opp_total = self._hand_total(opponent)

        preferred: list[str] = []
        if MODIFIER_LOCKDOWN in p.modifiers and opponent.modifiers:
            preferred.append(MODIFIER_LOCKDOWN)
        if my_total > target:
            if MODIFIER_TARGET_24 in p.modifiers:
                preferred.append(MODIFIER_TARGET_24)
            if MODIFIER_TARGET_27 in p.modifiers:
                preferred.append(MODIFIER_TARGET_27)
        if my_total < target:
            if MODIFIER_PRECISION_DRAW in p.modifiers:
                preferred.append(MODIFIER_PRECISION_DRAW)
            if MODIFIER_PRECISION_DRAW_PLUS in p.modifiers:
                preferred.append(MODIFIER_PRECISION_DRAW_PLUS)
            if MODIFIER_PRIME_DRAW in p.modifiers:
                preferred.append(MODIFIER_PRIME_DRAW)
        if p.hp <= opponent.hp:
            if MODIFIER_GUARD_PLUS in p.modifiers:
                preferred.append(MODIFIER_GUARD_PLUS)
            if MODIFIER_GUARD in p.modifiers:
                preferred.append(MODIFIER_GUARD)
        if opp_total >= target - 1:
            if MODIFIER_RAISE_2_PLUS in p.modifiers:
                preferred.append(MODIFIER_RAISE_2_PLUS)
            if MODIFIER_RAISE_2 in p.modifiers:
                preferred.append(MODIFIER_RAISE_2)
            if MODIFIER_RAISE_1 in p.modifiers:
                preferred.append(MODIFIER_RAISE_1)

        for modifier in preferred:
            if self._is_single_modifier_playable(p, modifier):
                return self._option_for_modifier(options, modifier)

        for modifier in p.modifiers:
            if self._is_single_modifier_playable(p, modifier):
                return self._option_for_modifier(options, modifier)
        return options[0] if options else None

    @staticmethod
    def _option_for_modifier(options: list[str], modifier: str) -> str | None:
        label = MODIFIER_LABELS.get(modifier, modifier)
        for option in options:
            body = option.split(":", 1)[1] if ":" in option else option
            if body == label or body.startswith(f"{label} -"):
                return option
        return None

    @staticmethod
    def _parse_modifier_option(option_value: str) -> int | None:
        try:
            prefix = option_value.split(":", 1)[0]
            return int(prefix)
        except (ValueError, IndexError):
            return None

    def _action_hit(self, player: Player, action_id: str) -> None:
        p = player if isinstance(player, TwentyOnePlayer) else None
        if not p:
            return

        card = self._draw_card()
        if not card:
            self.broadcast("Deck is empty. You can still choose to stay.")
            self.rebuild_all_menus()
            return

        self._clear_pending_stands()
        self._add_card_to_hand(
            p,
            card,
            announce_source=f"{p.name} draws",
            reveal_to_others=True,
        )
        p.stand_pending = False

        chance = max(0, min(100, self.options.draw_modifier_chance_percent))
        if random.randint(1, 100) <= chance:  # nosec B311
            self._give_random_modifiers(p, 1, announce=True)

        self.rebuild_all_menus()

    def _action_stand(self, player: Player, action_id: str) -> None:
        p = player if isinstance(player, TwentyOnePlayer) else None
        if not p:
            return

        p.stand_pending = True
        self.broadcast(f"{p.name} chooses to stay.")

        if self._both_players_standing():
            self._settle_round()
            return

        self._advance_turn_after_action()

    def _action_play_modifier(self, player: Player, selected: str, action_id: str) -> None:
        p = player if isinstance(player, TwentyOnePlayer) else None
        if not p:
            return

        choice_index = self._parse_modifier_option(selected)
        if choice_index is None or choice_index < 0 or choice_index >= len(p.modifiers):
            return

        modifier = p.modifiers.pop(choice_index)
        if not self._is_single_modifier_playable(p, modifier):
            p.modifiers.insert(choice_index, modifier)
            return

        self._clear_pending_stands()
        self.broadcast(f"{p.name} plays {MODIFIER_LABELS.get(modifier, modifier)}.")
        self._resolve_modifier(p, modifier)
        self.modifier_used_since_last_stand_resolution = True
        self._trigger_harvest_rewards()
        self.rebuild_all_menus()

    def _action_check_status(self, player: Player, action_id: str) -> None:
        p = player if isinstance(player, TwentyOnePlayer) else None
        if not p:
            return
        user = self.get_user(p)
        if not user:
            return

        target = self._current_target()
        bet = self._current_bet(p)
        hand_text = ", ".join(str(card.rank) for card in p.hand) if p.hand else "none"
        modifiers_text = ", ".join(MODIFIER_LABELS.get(t, t) for t in p.modifiers) if p.modifiers else "none"
        table_text = ", ".join(MODIFIER_LABELS.get(t, t) for t in p.table_modifiers) if p.table_modifiers else "none"
        user.speak(
            f"Target {target}. HP {p.hp}. Bet {bet}. Hand [{hand_text}] total {self._hand_total(p)}. "
            f"Modifiers in hand: {modifiers_text}. Table effects: {table_text}.",
            "table",
        )
        user.speak("Press M for the full modifier guide.", "table")
        opponent = self._opponent_of(p)
        if opponent:
            shown_cards = self._opponent_visible_cards(opponent)
            shown_text = ", ".join(str(card.rank) for card in shown_cards) if shown_cards else "none"
            shown_total = sum(card.rank for card in shown_cards)
            user.speak(
                f"{opponent.name}: HP {opponent.hp}, bet {self._current_bet(opponent)}, "
                f"shown cards [{shown_text}] shown total {shown_total}, hole card hidden.",
                "table",
            )

    def _action_modifier_guide(self, player: Player, action_id: str) -> None:
        p = player if isinstance(player, TwentyOnePlayer) else None
        if not p:
            return
        user = self.get_user(p)
        if not user:
            return

        user.speak("Modifier guide.", "table")
        for modifier_id, description in MODIFIER_HELP:
            name = MODIFIER_LABELS.get(modifier_id, modifier_id)
            user.speak(f"{name}: {description}", "table")
        user.speak(
            "Table effect limit is five. Target modifiers replace older target modifiers.",
            "table",
        )

    def _action_read_opponent_face_up(self, player: Player, action_id: str) -> None:
        p = player if isinstance(player, TwentyOnePlayer) else None
        if not p:
            return
        user = self.get_user(p)
        if not user:
            return
        opponent = self._opponent_of(p)
        if not opponent:
            user.speak("No opponent available.", "table")
            return

        shown_cards = self._opponent_visible_cards(opponent)
        shown_text = ", ".join(str(card.rank) for card in shown_cards) if shown_cards else "none"
        shown_total = sum(card.rank for card in shown_cards)
        user.speak(
            f"{opponent.name} face-up cards [{shown_text}] total {shown_total}. "
            "Hole card is hidden.",
            "table",
        )

    def _action_read_current_hand(self, player: Player, action_id: str) -> None:
        p = player if isinstance(player, TwentyOnePlayer) else None
        if not p:
            return
        user = self.get_user(p)
        if not user:
            return

        hand_text = ", ".join(str(card.rank) for card in p.hand) if p.hand else "none"
        user.speak(f"Your hand [{hand_text}] total {self._hand_total(p)}.", "table")

    def _action_read_current_bets(self, player: Player, action_id: str) -> None:
        p = player if isinstance(player, TwentyOnePlayer) else None
        if not p:
            return
        user = self.get_user(p)
        if not user:
            return

        my_bet = self._current_bet(p)
        opponent = self._opponent_of(p)
        if not opponent:
            user.speak(f"Current bet {my_bet}.", "table")
            return
        opponent_bet = self._current_bet(opponent)
        user.speak(
            f"Current bets. {p.name}: {my_bet}. {opponent.name}: {opponent_bet}.",
            "table",
        )

    def _action_read_active_effects(self, player: Player, action_id: str) -> None:
        p = player if isinstance(player, TwentyOnePlayer) else None
        if not p:
            return
        user = self.get_user(p)
        if not user:
            return

        my_effects = ", ".join(MODIFIER_LABELS.get(effect, effect) for effect in p.table_modifiers) if p.table_modifiers else "none"
        opponent = self._opponent_of(p)
        if not opponent:
            user.speak(f"Active effects. {p.name}: {my_effects}.", "table")
            return

        opponent_effects = ", ".join(
            MODIFIER_LABELS.get(effect, effect) for effect in opponent.table_modifiers
        ) if opponent.table_modifiers else "none"
        user.speak(
            f"Active effects. {p.name}: {my_effects}. {opponent.name}: {opponent_effects}.",
            "table",
        )

    def on_start(self) -> None:
        self.status = "playing"
        self.game_active = True
        self.phase = "turns"
        self.round_number = 0
        self.round_starter_index = 0
        self.next_round_wait_ticks = 0
        self.modifier_used_since_last_stand_resolution = False

        active = self.get_active_players()
        self._team_manager.team_mode = "individual"
        self._team_manager.setup_teams([p.name for p in active])
        self._team_manager.reset_all_scores()

        for player in active:
            if not isinstance(player, TwentyOnePlayer):
                continue
            player.hp = max(1, self.options.starting_health)
            player.hand.clear()
            player.modifiers.clear()
            player.table_modifiers.clear()
            player.stand_pending = False
            player.last_drawn_card_id = None

        self._sync_hp_scores()
        self._start_round(rotate_starter=False)

    def on_tick(self) -> None:
        super().on_tick()
        if not self.game_active or self.status != "playing":
            return

        if self.phase == "between_rounds":
            if self.next_round_wait_ticks > 0:
                self.next_round_wait_ticks -= 1
            if self.next_round_wait_ticks <= 0:
                self._start_round(rotate_starter=True)
            return

        if self.phase == "turns":
            BotHelper.on_tick(self)

    def _start_round(self, *, rotate_starter: bool) -> None:
        alive = self._alive_players()
        if len(alive) <= 1:
            self._end_game(alive[0] if alive else None)
            return

        if rotate_starter:
            self.round_starter_index = (self.round_starter_index + 1) % len(alive)
        if self.round_starter_index >= len(alive):
            self.round_starter_index = 0

        self.phase = "turns"
        self.round_number += 1
        self.modifier_used_since_last_stand_resolution = False

        self._build_round_deck()

        for player in alive:
            player.hand.clear()
            player.table_modifiers.clear()
            player.stand_pending = False
            player.last_drawn_card_id = None
            self._give_random_modifiers(player, self.options.starting_modifiers_per_round, announce=False)

        for deal_round in range(2):
            for player in alive:
                card = self._draw_card()
                if card:
                    reveal = deal_round > 0
                    self._add_card_to_hand(player, card, announce_source=None, reveal_to_others=reveal)

        self.set_turn_players(alive, reset_index=True)
        self.turn_index = self.round_starter_index

        self.broadcast(f"Round {self.round_number} begins. Target is {self._current_target()}.")
        for player in alive:
            shown = self._peek_last_drawn_card(player)
            if shown:
                self.broadcast(f"{player.name} shows {card_name(shown, 'en')} ({shown.rank}).")
            else:
                self.broadcast(f"{player.name} receives cards.")
            user = self.get_user(player)
            if user:
                if player.hand:
                    user.speak(f"Your hidden card is {card_name(player.hand[0], user.locale)} ({player.hand[0].rank}).", "table")
                if shown:
                    user.speak(f"Your shown card is {card_name(shown, user.locale)} ({shown.rank}).", "table")
                user.speak(f"Your total is {self._hand_total(player)}.", "table")
                modifiers_text = ", ".join(MODIFIER_LABELS.get(t, t) for t in player.modifiers) if player.modifiers else "none"
                user.speak(f"Your modifiers: {modifiers_text}.", "table")

        current = self.current_player
        if current:
            self.announce_turn()
            if current.is_bot:
                BotHelper.jolt_bot(current, ticks=random.randint(8, 16))  # nosec B311
        self.rebuild_all_menus()

    def _advance_turn_after_action(self) -> None:
        if self.phase != "turns":
            return
        self.advance_turn(announce=False)
        current = self.current_player
        if current:
            self.announce_turn()
            if current.is_bot:
                BotHelper.jolt_bot(current, ticks=random.randint(8, 16))  # nosec B311
        self.rebuild_all_menus()

    def _settle_round(self) -> None:
        players = self._alive_players()
        if len(players) < 2:
            self._end_game(players[0] if players else None)
            return

        self.phase = "between_rounds"
        p1, p2 = players[0], players[1]
        target = self._current_target()
        total_1 = self._hand_total(p1)
        total_2 = self._hand_total(p2)
        bust_1 = total_1 > target
        bust_2 = total_2 > target

        self.broadcast(
            f"Round totals (target {target}): {p1.name} {total_1}, {p2.name} {total_2}."
        )

        outcome = self._resolve_round_outcome(total_1, total_2, target)

        if outcome == "p1_wins":
            self._apply_round_loss_damage(p2)
            self.broadcast(f"{p1.name} wins the round.")
        elif outcome == "p2_wins":
            self._apply_round_loss_damage(p1)
            self.broadcast(f"{p2.name} wins the round.")
        else:
            self._apply_round_loss_damage(p1)
            self._apply_round_loss_damage(p2)
            self.broadcast("Round is a draw. Both players take damage.")

        if bust_1 and bust_2:
            self.broadcast("Both players busted; closer to target decides the winner.")
        elif bust_1:
            self.broadcast(f"{p1.name} busted.")
        elif bust_2:
            self.broadcast(f"{p2.name} busted.")

        self._sync_hp_scores()
        survivors = self._alive_players()
        if len(survivors) <= 1:
            self._end_game(survivors[0] if survivors else None)
            return

        self.next_round_wait_ticks = max(0, self.options.next_round_wait_ticks)
        self.rebuild_all_menus()

    @staticmethod
    def _resolve_round_outcome(total_1: int, total_2: int, target: int) -> str:
        bust_1 = total_1 > target
        bust_2 = total_2 > target
        if bust_1 and not bust_2:
            return "p2_wins"
        if bust_2 and not bust_1:
            return "p1_wins"
        if bust_1 and bust_2:
            diff_1 = abs(total_1 - target)
            diff_2 = abs(total_2 - target)
            if diff_1 < diff_2:
                return "p1_wins"
            if diff_2 < diff_1:
                return "p2_wins"
            return "draw"
        if total_1 > total_2:
            return "p1_wins"
        if total_2 > total_1:
            return "p2_wins"
        return "draw"

    def _apply_round_loss_damage(self, loser: TwentyOnePlayer) -> None:
        damage = max(0, self._current_bet(loser))
        if damage <= 0:
            self.broadcast(f"{loser.name} loses the round but bet is 0.")
            return
        loser.hp = max(0, loser.hp - damage)
        self.broadcast(f"{loser.name} takes {damage} damage and now has {loser.hp} HP.")

    def _end_game(self, winner: TwentyOnePlayer | None) -> None:
        self.phase = "finished"
        if winner:
            self.broadcast(f"{winner.name} wins 21 with {winner.hp} HP remaining.")
        else:
            self.broadcast("21 ends with no winner.")
        self.finish_game()

    def bot_think(self, player: TwentyOnePlayer) -> str | None:
        if self.phase != "turns" or self.current_player != player:
            return None

        opponent = self._opponent_of(player)
        if not opponent:
            return "stand"

        target = self._current_target()
        total = self._hand_total(player)
        opp_total = self._hand_total(opponent)

        if not self._modifiers_locked_for(player) and player.modifiers:
            if total > target and any(t in player.modifiers for t in TARGET_VALUE_MODIFIERS):
                return "play_modifier"
            if total < target - 5 and any(
                t in player.modifiers for t in (MODIFIER_PRECISION_DRAW, MODIFIER_PRECISION_DRAW_PLUS, MODIFIER_PRIME_DRAW)
            ):
                return "play_modifier"
            if opponent.stand_pending and total <= opp_total:
                if any(t in player.modifiers for t in (MODIFIER_RAISE_1, MODIFIER_RAISE_2, MODIFIER_RAISE_2_PLUS, MODIFIER_LOCKDOWN)):
                    return "play_modifier"
            if player.hp <= opponent.hp and any(t in player.modifiers for t in (MODIFIER_GUARD, MODIFIER_GUARD_PLUS)):
                return "play_modifier"

        if total < target - 2:
            return "hit"
        if opponent.stand_pending and total < opp_total and total <= target:
            return "hit"
        return "stand"

    def _resolve_modifier(self, player: TwentyOnePlayer, modifier: str) -> None:
        opponent = self._opponent_of(player)
        if not opponent:
            return

        if modifier == MODIFIER_RAISE_1:
            self._place_table_effect(player, modifier)
            self._give_random_modifiers(player, 1, announce=True)
            return

        if modifier == MODIFIER_RAISE_2:
            self._place_table_effect(player, modifier)
            self._give_random_modifiers(player, 1, announce=True)
            return

        if modifier == MODIFIER_RAISE_2_PLUS:
            self._place_table_effect(player, modifier)
            removed = self._extract_last_drawn_card(opponent)
            if removed:
                self._return_card_to_top_of_deck(removed)
                self.broadcast(f"{opponent.name}'s last face-up card is returned to top of deck.")
            self._give_random_modifiers(player, 1, announce=True)
            return

        if modifier in (MODIFIER_DRAW_2, MODIFIER_DRAW_3, MODIFIER_DRAW_4, MODIFIER_DRAW_5, MODIFIER_DRAW_6, MODIFIER_DRAW_7):
            rank = int(modifier.split("_")[1])
            card = self._draw_specific_rank(rank)
            if card:
                self._add_card_to_hand(
                    player,
                    card,
                    announce_source=f"{player.name} draws exact",
                    reveal_to_others=True,
                )
                player.stand_pending = False
            else:
                self.broadcast(f"No {rank} card available.")
            return

        if modifier == MODIFIER_SCRAP:
            removed = self._extract_last_drawn_card(opponent)
            if removed:
                self._return_card_to_top_of_deck(removed)
                self.broadcast(f"{opponent.name}'s last face-up card is returned to top of deck.")
            else:
                self.broadcast("No face-up card to remove.")
            return

        if modifier == MODIFIER_RECYCLE:
            removed = self._extract_last_drawn_card(opponent)
            if removed:
                self._return_card_to_top_of_deck(removed)
                self.broadcast(f"{opponent.name}'s last face-up card returns to top of deck.")
            else:
                self.broadcast("No face-up card to return.")
            return

        if modifier == MODIFIER_SWAP_DRAW:
            first = self._extract_last_drawn_card(player)
            second = self._extract_last_drawn_card(opponent)

            new_self = self._draw_card()
            new_opp = self._draw_card()
            if new_self:
                self._add_card_to_hand(
                    player,
                    new_self,
                    announce_source=f"{player.name} draws",
                    reveal_to_others=True,
                )
                player.stand_pending = False
            if new_opp:
                self._add_card_to_hand(
                    opponent,
                    new_opp,
                    announce_source=f"{opponent.name} draws",
                    reveal_to_others=True,
                )
                opponent.stand_pending = False
            returned_cards: list[Card] = []
            if first:
                returned_cards.append(first)
            if second:
                returned_cards.append(second)
            self._return_cards_to_top_of_deck(returned_cards)
            self.broadcast("Exchange resolves for both players.")
            return

        if modifier == MODIFIER_REDRAFT:
            self._discard_random_modifiers(player, 2)
            self._give_random_modifiers(player, 3, announce=True)
            return

        if modifier == MODIFIER_REDRAFT_PLUS:
            self._discard_random_modifiers(player, 1)
            self._give_random_modifiers(player, 4, announce=True)
            return

        if modifier in TABLE_EFFECT_MODIFIERS:
            self._place_table_effect(player, modifier)
            if modifier in TARGET_VALUE_MODIFIERS:
                self.broadcast(f"Target changes to {self._current_target()}.")
            return

        if modifier == MODIFIER_BREAK:
            removed = self._pop_last_table_effect(opponent)
            if removed:
                self.broadcast(f"{player.name} destroys {MODIFIER_LABELS.get(removed, removed)}.")
            else:
                self.broadcast("No table effect to destroy.")
            return

        if modifier == MODIFIER_BREAK_PLUS:
            if opponent.table_modifiers:
                count = len(opponent.table_modifiers)
                opponent.table_modifiers.clear()
                self.broadcast(f"{player.name} destroys all opponent table effects ({count}).")
            else:
                self.broadcast("No table effects to destroy.")
            return

        if modifier == MODIFIER_LOCKDOWN:
            if opponent.table_modifiers:
                opponent.table_modifiers.clear()
                self.broadcast(f"{player.name} clears opponent table effects.")
            self._place_table_effect(player, modifier)
            return

        if modifier == MODIFIER_PRECISION_DRAW:
            card = self._draw_best_possible_card(player)
            if card:
                self._add_card_to_hand(
                    player,
                    card,
                    announce_source=f"{player.name} precision draws",
                    reveal_to_others=True,
                )
                player.stand_pending = False
            else:
                self.broadcast("Precision Draw found no card.")
            return

        if modifier == MODIFIER_PRECISION_DRAW_PLUS:
            self._place_table_effect(player, modifier)
            card = self._draw_best_possible_card(player)
            if card:
                self._add_card_to_hand(
                    player,
                    card,
                    announce_source=f"{player.name} precision draws",
                    reveal_to_others=True,
                )
                player.stand_pending = False
            else:
                self.broadcast("Precision Draw+ found no card.")
            return

        if modifier == MODIFIER_PRIME_DRAW:
            card = self._draw_best_possible_card(player)
            if card:
                self._add_card_to_hand(
                    player,
                    card,
                    announce_source=f"{player.name} prime draws",
                    reveal_to_others=True,
                )
                player.stand_pending = False
            self._give_random_modifiers(player, 2, announce=True)
            return

        if modifier in TARGET_VALUE_MODIFIERS:
            self._place_table_effect(player, modifier)
            self.broadcast(f"Target changes to {self._current_target()}.")
            return

        if modifier == MODIFIER_SALVAGE:
            self._place_table_effect(player, modifier)
            return

        if modifier == MODIFIER_AID_RIVAL:
            card = self._draw_best_possible_card(opponent)
            if card:
                self._add_card_to_hand(
                    opponent,
                    card,
                    announce_source=f"{opponent.name} draws from Aid Rival",
                    reveal_to_others=True,
                )
                opponent.stand_pending = False
            else:
                self.broadcast("Aid Rival found no card.")

    def _alive_players(self) -> list[TwentyOnePlayer]:
        return [
            p for p in self.get_active_players()
            if isinstance(p, TwentyOnePlayer) and p.hp > 0
        ]

    def _opponent_of(self, player: TwentyOnePlayer) -> TwentyOnePlayer | None:
        for other in self._alive_players():
            if other.id != player.id:
                return other
        return None

    def _both_players_standing(self) -> bool:
        players = self._alive_players()
        if len(players) < 2:
            return False
        return all(p.stand_pending for p in players)

    def _clear_pending_stands(self) -> None:
        players = self._alive_players()
        if not any(p.stand_pending for p in players):
            return
        for p in players:
            p.stand_pending = False

    def _hand_total(self, player: TwentyOnePlayer) -> int:
        return sum(card.rank for card in player.hand)

    @staticmethod
    def _opponent_visible_cards(player: TwentyOnePlayer) -> list[Card]:
        if len(player.hand) <= 1:
            return []
        return player.hand[1:]

    def _current_target(self) -> int:
        for player in self._alive_players():
            for modifier in reversed(player.table_modifiers):
                if modifier in TARGET_VALUE_MODIFIERS:
                    return TARGET_VALUE_MODIFIERS[modifier]
        return 21

    def _current_bet(self, player: TwentyOnePlayer) -> int:
        base = max(0, self.options.base_bet)
        opponent = self._opponent_of(player)
        if not opponent:
            return base

        increase = 0
        for modifier in opponent.table_modifiers:
            if modifier == MODIFIER_RAISE_1:
                increase += 1
            elif modifier == MODIFIER_RAISE_2:
                increase += 2
            elif modifier == MODIFIER_RAISE_2_PLUS:
                increase += 2
            elif modifier == MODIFIER_PRECISION_DRAW_PLUS:
                increase += 5

        reduction = 0
        for modifier in player.table_modifiers:
            if modifier == MODIFIER_GUARD:
                reduction += 1
            elif modifier == MODIFIER_GUARD_PLUS:
                reduction += 2

        return max(0, base + increase - reduction)

    def _modifiers_locked_for(self, player: TwentyOnePlayer) -> bool:
        opponent = self._opponent_of(player)
        if not opponent:
            return False
        return MODIFIER_LOCKDOWN in opponent.table_modifiers

    def _is_single_modifier_playable(self, player: TwentyOnePlayer, modifier: str) -> bool:
        if self._modifiers_locked_for(player):
            return False
        if modifier not in MODIFIER_POOL:
            return False

        if modifier in TABLE_EFFECT_MODIFIERS:
            if modifier in TARGET_VALUE_MODIFIERS:
                return True
            return len(player.table_modifiers) < TABLE_EFFECT_LIMIT

        opponent = self._opponent_of(player)
        if not opponent:
            return False

        if modifier in (MODIFIER_SCRAP, MODIFIER_RECYCLE):
            return self._peek_last_drawn_card(opponent) is not None
        if modifier == MODIFIER_BREAK:
            return bool(opponent.table_modifiers)
        if modifier == MODIFIER_BREAK_PLUS:
            return bool(opponent.table_modifiers)
        return True

    def _place_table_effect(self, player: TwentyOnePlayer, modifier: str) -> None:
        if modifier in TARGET_VALUE_MODIFIERS:
            for p in self._alive_players():
                p.table_modifiers = [t for t in p.table_modifiers if t not in TARGET_VALUE_MODIFIERS]

        player.table_modifiers.append(modifier)
        while len(player.table_modifiers) > TABLE_EFFECT_LIMIT:
            removed = player.table_modifiers.pop(0)
            self.broadcast(f"{player.name}'s {MODIFIER_LABELS.get(removed, removed)} expires.")

    @staticmethod
    def _pop_last_table_effect(player: TwentyOnePlayer) -> str | None:
        if not player.table_modifiers:
            return None
        return player.table_modifiers.pop()

    def _trigger_harvest_rewards(self) -> None:
        for player in self._alive_players():
            if MODIFIER_SALVAGE in player.table_modifiers:
                self._give_random_modifiers(player, 1, announce=True)

    def _build_round_deck(self) -> None:
        cards: list[Card] = []
        card_id = self.round_number * 1000
        deck_count = max(1, self.options.deck_count)
        for _ in range(deck_count):
            for rank in range(1, 12):
                cards.append(Card(id=card_id, rank=rank, suit=0))
                card_id += 1
        self.deck = Deck(cards=cards)
        self.deck.shuffle()

    def _draw_card(self) -> Card | None:
        if not self.deck:
            return None
        if self.deck.is_empty():
            return None
        return self.deck.draw_one()

    def _draw_specific_rank(self, rank: int) -> Card | None:
        if not self.deck:
            return None
        if self.deck.is_empty():
            return None

        for index, card in enumerate(self.deck.cards):
            if card.rank == rank:
                return self.deck.cards.pop(index)
        return None

    def _draw_best_possible_card(self, player: TwentyOnePlayer) -> Card | None:
        if not self.deck:
            return None
        if not self.deck or self.deck.is_empty():
            return None

        target = self._current_target()
        current = self._hand_total(player)
        best_index = -1
        best_value = -1
        fallback_index = 0
        fallback_value = 999
        for index, card in enumerate(self.deck.cards):
            value = card.rank
            projected = current + value
            if projected <= target and value > best_value:
                best_value = value
                best_index = index
            diff = abs(projected - target)
            if diff < fallback_value:
                fallback_value = diff
                fallback_index = index
        chosen_index = best_index if best_index >= 0 else fallback_index
        return self.deck.cards.pop(chosen_index)

    def _add_card_to_hand(
        self,
        player: TwentyOnePlayer,
        card: Card,
        *,
        announce_source: str | None,
        reveal_to_others: bool = True,
    ) -> None:
        player.hand.append(card)
        player.last_drawn_card_id = card.id if reveal_to_others else None
        if announce_source:
            if reveal_to_others:
                self.broadcast(f"{announce_source} {card_name(card, 'en')} ({card.rank}).")
            else:
                self._speak_private(player, f"You receive a hidden card ({card.rank}).")
                self.broadcast(f"{player.name} receives a hidden card.", exclude=player)

    def _speak_private(self, player: TwentyOnePlayer, text: str) -> None:
        if hasattr(self, "record_transcript_event"):
            self.record_transcript_event(player, text, "table")
        user = self.get_user(player)
        if user:
            user.speak(text, "table")

    def _return_card_to_top_of_deck(self, card: Card) -> None:
        if not self.deck:
            self.deck = Deck(cards=[card])
            return
        self.deck.add_top([card])

    def _return_cards_to_top_of_deck(self, cards: list[Card]) -> None:
        if not cards:
            return
        if not self.deck:
            self.deck = Deck(cards=list(cards))
            return
        self.deck.add_top(cards)

    def _peek_last_drawn_card(self, player: TwentyOnePlayer) -> Card | None:
        if player.last_drawn_card_id is None:
            return None
        for card in player.hand:
            if card.id == player.last_drawn_card_id:
                return card
        return None

    def _extract_last_drawn_card(self, player: TwentyOnePlayer) -> Card | None:
        card = self._peek_last_drawn_card(player)
        if not card:
            return None
        for index, hand_card in enumerate(player.hand):
            if hand_card.id == card.id:
                removed = player.hand.pop(index)
                player.last_drawn_card_id = None
                return removed
        return None

    def _give_random_modifiers(self, player: TwentyOnePlayer, count: int, *, announce: bool) -> None:
        for _ in range(max(0, count)):
            modifier = random.choice(MODIFIER_POOL)  # nosec B311
            player.modifiers.append(modifier)
            if announce:
                self._speak_private(player, f"You gain modifier {MODIFIER_LABELS.get(modifier, modifier)}.")
                self.broadcast(f"{player.name} gains a modifier card.", exclude=player)

    @staticmethod
    def _discard_random_modifiers(player: TwentyOnePlayer, count: int) -> None:
        for _ in range(min(max(0, count), len(player.modifiers))):
            index = random.randrange(len(player.modifiers))  # nosec B311
            player.modifiers.pop(index)

    def _sync_hp_scores(self) -> None:
        for team in self._team_manager.teams:
            team.total_score = 0
        for player in self.players:
            if not isinstance(player, TwentyOnePlayer) or player.is_spectator:
                continue
            team = self._team_manager.get_team(player.name)
            if team:
                team.total_score = player.hp

    def build_game_result(self) -> GameResult:
        players = [
            p for p in self.players
            if isinstance(p, TwentyOnePlayer) and not p.is_spectator
        ]
        winner = max(players, key=lambda p: p.hp, default=None)
        final_hp = {p.name: p.hp for p in players}

        return GameResult(
            game_type=self.get_type(),
            timestamp=datetime.now().isoformat(),
            duration_ticks=self.sound_scheduler_tick,
            player_results=[
                PlayerResult(
                    player_id=p.id,
                    player_name=p.name,
                    is_bot=p.is_bot,
                    is_virtual_bot=getattr(p, "is_virtual_bot", False),
                )
                for p in players
            ],
            custom_data={
                "winner_name": winner.name if winner else None,
                "winner_hp": winner.hp if winner else 0,
                "final_hp": final_hp,
                "rounds_played": self.round_number,
            },
        )

    def format_end_screen(self, result: GameResult, locale: str) -> list[str]:
        lines = [Localization.get(locale, "game-final-scores")]
        final_hp = result.custom_data.get("final_hp", {})
        sorted_hp = sorted(final_hp.items(), key=lambda item: item[1], reverse=True)
        for index, (name, hp) in enumerate(sorted_hp, 1):
            lines.append(f"{index}. {name}: {hp} HP")
        return lines
