"""
Age of Heroes Game Implementation for PlayPalace v11.

A civilization-building card game where tribes compete to build an empire of
five cities, complete their monument of culture, or be the last tribe standing.
"""

from dataclasses import dataclass, field
from datetime import datetime
import random

from mashumaro.mixins.json import DataClassJSONMixin

from ..base import Game, Player, GameOptions
from ..registry import register_game
from ...game_utils.actions import Action, ActionSet, MenuInput, Visibility
from ...game_utils.bot_helper import BotHelper
from ...game_utils.game_result import GameResult, PlayerResult
from ...game_utils.options import IntOption, BoolOption, option_field
from ...messages.localization import Localization
from ...ui.keybinds import KeybindState

from .cards import (
    Card,
    Deck,
    CardType,
    ResourceType,
    SpecialResourceType,
    EventType,
    MANDATORY_EVENTS,
    DISASTER_EVENTS,
    get_card_name,
    read_cards,
)
from .state import (
    Tribe,
    TribeState,
    WarState,
    TradeOffer,
    GamePhase,
    PlaySubPhase,
    ActionType,
    WarGoal,
    BuildingType,
    BUILDING_COSTS,
    TRIBE_SPECIAL_RESOURCE,
    DEFAULT_ARMY_SUPPLY,
    DEFAULT_CITY_SUPPLY,
    DEFAULT_FORTRESS_SUPPLY,
    DEFAULT_GENERAL_SUPPLY,
    DEFAULT_ROAD_SUPPLY,
    get_tribe_name,
    get_building_name,
    get_action_name,
    get_war_goal_name,
)
from .construction import (
    can_build,
    get_affordable_buildings,
    build,
    get_road_targets,
    build_road,
)
from .trading import (
    create_offer,
    cancel_offer,
    execute_trade,
    stop_trading,
    is_trading_complete,
    get_player_offers,
    get_matching_offers,
    can_accept_offer,
)
from .combat import (
    can_declare_war,
    get_valid_war_targets,
    get_valid_war_goals,
    declare_war,
    prepare_forces,
    resolve_battle_round,
    is_battle_over,
    get_battle_winner,
    apply_war_outcome,
)
from . import bot as bot_ai


# Hand size limit
MAX_HAND_SIZE = 5

# Trading timeout (30 seconds at ~20 ticks/second)
TRADING_TIMEOUT_TICKS = 600


@dataclass
class AgeOfHeroesPlayer(Player):
    """Player state for Age of Heroes."""

    hand: list[Card] = field(default_factory=list)
    tribe_state: TribeState | None = None

    # Setup phase
    dice_roll: int = 0  # Result of dice roll for turn order

    # Current turn state
    current_action: str | None = None  # ActionType being performed
    pending_discard: int = 0  # Cards that must be discarded

    # Trading state
    has_stopped_trading: bool = False  # Left the auction
    trading_ticks_waited: int = 0  # Ticks spent waiting for trades
    has_made_offers: bool = False  # Whether bot has made offers this phase


@dataclass
class AgeOfHeroesOptions(GameOptions):
    """Options for Age of Heroes game."""

    victory_cities: int = option_field(
        IntOption(
            default=5,
            min_val=3,
            max_val=7,
            value_key="cities",
            label="ageofheroes-set-victory-cities",
            prompt="ageofheroes-enter-victory-cities",
            change_msg="ageofheroes-option-changed-victory-cities",
        )
    )
    neighbor_roads_only: bool = option_field(
        BoolOption(
            default=True,
            value_key="enabled",
            label="ageofheroes-toggle-neighbor-roads",
            change_msg="ageofheroes-option-changed-neighbor-roads",
        )
    )


@dataclass
@register_game
class AgeOfHeroesGame(Game):
    """
    Age of Heroes - A civilization-building card game.

    Players lead tribes competing to achieve victory through:
    - Building 5 cities (Empire of Five Cities)
    - Completing their monument with 5 special resources (Carriers of Great Culture)
    - Being the last tribe standing (The Most Persistent)
    """

    players: list[AgeOfHeroesPlayer] = field(default_factory=list)
    options: AgeOfHeroesOptions = field(default_factory=AgeOfHeroesOptions)

    # Game state
    deck: Deck = field(default_factory=Deck)
    discard_pile: list[Card] = field(default_factory=list)

    # Phase tracking
    phase: str = GamePhase.SETUP
    sub_phase: str = ""
    current_day: int = 0  # Round counter

    # Supply tracking (shared pool)
    army_supply: int = DEFAULT_ARMY_SUPPLY
    city_supply: int = DEFAULT_CITY_SUPPLY
    fortress_supply: int = DEFAULT_FORTRESS_SUPPLY
    general_supply: int = DEFAULT_GENERAL_SUPPLY
    road_supply: int = DEFAULT_ROAD_SUPPLY

    # Setup phase - track who has rolled
    setup_rolls: dict[str, int] = field(default_factory=dict)  # player_id -> dice total

    # War state
    war_state: WarState = field(default_factory=WarState)

    # Trading state
    trade_offers: list[TradeOffer] = field(default_factory=list)

    # Road building - pending request
    road_request_from: int = -1  # Player index requesting road
    road_request_to: int = -1  # Player index being asked

    @classmethod
    def get_name(cls) -> str:
        return "Age of Heroes"

    @classmethod
    def get_type(cls) -> str:
        return "ageofheroes"

    @classmethod
    def get_category(cls) -> str:
        return "category-card-games"

    @classmethod
    def get_min_players(cls) -> int:
        return 2

    @classmethod
    def get_max_players(cls) -> int:
        return 6

    def create_player(
        self, player_id: str, name: str, is_bot: bool = False
    ) -> AgeOfHeroesPlayer:
        """Create a new player with Age of Heroes-specific state."""
        return AgeOfHeroesPlayer(id=player_id, name=name, is_bot=is_bot)

    # ==========================================================================
    # Action Sets
    # ==========================================================================

    def create_turn_action_set(self, player: AgeOfHeroesPlayer) -> ActionSet:
        """Create the turn action set for a player."""
        action_set = ActionSet(name="turn")

        # Setup phase - dice roll
        action_set.add(
            Action(
                id="roll_dice",
                label="Roll dice",
                handler="_action_roll_dice",
                is_enabled="_is_roll_dice_enabled",
                is_hidden="_is_roll_dice_hidden",
                get_label="_get_roll_dice_label",
            )
        )

        # Continue button (used in various phases)
        action_set.add(
            Action(
                id="continue",
                label="Continue",
                handler="_action_continue",
                is_enabled="_is_continue_enabled",
                is_hidden="_is_continue_hidden",
            )
        )

        # Main play actions
        for action_type in ActionType:
            action_set.add(
                Action(
                    id=f"action_{action_type.value}",
                    label="",
                    handler="_action_select_main_action",
                    is_enabled="_is_main_action_enabled",
                    is_hidden="_is_main_action_hidden",
                    get_label="_get_main_action_label",
                )
            )

        # Trading actions
        action_set.add(
            Action(
                id="stop_trading",
                label="Stop Trading",
                handler="_action_stop_trading",
                is_enabled="_is_trading_enabled",
                is_hidden="_is_trading_hidden",
                get_label="_get_stop_trading_label",
            )
        )

        # Status actions (keybind only)
        action_set.add(
            Action(
                id="check_status",
                label="Check status",
                handler="_action_check_status",
                is_enabled="_is_status_enabled",
                is_hidden="_is_always_hidden",
            )
        )
        action_set.add(
            Action(
                id="check_status_detailed",
                label="Detailed status",
                handler="_action_check_status_detailed",
                is_enabled="_is_status_enabled",
                is_hidden="_is_always_hidden",
            )
        )

        return action_set

    def setup_keybinds(self) -> None:
        """Define all keybinds for the game."""
        super().setup_keybinds()

        # Remove base class 's' and 'shift+s' keybinds before adding ours
        if "s" in self._keybinds:
            self._keybinds["s"] = []
        if "shift+s" in self._keybinds:
            self._keybinds["shift+s"] = []

        # Status keybinds
        self.define_keybind(
            "s",
            "Check status",
            ["check_status"],
            state=KeybindState.ACTIVE,
            include_spectators=True,
        )
        self.define_keybind(
            "shift+s",
            "Detailed status",
            ["check_status_detailed"],
            state=KeybindState.ACTIVE,
            include_spectators=True,
        )

    # ==========================================================================
    # Action Callbacks - Visibility/Enabled
    # ==========================================================================

    def _is_always_hidden(self, player: Player) -> Visibility:
        """Always hidden (keybind only)."""
        return Visibility.HIDDEN

    def _is_status_enabled(self, player: Player) -> str | None:
        """Status is enabled once game starts."""
        if self.status != "playing":
            return "ageofheroes-game-not-started"
        return None

    def _is_roll_dice_enabled(self, player: Player) -> str | None:
        """Roll dice is enabled in setup phase for players who haven't rolled."""
        if self.status != "playing":
            return "ageofheroes-game-not-started"
        if self.phase != GamePhase.SETUP:
            return "ageofheroes-wrong-phase"
        if player.id in self.setup_rolls:
            return "ageofheroes-already-rolled"
        return None

    def _is_roll_dice_hidden(self, player: Player) -> Visibility:
        """Roll dice is visible only in setup phase."""
        if self.phase != GamePhase.SETUP:
            return Visibility.HIDDEN
        if player.id in self.setup_rolls:
            return Visibility.HIDDEN
        return Visibility.VISIBLE

    def _get_roll_dice_label(self, player: Player, action_id: str) -> str:
        """Get label for roll dice action."""
        user = self.get_user(player)
        locale = user.locale if user else "en"
        return Localization.get(locale, "ageofheroes-roll-dice")

    def _is_continue_enabled(self, player: Player) -> str | None:
        """Continue is enabled at phase transitions."""
        if self.status != "playing":
            return "ageofheroes-game-not-started"
        return None

    def _is_continue_hidden(self, player: Player) -> Visibility:
        """Continue is usually hidden."""
        return Visibility.HIDDEN

    def _is_main_action_enabled(self, player: Player) -> str | None:
        """Main actions are enabled during play phase action selection."""
        if self.status != "playing":
            return "ageofheroes-game-not-started"
        if self.phase != GamePhase.PLAY:
            return "ageofheroes-wrong-phase"
        if self.sub_phase != PlaySubPhase.SELECT_ACTION:
            return "ageofheroes-wrong-phase"
        if self.current_player != player:
            return "ageofheroes-not-your-turn"
        return None

    def _is_main_action_hidden(self, player: Player) -> Visibility:
        """Main actions are visible during action selection."""
        if self.phase != GamePhase.PLAY:
            return Visibility.HIDDEN
        if self.sub_phase != PlaySubPhase.SELECT_ACTION:
            return Visibility.HIDDEN
        if self.current_player != player:
            return Visibility.HIDDEN
        return Visibility.VISIBLE

    def _get_main_action_label(self, player: Player, action_id: str) -> str:
        """Get label for main action."""
        user = self.get_user(player)
        locale = user.locale if user else "en"
        # Extract action type from action_id (e.g., "action_tax_collection" -> "tax_collection")
        action_type = action_id.replace("action_", "")
        return get_action_name(action_type, locale)

    def _is_trading_enabled(self, player: Player) -> str | None:
        """Trading is enabled during fair phase."""
        if self.status != "playing":
            return "ageofheroes-game-not-started"
        if self.phase != GamePhase.FAIR:
            return "ageofheroes-wrong-phase"
        if not isinstance(player, AgeOfHeroesPlayer):
            return "Invalid player"
        if player.has_stopped_trading:
            return "ageofheroes-left-auction"
        return None

    def _is_trading_hidden(self, player: Player) -> Visibility:
        """Trading actions visible during fair phase."""
        if self.phase != GamePhase.FAIR:
            return Visibility.HIDDEN
        if isinstance(player, AgeOfHeroesPlayer) and player.has_stopped_trading:
            return Visibility.HIDDEN
        return Visibility.VISIBLE

    def _get_stop_trading_label(self, player: Player, action_id: str) -> str:
        """Get label for stop trading action."""
        user = self.get_user(player)
        locale = user.locale if user else "en"
        return Localization.get(locale, "ageofheroes-stop-trading")

    # ==========================================================================
    # Action Handlers
    # ==========================================================================

    def _action_roll_dice(self, player: Player, action_id: str) -> None:
        """Handle dice roll for turn order in setup phase."""
        if not isinstance(player, AgeOfHeroesPlayer):
            return

        # Roll two dice
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total = die1 + die2
        player.dice_roll = total
        self.setup_rolls[player.id] = total

        # Play dice sound
        self.play_sound("game_pig/dice.ogg")

        # Announce result
        user = self.get_user(player)
        if user:
            user.speak_l("ageofheroes-dice-result", total=total, die1=die1, die2=die2)

        # Announce to others
        for p in self.players:
            if p != player:
                other_user = self.get_user(p)
                if other_user:
                    other_user.speak_l(
                        "ageofheroes-dice-result-other", player=player.name, total=total
                    )

        # Check if all players have rolled
        if len(self.setup_rolls) == len(self.get_active_players()):
            self._resolve_setup_rolls()

        self.rebuild_all_menus()

    def _resolve_setup_rolls(self) -> None:
        """Resolve setup dice rolls and determine turn order."""
        active_players = self.get_active_players()

        # Find highest roll
        max_roll = max(self.setup_rolls.values())
        winners = [p for p in active_players if self.setup_rolls.get(p.id, 0) == max_roll]

        if len(winners) > 1:
            # Tie - need to reroll
            self.broadcast_l("ageofheroes-dice-tie", total=max_roll)
            # Clear rolls for tied players
            for p in winners:
                del self.setup_rolls[p.id]
                p.dice_roll = 0
            # Jolt bots to reroll
            for p in winners:
                if p.is_bot:
                    BotHelper.jolt_bot(p, ticks=random.randint(20, 30))
        else:
            # We have a winner - they go first
            first_player = winners[0]

            # Announce
            for p in self.players:
                user = self.get_user(p)
                if user:
                    if p == first_player:
                        user.speak_l("ageofheroes-first-player-you", total=max_roll)
                    else:
                        user.speak_l(
                            "ageofheroes-first-player",
                            player=first_player.name,
                            total=max_roll,
                        )

            # Set turn order starting with winner
            self.set_turn_players(active_players)
            first_index = active_players.index(first_player)
            self.turn_index = first_index

            # Deal initial hands (5 cards each)
            self._deal_initial_hands()

            # Move to prepare phase
            self._start_prepare_phase()

    def _action_continue(self, player: Player, action_id: str) -> None:
        """Handle continue button press."""
        # Used for phase transitions when player acknowledgment is needed
        pass

    def _action_select_main_action(self, player: Player, action_id: str) -> None:
        """Handle main action selection in play phase."""
        if not isinstance(player, AgeOfHeroesPlayer):
            return

        # Extract action type from action_id
        action_type = action_id.replace("action_", "")
        player.current_action = action_type

        if action_type == ActionType.TAX_COLLECTION:
            self._perform_tax_collection(player)
        elif action_type == ActionType.CONSTRUCTION:
            self._start_construction(player)
        elif action_type == ActionType.WAR:
            self._start_war_declaration(player)
        elif action_type == ActionType.DO_NOTHING:
            self._perform_do_nothing(player)

    def _action_check_status(self, player: Player, action_id: str) -> None:
        """Show basic status for all players."""
        user = self.get_user(player)
        if not user:
            return

        locale = user.locale
        for p in self.get_active_players():
            if not isinstance(p, AgeOfHeroesPlayer) or not p.tribe_state:
                continue

            ts = p.tribe_state
            tribe_name = get_tribe_name(ts.tribe, locale)
            user.speak_l(
                "ageofheroes-status",
                player=p.name,
                tribe=tribe_name,
                cities=ts.cities,
                armies=ts.get_available_armies(),
                monument=ts.monument_progress,
            )

    def _action_check_status_detailed(self, player: Player, action_id: str) -> None:
        """Show detailed status in a status box."""
        user = self.get_user(player)
        if not user:
            return

        locale = user.locale
        lines = []

        for p in self.get_active_players():
            if not isinstance(p, AgeOfHeroesPlayer) or not p.tribe_state:
                continue

            ts = p.tribe_state
            tribe_name = get_tribe_name(ts.tribe, locale)

            # Build road string
            road_parts = []
            if ts.road_left:
                road_parts.append(Localization.get(locale, "ageofheroes-status-road-left"))
            if ts.road_right:
                road_parts.append(Localization.get(locale, "ageofheroes-status-road-right"))
            road_str = (
                ", ".join(road_parts)
                if road_parts
                else Localization.get(locale, "ageofheroes-status-none")
            )

            # Build status line
            line = f"{p.name} ({tribe_name}): "
            line += f"{ts.cities} cities, "
            line += f"{ts.get_available_armies()} armies, "
            line += f"{ts.generals} generals, "
            line += f"{ts.fortresses} fortresses, "
            line += f"{ts.monument_progress}/5 monument, "
            line += f"Roads: {road_str}"

            if ts.earthquaked_armies > 0:
                line += f", {ts.earthquaked_armies} recovering"
            if ts.returning_armies > 0:
                line += f", {ts.returning_armies} returning"

            lines.append(line)

        self.status_box(player, lines)

    # ==========================================================================
    # Game Flow
    # ==========================================================================

    def on_start(self) -> None:
        """Called when the game starts."""
        self.status = "playing"
        self.game_active = True

        # Assign tribes to players
        self._assign_tribes()

        # Build deck based on player count
        self.deck.build_standard_deck(len(self.get_active_players()))
        self.deck.shuffle()

        # Initialize supply based on player count
        self._initialize_supply()

        # Start setup phase
        self.phase = GamePhase.SETUP
        self.setup_rolls = {}

        # Tell players their tribes
        for player in self.get_active_players():
            if not isinstance(player, AgeOfHeroesPlayer) or not player.tribe_state:
                continue

            user = self.get_user(player)
            if user:
                locale = user.locale
                tribe_name = get_tribe_name(player.tribe_state.tribe, locale)
                special = player.tribe_state.get_special_resource()
                special_name = get_card_name(
                    Card(id=-1, card_type=CardType.SPECIAL, subtype=special), locale
                )
                user.speak_l(
                    "ageofheroes-setup-start", tribe=tribe_name, special=special_name
                )

        # Play music
        self.play_music("game_ageofheroes/music.ogg")

        # Jolt bots to roll dice
        for p in self.get_active_players():
            if p.is_bot:
                BotHelper.jolt_bot(p, ticks=random.randint(20, 40))

        self.rebuild_all_menus()

    def _assign_tribes(self) -> None:
        """Assign tribes to players."""
        active_players = self.get_active_players()
        tribes = list(Tribe)[: len(active_players)]
        random.shuffle(tribes)

        for i, player in enumerate(active_players):
            if isinstance(player, AgeOfHeroesPlayer):
                player.tribe_state = TribeState(tribe=tribes[i])

    def _initialize_supply(self) -> None:
        """Initialize building supply based on player count."""
        # Standard supply works for 2-6 players
        self.army_supply = DEFAULT_ARMY_SUPPLY
        self.city_supply = DEFAULT_CITY_SUPPLY
        self.fortress_supply = DEFAULT_FORTRESS_SUPPLY
        self.general_supply = DEFAULT_GENERAL_SUPPLY
        self.road_supply = DEFAULT_ROAD_SUPPLY

    def _deal_initial_hands(self) -> None:
        """Deal initial hands to all players."""
        for player in self.get_active_players():
            if isinstance(player, AgeOfHeroesPlayer):
                player.hand = self._draw_cards(MAX_HAND_SIZE)
                # Tell player their cards
                user = self.get_user(player)
                if user:
                    cards_str = read_cards(player.hand, user.locale)
                    user.speak(f"Your cards: {cards_str}")

    def _draw_cards(self, count: int) -> list[Card]:
        """Draw cards from deck, reshuffling discard pile if needed."""
        drawn = []
        for _ in range(count):
            card = self._draw_one()
            if card:
                drawn.append(card)
        return drawn

    def _draw_one(self) -> Card | None:
        """Draw a single card, reshuffling discard pile if needed."""
        if self.deck.is_empty() and self.discard_pile:
            # Reshuffle discard pile into deck
            self.deck.add_all(self.discard_pile)
            self.discard_pile = []
            self.deck.shuffle()
            self.broadcast_l("ageofheroes-deck-reshuffled")
        return self.deck.draw_one()

    def _start_prepare_phase(self) -> None:
        """Start the preparation phase."""
        self.phase = GamePhase.PREPARE
        self.broadcast_l("ageofheroes-prepare-start")

        # Process mandatory events for all players
        self._process_prepare_phase()

    def _process_prepare_phase(self) -> None:
        """Process the preparation phase - play events and discard disasters."""
        # For simplicity, auto-process events in order
        # Population Growth -> apply immediately
        # Disasters -> discard
        for player in self.get_active_players():
            if not isinstance(player, AgeOfHeroesPlayer):
                continue

            self._process_player_events(player)

        # After all events processed, move to fair phase
        self._start_fair_phase()

    def _process_player_events(self, player: AgeOfHeroesPlayer) -> None:
        """Process mandatory events for a player."""
        if not player.tribe_state:
            return

        # Find and process mandatory events
        cards_to_remove = []
        for i, card in enumerate(player.hand):
            if not card.is_mandatory_event():
                continue

            if card.subtype == EventType.POPULATION_GROWTH:
                # Build a free city
                if self.city_supply > 0:
                    player.tribe_state.cities += 1
                    self.city_supply -= 1
                    self.broadcast_personal_l(
                        player,
                        "ageofheroes-population-growth-you",
                        "ageofheroes-population-growth",
                    )
                    self.play_sound("game_ageofheroes/build.ogg")
                cards_to_remove.append(i)

            elif card.subtype == EventType.EARTHQUAKE:
                # Disable armies
                player.tribe_state.earthquaked_armies = player.tribe_state.armies
                self.broadcast_personal_l(
                    player, "ageofheroes-earthquake-you", "ageofheroes-earthquake"
                )
                self.play_sound("game_ageofheroes/disaster.ogg")
                cards_to_remove.append(i)

            elif card.subtype == EventType.ERUPTION:
                # Lose a city
                if player.tribe_state.cities > 0:
                    player.tribe_state.cities -= 1
                    self.city_supply += 1
                self.broadcast_personal_l(
                    player, "ageofheroes-eruption-you", "ageofheroes-eruption"
                )
                self.play_sound("game_ageofheroes/disaster.ogg")
                cards_to_remove.append(i)

            elif card.subtype in (EventType.HUNGER, EventType.BARBARIANS):
                # Just discard
                user = self.get_user(player)
                if user:
                    card_name = get_card_name(card, user.locale)
                    user.speak_l("ageofheroes-discard-card-you", card=card_name)
                self._broadcast_discard(player, card)
                cards_to_remove.append(i)

        # Remove processed cards (in reverse order to preserve indices)
        for i in reversed(cards_to_remove):
            removed = player.hand.pop(i)
            self.discard_pile.append(removed)

        # Check for elimination
        self._check_elimination(player)

    def _broadcast_discard(self, player: AgeOfHeroesPlayer, card: Card) -> None:
        """Broadcast card discard to other players."""
        for p in self.players:
            if p == player:
                continue
            user = self.get_user(p)
            if user:
                card_name = get_card_name(card, user.locale)
                user.speak_l("ageofheroes-discard-card", player=player.name, card=card_name)

    def _start_fair_phase(self) -> None:
        """Start the fair/trading phase."""
        self.phase = GamePhase.FAIR
        self.trade_offers = []

        # Reset trading state
        for player in self.get_active_players():
            if isinstance(player, AgeOfHeroesPlayer):
                player.has_stopped_trading = False
                player.trading_ticks_waited = 0
                player.has_made_offers = False

        # Players draw cards based on road network
        self._distribute_fair_cards()

        self.broadcast_l("ageofheroes-fair-start")
        self.broadcast_l("ageofheroes-auction-start")

        # Check if trading is already complete (all bots auto-stop)
        self._check_trading_complete()

    def _distribute_fair_cards(self) -> None:
        """Distribute cards based on road networks."""
        for player in self.get_active_players():
            if not isinstance(player, AgeOfHeroesPlayer) or not player.tribe_state:
                continue

            # Count connected tribes via roads
            cards_to_draw = self._count_road_network(player)
            if cards_to_draw > 0:
                drawn = self._draw_cards(cards_to_draw)
                player.hand.extend(drawn)

                user = self.get_user(player)
                if user:
                    user.speak_l("ageofheroes-fair-draw", count=cards_to_draw)

                # Announce to others
                for p in self.players:
                    if p != player:
                        other_user = self.get_user(p)
                        if other_user:
                            other_user.speak_l(
                                "ageofheroes-fair-draw-other",
                                player=player.name,
                                count=cards_to_draw,
                            )

    def _count_road_network(self, player: AgeOfHeroesPlayer) -> int:
        """Count how many tribes are connected via road network."""
        if not player.tribe_state:
            return 1

        active_players = self.get_active_players()
        player_index = active_players.index(player)
        visited = {player_index}
        count = 1

        # Check left connections
        current = player_index
        while True:
            current_player = active_players[current]
            if not isinstance(current_player, AgeOfHeroesPlayer):
                break
            if not current_player.tribe_state:
                break
            if not current_player.tribe_state.road_left:
                break

            # Move to left neighbor (circular)
            left_index = (current - 1) % len(active_players)
            if left_index in visited:
                break
            visited.add(left_index)
            count += 1
            current = left_index

        # Check right connections
        current = player_index
        while True:
            current_player = active_players[current]
            if not isinstance(current_player, AgeOfHeroesPlayer):
                break
            if not current_player.tribe_state:
                break
            if not current_player.tribe_state.road_right:
                break

            # Move to right neighbor (circular)
            right_index = (current + 1) % len(active_players)
            if right_index in visited:
                break
            visited.add(right_index)
            count += 1
            current = right_index

        return count

    def _check_trading_complete(self) -> None:
        """Check if trading phase is complete and advance if so."""
        if self.phase != GamePhase.FAIR:
            return

        # Count active traders
        active_traders = 0
        for player in self.get_active_players():
            if isinstance(player, AgeOfHeroesPlayer):
                if not player.has_stopped_trading:
                    active_traders += 1

        # End trading if all stopped or only one remains
        if active_traders <= 1:
            self._start_play_phase()

    def _action_stop_trading(self, player: Player, action_id: str) -> None:
        """Handle stop trading action."""
        if not isinstance(player, AgeOfHeroesPlayer):
            return

        if self.phase != GamePhase.FAIR:
            return

        if player.has_stopped_trading:
            return

        # Mark player as stopped
        stop_trading(self, player)

        # Announce
        self.broadcast_personal_l(
            player, "ageofheroes-left-auction-you", "ageofheroes-left-auction"
        )

        # Check if trading is complete
        self._check_trading_complete()

    def _bot_do_trading(self, player: AgeOfHeroesPlayer) -> None:
        """Bot performs trading actions during fair phase."""
        if player.has_stopped_trading:
            return

        # First, make offers if we haven't yet
        if not player.has_made_offers:
            self._bot_make_trade_offers(player)
            player.has_made_offers = True
            return

        # Check for matching trades and execute them
        trades_made = self._check_and_execute_trades()

        # If a trade was made, reset the wait timer
        if trades_made:
            player.trading_ticks_waited = 0
            return

        # Increment wait time
        player.trading_ticks_waited += 1

        # Stop trading after timeout
        if player.trading_ticks_waited >= TRADING_TIMEOUT_TICKS:
            self._action_stop_trading(player, "stop_trading")

    def _bot_make_trade_offers(self, player: AgeOfHeroesPlayer) -> None:
        """Bot makes trade offers for cards they want."""
        if not player.tribe_state:
            return

        # What do we want? Our special resource for monument
        wanted_special = TRIBE_SPECIAL_RESOURCE.get(player.tribe_state.tribe)

        # Look through our hand for cards to offer
        for i, card in enumerate(player.hand):
            # Don't offer our own special resource
            if card.card_type == CardType.SPECIAL:
                if card.subtype == wanted_special:
                    continue  # Keep this, we need it!

            # Offer other special resources (we can't use them)
            if card.card_type == CardType.SPECIAL:
                # Offer this for our special resource
                offer = create_offer(
                    self, player, i,
                    wanted_type=CardType.SPECIAL,
                    wanted_subtype=wanted_special,
                )
                if offer:
                    self._announce_offer(player, card, wanted_special)

            # Offer disaster cards for anything useful
            if card.is_disaster():
                # Offer for our special resource
                offer = create_offer(
                    self, player, i,
                    wanted_type=CardType.SPECIAL,
                    wanted_subtype=wanted_special,
                )
                if offer:
                    self._announce_offer(player, card, wanted_special)

    def _announce_offer(
        self, player: AgeOfHeroesPlayer, offered_card: Card, wanted_subtype: str
    ) -> None:
        """Announce a trade offer."""
        for p in self.players:
            user = self.get_user(p)
            if user:
                offered_name = get_card_name(offered_card, user.locale)
                # Get wanted name
                wanted_card = Card(id=-1, card_type=CardType.SPECIAL, subtype=wanted_subtype)
                wanted_name = get_card_name(wanted_card, user.locale)

                if p == player:
                    user.speak_l(
                        "ageofheroes-offer-made-you",
                        card=offered_name,
                        wanted=wanted_name,
                    )
                else:
                    user.speak_l(
                        "ageofheroes-offer-made",
                        player=player.name,
                        card=offered_name,
                        wanted=wanted_name,
                    )

    def _check_and_execute_trades(self) -> bool:
        """Check for matching offers and execute trades. Returns True if any trade made."""
        trades_made = False
        active_players = self.get_active_players()

        # Check all pairs of offers for matches
        i = 0
        while i < len(self.trade_offers):
            offer1 = self.trade_offers[i]
            if offer1.player_index >= len(active_players):
                i += 1
                continue

            player1 = active_players[offer1.player_index]
            if not isinstance(player1, AgeOfHeroesPlayer):
                i += 1
                continue

            if offer1.card_index >= len(player1.hand):
                i += 1
                continue

            card1 = player1.hand[offer1.card_index]

            j = i + 1
            while j < len(self.trade_offers):
                offer2 = self.trade_offers[j]
                if offer2.player_index >= len(active_players):
                    j += 1
                    continue
                if offer2.player_index == offer1.player_index:
                    j += 1
                    continue

                player2 = active_players[offer2.player_index]
                if not isinstance(player2, AgeOfHeroesPlayer):
                    j += 1
                    continue

                if offer2.card_index >= len(player2.hand):
                    j += 1
                    continue

                card2 = player2.hand[offer2.card_index]

                # Check if offers match
                # offer1 wants what player2 offers, and offer2 wants what player1 offers
                match1 = (
                    (offer1.wanted_type is None or offer1.wanted_type == card2.card_type)
                    and (offer1.wanted_subtype is None or offer1.wanted_subtype == card2.subtype)
                )
                match2 = (
                    (offer2.wanted_type is None or offer2.wanted_type == card1.card_type)
                    and (offer2.wanted_subtype is None or offer2.wanted_subtype == card1.subtype)
                )

                if match1 and match2:
                    # Check special resource restrictions
                    # Special resources can only go to the tribe that needs them
                    valid = True
                    if card1.card_type == CardType.SPECIAL:
                        needed_by = None
                        for tribe, special in TRIBE_SPECIAL_RESOURCE.items():
                            if special == card1.subtype:
                                needed_by = tribe
                                break
                        if needed_by and player2.tribe_state:
                            if player2.tribe_state.tribe != needed_by:
                                valid = False

                    if card2.card_type == CardType.SPECIAL:
                        needed_by = None
                        for tribe, special in TRIBE_SPECIAL_RESOURCE.items():
                            if special == card2.subtype:
                                needed_by = tribe
                                break
                        if needed_by and player1.tribe_state:
                            if player1.tribe_state.tribe != needed_by:
                                valid = False

                    if valid:
                        # Execute the trade
                        self._execute_matched_trade(player1, offer1, player2, offer2)
                        trades_made = True
                        # Restart search since indices changed
                        i = 0
                        break

                j += 1
            else:
                i += 1
                continue
            break  # Restart outer loop after trade

        return trades_made

    def _execute_matched_trade(
        self,
        player1: AgeOfHeroesPlayer,
        offer1: TradeOffer,
        player2: AgeOfHeroesPlayer,
        offer2: TradeOffer,
    ) -> None:
        """Execute a matched trade between two players."""
        card1 = player1.hand[offer1.card_index]
        card2 = player2.hand[offer2.card_index]

        # Swap cards
        player1.hand[offer1.card_index] = card2
        player2.hand[offer2.card_index] = card1

        # Remove offers
        if offer1 in self.trade_offers:
            self.trade_offers.remove(offer1)
        if offer2 in self.trade_offers:
            self.trade_offers.remove(offer2)

        # Announce trade
        self.play_sound("game_ageofheroes/trade.ogg")

        for p in self.players:
            user = self.get_user(p)
            if user:
                card1_name = get_card_name(card1, user.locale)
                card2_name = get_card_name(card2, user.locale)

                if p == player1:
                    user.speak_l(
                        "ageofheroes-trade-accepted-you",
                        other=player2.name,
                        receive=card2_name,
                    )
                elif p == player2:
                    user.speak_l(
                        "ageofheroes-trade-accepted-you",
                        other=player1.name,
                        receive=card1_name,
                    )
                else:
                    user.speak_l(
                        "ageofheroes-trade-accepted",
                        player=player1.name,
                        other=player2.name,
                        give=card1_name,
                        receive=card2_name,
                    )

    def _start_play_phase(self) -> None:
        """Start the main play phase."""
        self.phase = GamePhase.PLAY
        self.current_day += 1
        self.broadcast_l("ageofheroes-play-start")
        self.broadcast_l("ageofheroes-day", day=self.current_day)

        self._start_turn()

    def _start_turn(self) -> None:
        """Start a player's turn."""
        player = self.current_player
        if not isinstance(player, AgeOfHeroesPlayer):
            return

        # Process end-of-turn effects from previous turn
        if player.tribe_state:
            armies_back, generals_back, recovered = player.tribe_state.process_end_of_turn()
            if armies_back > 0 or generals_back > 0:
                self.broadcast_personal_l(
                    player, "ageofheroes-army-returned-you", "ageofheroes-army-returned"
                )
            if recovered > 0:
                self.broadcast_personal_l(
                    player, "ageofheroes-army-recover-you", "ageofheroes-army-recover"
                )

        # Draw a card
        self.sub_phase = PlaySubPhase.DRAW_CARD
        drawn = self._draw_one()
        if drawn:
            player.hand.append(drawn)
            user = self.get_user(player)
            if user:
                card_name = get_card_name(drawn, user.locale)
                user.speak_l("ageofheroes-draw-card-you", card=card_name)

            # Announce to others
            for p in self.players:
                if p != player:
                    other_user = self.get_user(p)
                    if other_user:
                        other_user.speak_l("ageofheroes-draw-card", player=player.name)

        # Auto-collect special resources for monument
        self._collect_special_resources(player)

        # Move to action selection
        self.sub_phase = PlaySubPhase.SELECT_ACTION
        self.announce_turn()

        # Tell player their options
        user = self.get_user(player)
        if user:
            user.speak_l("ageofheroes-your-action")

        if player.is_bot:
            BotHelper.jolt_bot(player, ticks=random.randint(30, 50))

        self.rebuild_all_menus()

    def _collect_special_resources(self, player: AgeOfHeroesPlayer) -> None:
        """Auto-collect special resources for monument building."""
        if not player.tribe_state:
            return

        tribe_special = player.tribe_state.get_special_resource()
        cards_to_remove = []

        for i, card in enumerate(player.hand):
            if card.card_type == CardType.SPECIAL and card.subtype == tribe_special:
                if player.tribe_state.monument_progress < 5:
                    player.tribe_state.monument_progress += 1
                    cards_to_remove.append(i)

        # Remove collected cards
        for i in reversed(cards_to_remove):
            removed = player.hand.pop(i)
            self.discard_pile.append(removed)

        # Announce if progress was made
        if cards_to_remove:
            percent = player.tribe_state.monument_progress * 20
            self.broadcast_personal_l(
                player,
                "ageofheroes-monument-progress-you",
                "ageofheroes-monument-progress",
                percent=percent,
                count=player.tribe_state.monument_progress,
            )

            # Check for monument victory
            if player.tribe_state.monument_progress >= 5:
                self._declare_victory(player, "monument")

    def _perform_tax_collection(self, player: AgeOfHeroesPlayer) -> None:
        """Perform tax collection action."""
        if not player.tribe_state:
            return

        cities = player.tribe_state.cities
        if cities == 0:
            # No cities - exchange a card
            user = self.get_user(player)
            if user:
                user.speak_l("ageofheroes-tax-no-city")
            # For now, auto-exchange first card
            if player.hand:
                discarded = player.hand.pop(0)
                self.discard_pile.append(discarded)
                drawn = self._draw_one()
                if drawn:
                    player.hand.append(drawn)
                self.broadcast_personal_l(
                    player,
                    "ageofheroes-tax-no-city-done-you",
                    "ageofheroes-tax-no-city-done",
                )
        else:
            # Draw cards equal to cities
            drawn = self._draw_cards(cities)
            player.hand.extend(drawn)
            self.broadcast_personal_l(
                player,
                "ageofheroes-tax-collection-you",
                "ageofheroes-tax-collection",
                cities=cities,
                cards=len(drawn),
            )

        self._end_action(player)

    def _start_construction(self, player: AgeOfHeroesPlayer) -> None:
        """Start construction action."""
        if not player.tribe_state:
            self._end_action(player)
            return

        affordable = get_affordable_buildings(self, player)
        if not affordable:
            user = self.get_user(player)
            if user:
                user.speak_l("ageofheroes-no-resources")
            self._end_action(player)
            return

        # For bots, auto-select what to build
        if player.is_bot:
            self._bot_perform_construction(player)
        else:
            # TODO: Show construction menu for human players
            # For now, just end the action
            user = self.get_user(player)
            if user:
                user.speak_l("ageofheroes-construction-stopped")
            self._end_action(player)

    def _bot_perform_construction(self, player: AgeOfHeroesPlayer) -> None:
        """Bot performs construction."""
        if not player.tribe_state:
            self._end_action(player)
            return

        # Use bot AI to select what to build
        building_type = bot_ai.bot_select_construction(self, player)
        if not building_type:
            self._end_action(player)
            return

        # Handle road building specially (needs neighbor permission)
        if building_type == BuildingType.ROAD:
            targets = get_road_targets(self, player)
            if targets:
                # Auto-accept road for bots
                target_index, direction = targets[0]
                # Spend resources first
                from .construction import spend_resources, BUILDING_COSTS
                spend_resources(player, BUILDING_COSTS[BuildingType.ROAD], self.discard_pile)
                self.road_supply -= 1
                build_road(self, player, target_index, direction)
            self._end_action(player)
            return

        # Build the selected building
        if build(self, player, building_type):
            # Check for city victory
            if building_type == BuildingType.CITY:
                if player.tribe_state.cities >= self.options.victory_cities:
                    self._declare_victory(player, "cities")
                    return

        self._end_action(player)

    def _start_war_declaration(self, player: AgeOfHeroesPlayer) -> None:
        """Start war declaration."""
        if not player.tribe_state:
            self._end_action(player)
            return

        # Check if player can declare war
        war_error = can_declare_war(self, player)
        if war_error:
            user = self.get_user(player)
            if user:
                user.speak_l(war_error)
            self._end_action(player)
            return

        # For bots, auto-select target and execute war
        if player.is_bot:
            self._bot_perform_war(player)
        else:
            # TODO: Show war menu for human players
            user = self.get_user(player)
            if user:
                user.speak_l("ageofheroes-war-no-army")
            self._end_action(player)

    def _bot_perform_war(self, player: AgeOfHeroesPlayer) -> None:
        """Bot performs war declaration and combat."""
        if not player.tribe_state:
            self._end_action(player)
            return

        # Select target and goal using bot AI
        result = bot_ai.bot_select_war_target(self, player)
        if not result:
            self._end_action(player)
            return

        target_index, goal = result

        # Declare war
        if not declare_war(self, player, target_index, goal):
            self._end_action(player)
            return

        # Get defender
        active_players = self.get_active_players()
        defender = active_players[target_index]
        if not isinstance(defender, AgeOfHeroesPlayer):
            self.war_state.reset()
            self._end_action(player)
            return

        # Prepare attacker forces using bot AI
        att_armies, att_generals, att_heroes, att_hero_generals = bot_ai.bot_select_armies(
            self, player, is_attacking=True
        )
        prepare_forces(self, player, att_armies, att_generals, att_heroes, att_hero_generals)

        # Prepare defender forces (if bot) or auto-prepare
        if defender.is_bot:
            def_armies, def_generals, def_heroes, def_hero_generals = bot_ai.bot_select_armies(
                self, defender, is_attacking=False
            )
            prepare_forces(self, defender, def_armies, def_generals, def_heroes, def_hero_generals)
        else:
            # Auto-prepare defender with all available forces
            if defender.tribe_state:
                def_armies = defender.tribe_state.get_available_armies()
                def_generals = defender.tribe_state.get_available_generals()
                prepare_forces(self, defender, def_armies, def_generals, 0, 0)

        # Run battle rounds until one side is defeated
        max_rounds = 20  # Safety limit
        rounds = 0
        while not is_battle_over(self) and rounds < max_rounds:
            rounds += 1
            resolve_battle_round(self)

        # Apply war outcome
        apply_war_outcome(self)

        # Check for elimination
        self._check_elimination(defender)
        self._check_elimination(player)

        self._end_action(player)

    def _perform_do_nothing(self, player: AgeOfHeroesPlayer) -> None:
        """Perform do nothing action."""
        self.broadcast_personal_l(
            player, "ageofheroes-do-nothing-you", "ageofheroes-do-nothing"
        )
        self._end_action(player)

    def _end_action(self, player: AgeOfHeroesPlayer) -> None:
        """End the current action and check for hand overflow."""
        player.current_action = None

        # Check hand size
        if len(player.hand) > MAX_HAND_SIZE:
            self.sub_phase = PlaySubPhase.DISCARD_EXCESS
            player.pending_discard = len(player.hand) - MAX_HAND_SIZE
            user = self.get_user(player)
            if user:
                user.speak_l(
                    "ageofheroes-discard-excess",
                    max=MAX_HAND_SIZE,
                    count=player.pending_discard,
                )
            # For bots, auto-discard
            if player.is_bot:
                self._bot_discard_excess(player)
            return

        self._end_turn()

    def _bot_discard_excess(self, player: AgeOfHeroesPlayer) -> None:
        """Bot discards excess cards."""
        while len(player.hand) > MAX_HAND_SIZE:
            # Discard least valuable card (simple heuristic)
            worst_index = 0
            player.hand.pop(worst_index)
        player.pending_discard = 0
        self._end_turn()

    def _end_turn(self) -> None:
        """End the current turn and advance to next player."""
        # Check victory conditions
        winner = self._check_victory()
        if winner:
            return

        # Check if day is over (all players had a turn)
        active_players = self.get_active_players()
        next_index = (self.turn_index + 1) % len(active_players)

        if next_index == 0:
            # Start new day
            self._start_new_day()
        else:
            # Continue to next player
            self.advance_turn(announce=False)
            self._start_turn()

    def _start_new_day(self) -> None:
        """Start a new day (round)."""
        # Reset turn index for the new day
        self.turn_index = 0
        # Return to prepare phase for new events
        self._start_prepare_phase()

    def _check_victory(self) -> AgeOfHeroesPlayer | None:
        """Check for victory conditions."""
        active_players = [
            p
            for p in self.get_active_players()
            if isinstance(p, AgeOfHeroesPlayer) and p.tribe_state and not p.tribe_state.is_eliminated()
        ]

        # Last standing
        if len(active_players) == 1:
            self._declare_victory(active_players[0], "last_standing")
            return active_players[0]

        # Check cities and monument for each player
        for player in active_players:
            if not player.tribe_state:
                continue

            # 5 Cities
            if player.tribe_state.cities >= self.options.victory_cities:
                self._declare_victory(player, "cities")
                return player

            # Monument complete
            if player.tribe_state.monument_progress >= 5:
                self._declare_victory(player, "monument")
                return player

        return None

    def _declare_victory(self, player: AgeOfHeroesPlayer, victory_type: str) -> None:
        """Declare a victory."""
        self.phase = GamePhase.GAME_OVER
        self.play_sound("game_pig/win.ogg")

        if victory_type == "cities":
            self.broadcast_personal_l(
                player, "ageofheroes-victory-cities-you", "ageofheroes-victory-cities"
            )
        elif victory_type == "monument":
            self.broadcast_personal_l(
                player, "ageofheroes-victory-monument-you", "ageofheroes-victory-monument"
            )
        elif victory_type == "last_standing":
            self.broadcast_personal_l(
                player,
                "ageofheroes-victory-last-standing-you",
                "ageofheroes-victory-last-standing",
            )

        self.broadcast_l("ageofheroes-game-over")
        self.finish_game()

    def _check_elimination(self, player: AgeOfHeroesPlayer) -> None:
        """Check if a player has been eliminated."""
        if not player.tribe_state:
            return

        if player.tribe_state.is_eliminated() and len(player.hand) == 0:
            player.is_spectator = True
            self.broadcast_personal_l(
                player, "ageofheroes-eliminated-you", "ageofheroes-eliminated"
            )

    # ==========================================================================
    # Bot AI
    # ==========================================================================

    def on_tick(self) -> None:
        """Called every tick."""
        super().on_tick()
        if not self.game_active:
            return

        # During setup phase, all bots who haven't rolled need to act
        if self.phase == GamePhase.SETUP:
            for player in self.get_active_players():
                if not player.is_bot:
                    continue
                if player.id in self.setup_rolls:
                    continue  # Already rolled

                # Count down thinking time
                if player.bot_think_ticks > 0:
                    player.bot_think_ticks -= 1
                    continue

                # Execute pending action
                if player.bot_pending_action:
                    action_id = player.bot_pending_action
                    player.bot_pending_action = None
                    self.execute_action(player, action_id)
                    continue

                # Ask for action
                action_id = self.bot_think(player)
                if action_id:
                    player.bot_pending_action = action_id

        # During fair phase, bots trade and then stop
        elif self.phase == GamePhase.FAIR:
            for player in self.get_active_players():
                if not isinstance(player, AgeOfHeroesPlayer):
                    continue
                if not player.is_bot:
                    continue
                if player.has_stopped_trading:
                    continue

                # Bots stop trading after a short delay
                if player.bot_think_ticks > 0:
                    player.bot_think_ticks -= 1
                    continue

                self._bot_do_trading(player)
        else:
            # Normal turn-based bot handling
            BotHelper.on_tick(self)

    def bot_think(self, player: Player) -> str | None:
        """Bot AI decision making."""
        if not isinstance(player, AgeOfHeroesPlayer):
            return None

        # Setup phase - roll dice
        if self.phase == GamePhase.SETUP:
            if player.id not in self.setup_rolls:
                return "roll_dice"

        # Play phase - select action
        if self.phase == GamePhase.PLAY and self.sub_phase == PlaySubPhase.SELECT_ACTION:
            if self.current_player == player:
                return self._bot_select_action(player)

        return None

    def _bot_select_action(self, player: AgeOfHeroesPlayer) -> str:
        """Bot selects a main action."""
        return bot_ai.bot_select_action(self, player)

    # ==========================================================================
    # Game Result
    # ==========================================================================

    def build_game_result(self) -> GameResult:
        """Build the game result."""
        active_players = self.get_active_players()

        # Find winner
        winner = None
        for p in active_players:
            if isinstance(p, AgeOfHeroesPlayer) and p.tribe_state:
                if (
                    p.tribe_state.cities >= self.options.victory_cities
                    or p.tribe_state.monument_progress >= 5
                ):
                    winner = p
                    break

        # If no winner by cities/monument, last standing
        non_eliminated = [
            p
            for p in active_players
            if isinstance(p, AgeOfHeroesPlayer) and p.tribe_state and not p.tribe_state.is_eliminated()
        ]
        if not winner and len(non_eliminated) == 1:
            winner = non_eliminated[0]

        return GameResult(
            game_type=self.get_type(),
            timestamp=datetime.now().isoformat(),
            duration_ticks=self.sound_scheduler_tick,
            player_results=[
                PlayerResult(
                    player_id=p.id,
                    player_name=p.name,
                    is_bot=p.is_bot,
                )
                for p in active_players
            ],
            custom_data={
                "winner_name": winner.name if winner else None,
                "days_played": self.current_day,
            },
        )

    def format_end_screen(self, result: GameResult, locale: str) -> list[str]:
        """Format the end screen."""
        lines = [Localization.get(locale, "ageofheroes-game-over")]

        winner_name = result.custom_data.get("winner_name")
        if winner_name:
            lines.append(f"Winner: {winner_name}")

        days = result.custom_data.get("days_played", 0)
        lines.append(f"Days: {days}")

        return lines
