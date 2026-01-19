"""Bot AI for Age of Heroes."""

from __future__ import annotations
import random
from typing import TYPE_CHECKING

from .cards import Card, CardType, ResourceType, EventType
from .state import (
    GamePhase,
    PlaySubPhase,
    ActionType,
    BuildingType,
    WarGoal,
    BUILDING_COSTS,
)
from .construction import can_build, get_affordable_buildings, get_road_targets
from .combat import (
    can_declare_war,
    get_valid_war_targets,
    get_valid_war_goals,
    check_olympics_defense,
)

if TYPE_CHECKING:
    from .game import AgeOfHeroesGame, AgeOfHeroesPlayer


def bot_think(game: AgeOfHeroesGame, player: AgeOfHeroesPlayer) -> str | None:
    """Main bot AI decision function. Returns action ID or None."""
    # Setup phase - roll dice
    if game.phase == GamePhase.SETUP:
        if player.id not in game.setup_rolls:
            return "roll_dice"
        return None

    # Play phase decisions
    if game.phase == GamePhase.PLAY:
        return bot_think_play_phase(game, player)

    # Fair phase - trading decisions
    if game.phase == GamePhase.FAIR:
        return bot_think_fair_phase(game, player)

    return None


def bot_think_play_phase(
    game: AgeOfHeroesGame, player: AgeOfHeroesPlayer
) -> str | None:
    """Bot decision making during play phase."""
    if game.current_player != player:
        return None

    if game.sub_phase == PlaySubPhase.SELECT_ACTION:
        return bot_select_action(game, player)

    if game.sub_phase == PlaySubPhase.DISCARD_EXCESS:
        return bot_discard_excess(game, player)

    return None


def bot_select_action(game: AgeOfHeroesGame, player: AgeOfHeroesPlayer) -> str:
    """Bot selects main turn action."""
    if not player.tribe_state:
        return f"action_{ActionType.DO_NOTHING.value}"

    # Priority-based decision making:
    # 1. Build city if close to victory (4 cities) and can afford it
    # 2. Build city if possible (victory path)
    # 3. Collect special resources (monument victory)
    # 4. Build armies if threatened or planning war
    # 5. Attack weak opponents
    # 6. Build other structures
    # 7. Tax collection for cards
    # 8. Do nothing

    cities = player.tribe_state.cities
    armies = player.tribe_state.get_available_armies()
    monument = player.tribe_state.monument_progress

    # Check what we can build
    affordable = get_affordable_buildings(game, player)

    # Victory push - if we have 4 cities and can build another
    if cities == 4 and BuildingType.CITY in affordable:
        return f"action_{ActionType.CONSTRUCTION.value}"

    # Build city if possible (high priority)
    if BuildingType.CITY in affordable and cities < 5:
        # Strongly prefer building cities
        if random.random() < 0.8:  # 80% chance to build
            return f"action_{ActionType.CONSTRUCTION.value}"

    # Monument near completion - collect more cards via tax
    if monument >= 3:
        # Tax collection to get more special resources
        return f"action_{ActionType.TAX_COLLECTION.value}"

    # If we have armies and there's a weak target, consider war
    if armies >= 2:
        war_check = can_declare_war(game, player)
        if war_check is None:
            targets = get_valid_war_targets(game, player)
            for target_idx, target in targets:
                if hasattr(target, "tribe_state") and target.tribe_state:
                    target_armies = target.tribe_state.get_available_armies()
                    # Attack if we have advantage (more armies than target)
                    if armies > target_armies:
                        if random.random() < 0.6:  # 60% chance to attack
                            return f"action_{ActionType.WAR.value}"

    # Build armies if we have few (aim for 3-4 for military strength)
    if armies < 3 and BuildingType.ARMY in affordable:
        if random.random() < 0.7:  # 70% chance to build army when low
            return f"action_{ActionType.CONSTRUCTION.value}"

    # Build other structures
    if affordable and random.random() < 0.4:
        return f"action_{ActionType.CONSTRUCTION.value}"

    # Tax collection for cards
    if cities >= 1:
        return f"action_{ActionType.TAX_COLLECTION.value}"

    # Default to do nothing
    return f"action_{ActionType.DO_NOTHING.value}"


def bot_discard_excess(game: AgeOfHeroesGame, player: AgeOfHeroesPlayer) -> str | None:
    """Bot decides which card to discard when over hand limit."""
    # This would trigger a discard action - for now handled automatically
    # The game.py already handles bot auto-discard
    return None


def bot_think_fair_phase(
    game: AgeOfHeroesGame, player: AgeOfHeroesPlayer
) -> str | None:
    """Bot decision making during fair/trading phase."""
    # For simplicity, bots don't actively trade - they just stop
    if not player.has_stopped_trading:
        return "stop_trading"
    return None


def bot_select_construction(
    game: AgeOfHeroesGame, player: AgeOfHeroesPlayer
) -> str | None:
    """Bot selects what to build."""
    if not player.tribe_state:
        return None

    affordable = get_affordable_buildings(game, player)
    if not affordable:
        return None

    cities = player.tribe_state.cities
    armies = player.tribe_state.get_available_armies()
    fortresses = player.tribe_state.fortresses

    # Priority order:
    # 1. City (if close to victory)
    # 2. Army (if vulnerable)
    # 3. Fortress (if no fortress)
    # 4. General (if armies > generals)
    # 5. Road (for fair cards)
    # 6. City (general case)
    # 7. Army (general case)

    # Close to victory - build city
    if cities >= 3 and BuildingType.CITY in affordable:
        return BuildingType.CITY

    # Vulnerable - build army
    if armies < 2 and BuildingType.ARMY in affordable:
        return BuildingType.ARMY

    # No fortress - build one
    if fortresses == 0 and BuildingType.FORTRESS in affordable:
        return BuildingType.FORTRESS

    # Need generals
    generals = player.tribe_state.generals
    if armies > generals + 1 and BuildingType.GENERAL in affordable:
        return BuildingType.GENERAL

    # Build road for fair cards
    if BuildingType.ROAD in affordable:
        targets = get_road_targets(game, player)
        if targets and random.random() < 0.3:
            return BuildingType.ROAD

    # Default priorities
    if BuildingType.CITY in affordable:
        return BuildingType.CITY
    if BuildingType.ARMY in affordable:
        return BuildingType.ARMY

    # Build anything available
    return random.choice(affordable) if affordable else None


def _select_war_goal(
    available_goals: list[str],
    target_state: "TribeState",
    our_state: "TribeState",
) -> str:
    """Select the best war goal based on strategic considerations."""
    from .state import TribeState

    # Priority 1: Destruction if target is close to monument victory
    if WarGoal.DESTRUCTION in available_goals and target_state.monument_progress >= 2:
        # Higher chance to destroy if they're closer to winning
        if target_state.monument_progress >= 4:
            return WarGoal.DESTRUCTION
        elif target_state.monument_progress >= 3 and random.random() < 0.8:
            return WarGoal.DESTRUCTION
        elif random.random() < 0.5:
            return WarGoal.DESTRUCTION

    # Priority 2: Conquest if target has cities and we want to expand
    if WarGoal.CONQUEST in available_goals:
        # Strong preference if target has many cities or we're close to city victory
        if target_state.cities >= 3 or our_state.cities >= 3:
            if random.random() < 0.7:
                return WarGoal.CONQUEST
        # Otherwise still consider it
        elif random.random() < 0.4:
            return WarGoal.CONQUEST

    # Priority 3: Plunder for resources
    if WarGoal.PLUNDER in available_goals:
        # Good if we need cards for building
        if random.random() < 0.6:
            return WarGoal.PLUNDER

    # Default: pick first available
    return available_goals[0] if available_goals else WarGoal.CONQUEST


def bot_select_war_target(
    game: AgeOfHeroesGame, player: AgeOfHeroesPlayer
) -> tuple[int, str] | None:
    """Bot selects war target and goal. Returns (target_index, goal) or None."""
    if not player.tribe_state:
        return None

    targets = get_valid_war_targets(game, player)
    if not targets:
        return None

    our_armies = player.tribe_state.get_available_armies()

    # Score each target
    best_target = None
    best_score = -1
    best_goal = WarGoal.CONQUEST

    for target_idx, target in targets:
        if not hasattr(target, "tribe_state") or not target.tribe_state:
            continue

        target_armies = target.tribe_state.get_available_armies()
        target_fortresses = target.tribe_state.fortresses

        # Only attack if we have advantage
        effective_defense = target_armies + target_fortresses
        if our_armies <= effective_defense:
            continue

        # Get valid goals for this target
        goals = get_valid_war_goals(game, player, target)
        if not goals:
            continue

        # Score the target
        score = our_armies - effective_defense

        # Select goal based on strategic value
        selected_goal = _select_war_goal(goals, target.tribe_state, player.tribe_state)

        # Bonus score for high-value targets
        if selected_goal == WarGoal.CONQUEST and target.tribe_state.cities >= 4:
            score += 10  # Target close to city victory
        elif selected_goal == WarGoal.DESTRUCTION and target.tribe_state.monument_progress >= 3:
            score += 8  # Target close to monument victory

        if score > best_score:
            best_score = score
            best_target = target_idx
            best_goal = selected_goal

    if best_target is not None:
        return (best_target, best_goal)

    return None


def bot_select_armies(
    game: AgeOfHeroesGame, player: AgeOfHeroesPlayer, is_attacking: bool
) -> tuple[int, int, int, int]:
    """Bot selects armies, generals, heroes for battle.

    Returns (armies, generals, heroes_as_armies, heroes_as_generals).
    """
    if not player.tribe_state:
        return (0, 0, 0, 0)

    available_armies = player.tribe_state.get_available_armies()
    available_generals = player.tribe_state.get_available_generals()

    # Count hero cards
    hero_cards = sum(
        1 for card in player.hand
        if card.card_type == CardType.EVENT and card.subtype == EventType.HERO
    )

    if is_attacking:
        # Commit most forces, keep 1 army for defense
        armies = max(0, available_armies - 1)
        generals = available_generals
        # Use hero cards as armies for extra strength
        heroes_as_armies = hero_cards
        heroes_as_generals = 0
    else:
        # Defending - commit all available forces
        armies = available_armies
        generals = available_generals
        # Use heroes as generals for defense bonus
        heroes_as_armies = 0
        heroes_as_generals = hero_cards

    return (armies, generals, heroes_as_armies, heroes_as_generals)


def bot_should_use_olympics(
    game: AgeOfHeroesGame, player: AgeOfHeroesPlayer
) -> bool:
    """Bot decides whether to use Olympic Games to cancel war."""
    if not player.tribe_state:
        return False

    # Use Olympics if:
    # 1. We have few armies to defend
    # 2. The war goal threatens our victory

    our_armies = player.tribe_state.get_available_armies()
    our_cities = player.tribe_state.cities
    our_monument = player.tribe_state.monument_progress

    war = game.war_state

    # Definitely use if we have no armies
    if our_armies == 0:
        return True

    # Use if conquest and we're close to losing
    if war.goal == WarGoal.CONQUEST and our_cities <= 1:
        return True

    # Use if destruction and we're close to monument victory
    if war.goal == WarGoal.DESTRUCTION and our_monument >= 4:
        return True

    # Use if we're significantly outnumbered
    attacker_strength = war.get_attacker_total_armies() + war.get_attacker_total_generals()
    defender_strength = our_armies + player.tribe_state.fortresses
    if attacker_strength > defender_strength * 2:
        return True

    return False


def bot_should_use_fortune(
    game: AgeOfHeroesGame, player: AgeOfHeroesPlayer, lost_roll: bool
) -> bool:
    """Bot decides whether to use Fortune to reroll."""
    if not lost_roll:
        return False

    if not player.tribe_state:
        return False

    war = game.war_state
    active_players = game.get_active_players()
    player_index = active_players.index(player)

    # Use if we're the attacker and close to winning
    if player_index == war.attacker_index:
        if war.get_attacker_total_armies() > 0:
            # Use Fortune to try to win
            return True

    # Use if we're the defender and about to lose badly
    if player_index == war.defender_index:
        if war.get_defender_total_armies() <= 1:
            # Last chance - use Fortune
            return True

    return False


def score_card_for_discard(card: Card, player: AgeOfHeroesPlayer) -> int:
    """Score a card for discard decision. Higher = more likely to discard."""
    if not player.tribe_state:
        return 50

    score = 50  # Base score

    # Never discard our special monument resource
    if card.card_type == CardType.SPECIAL:
        own_special = player.tribe_state.get_special_resource()
        if card.subtype == own_special:
            return 0  # Never discard
        else:
            # Other special resources have some value for trading
            score = 30

    # Resources have moderate value
    if card.card_type == CardType.RESOURCE:
        # Check if we need this for building
        resource = card.subtype
        needed_count = 0
        for building, costs in BUILDING_COSTS.items():
            if resource in costs:
                needed_count += 1

        # More useful resources are less likely to be discarded
        score = 60 - (needed_count * 10)

    # Events have varying value
    if card.card_type == CardType.EVENT:
        if card.subtype == EventType.HERO:
            score = 20  # Very useful
        elif card.subtype == EventType.FORTUNE:
            score = 30  # Useful
        elif card.subtype == EventType.OLYMPICS:
            # More valuable if we have few armies
            if player.tribe_state.get_available_armies() < 2:
                score = 10
            else:
                score = 40
        else:
            # Other events (disasters handled elsewhere)
            score = 70

    return score


def bot_select_card_to_discard(
    game: AgeOfHeroesGame, player: AgeOfHeroesPlayer
) -> int:
    """Bot selects which card to discard. Returns card index."""
    if not player.hand:
        return 0

    # Score each card
    best_index = 0
    best_score = -1

    for i, card in enumerate(player.hand):
        score = score_card_for_discard(card, player)
        if score > best_score:
            best_score = score
            best_index = i

    return best_index
