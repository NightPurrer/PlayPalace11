"""Combat/War system for Age of Heroes."""

from __future__ import annotations
import random
from typing import TYPE_CHECKING

from .cards import Card, CardType, EventType, get_card_name
from .state import (
    WarState,
    WarGoal,
    get_war_goal_name,
    get_tribe_name,
)

if TYPE_CHECKING:
    from .game import AgeOfHeroesGame, AgeOfHeroesPlayer


def can_declare_war(game: AgeOfHeroesGame, player: AgeOfHeroesPlayer) -> str | None:
    """Check if a player can declare war. Returns error message or None."""
    if not player.tribe_state:
        return "No tribe state"

    # Need at least one available army
    if player.tribe_state.get_available_armies() < 1:
        return "ageofheroes-war-no-army"

    # Need at least one valid target
    if not get_valid_war_targets(game, player):
        return "No valid targets"

    return None


def get_valid_war_targets(
    game: AgeOfHeroesGame, player: AgeOfHeroesPlayer
) -> list[tuple[int, AgeOfHeroesPlayer]]:
    """Get list of valid war targets (player_index, player)."""
    targets = []
    active_players = game.get_active_players()
    player_index = active_players.index(player)

    for i, p in enumerate(active_players):
        if i == player_index:
            continue
        if not hasattr(p, "tribe_state") or not p.tribe_state:
            continue
        if p.tribe_state.is_eliminated():
            continue

        # Can attack anyone (for simplicity)
        # In classic rules, might be limited to neighbors without roads
        targets.append((i, p))

    return targets


def get_valid_war_goals(
    game: AgeOfHeroesGame,
    attacker: AgeOfHeroesPlayer,
    defender: AgeOfHeroesPlayer,
) -> list[str]:
    """Get list of valid war goals against a specific defender."""
    goals = []

    if not defender.tribe_state:
        return goals

    # Conquest - can always try to take a city (if defender has any)
    if defender.tribe_state.cities > 0:
        goals.append(WarGoal.CONQUEST)

    # Plunder - can always try to steal cards (if defender has any)
    if len(defender.hand) > 0:
        goals.append(WarGoal.PLUNDER)

    # Destruction - can destroy monument progress (if defender has any)
    if defender.tribe_state.monument_progress > 0:
        goals.append(WarGoal.DESTRUCTION)

    return goals


def declare_war(
    game: AgeOfHeroesGame,
    attacker: AgeOfHeroesPlayer,
    defender_index: int,
    goal: str,
) -> bool:
    """Declare war on another player."""
    active_players = game.get_active_players()

    if defender_index < 0 or defender_index >= len(active_players):
        return False

    attacker_index = active_players.index(attacker)
    defender = active_players[defender_index]

    if not hasattr(defender, "tribe_state") or not defender.tribe_state:
        return False

    # Initialize war state
    game.war_state = WarState(
        attacker_index=attacker_index,
        defender_index=defender_index,
        goal=goal,
    )

    # Announce war declaration
    game.play_sound("game_ageofheroes/war.ogg")

    for p in game.players:
        user = game.get_user(p)
        if user:
            locale = user.locale
            goal_name = get_war_goal_name(goal, locale)
            user.speak_l(
                "ageofheroes-war-declare",
                attacker=attacker.name,
                defender=defender.name,
                goal=goal_name,
            )

    return True


def check_olympics_defense(game: AgeOfHeroesGame) -> AgeOfHeroesPlayer | None:
    """Check if defender has Olympic Games card to cancel war."""
    active_players = game.get_active_players()
    war = game.war_state

    if war.defender_index < 0 or war.defender_index >= len(active_players):
        return None

    defender = active_players[war.defender_index]
    if not hasattr(defender, "hand"):
        return None

    # Check if defender has Olympic Games
    for card in defender.hand:
        if card.card_type == CardType.EVENT and card.subtype == EventType.OLYMPICS:
            return defender

    return None


def use_olympics(game: AgeOfHeroesGame, player: AgeOfHeroesPlayer) -> bool:
    """Use Olympic Games to cancel war."""
    # Find and remove Olympics card
    for i, card in enumerate(player.hand):
        if card.card_type == CardType.EVENT and card.subtype == EventType.OLYMPICS:
            removed = player.hand.pop(i)
            game.discard_pile.append(removed)

            # Cancel the war
            game.war_state.cancelled_by_olympics = True
            game.play_sound("game_ageofheroes/olympics.ogg")

            game.broadcast_l("ageofheroes-olympics-cancel", name=player.name)
            return True

    return False


def prepare_forces(
    game: AgeOfHeroesGame,
    player: AgeOfHeroesPlayer,
    armies: int,
    generals: int,
    heroes: int = 0,
    hero_generals: int = 0,
) -> bool:
    """Prepare forces for battle."""
    if not player.tribe_state:
        return False

    active_players = game.get_active_players()
    player_index = active_players.index(player)
    war = game.war_state

    # Validate army/general counts
    available_armies = player.tribe_state.get_available_armies()
    available_generals = player.tribe_state.get_available_generals()

    # Count hero cards available
    hero_cards = sum(
        1 for card in player.hand
        if card.card_type == CardType.EVENT and card.subtype == EventType.HERO
    )

    total_heroes_used = heroes + hero_generals
    if total_heroes_used > hero_cards:
        return False

    if armies > available_armies:
        return False
    if generals > available_generals:
        return False

    # Commit forces
    if player_index == war.attacker_index:
        war.attacker_armies = armies
        war.attacker_generals = generals
        war.attacker_heroes = heroes
        war.attacker_hero_generals = hero_generals
        war.attacker_prepared = True
    elif player_index == war.defender_index:
        war.defender_armies = armies
        war.defender_generals = generals
        war.defender_heroes = heroes
        war.defender_hero_generals = hero_generals
        war.defender_prepared = True
    else:
        return False

    # Remove hero cards from hand
    for _ in range(total_heroes_used):
        for i, card in enumerate(player.hand):
            if card.card_type == CardType.EVENT and card.subtype == EventType.HERO:
                removed = player.hand.pop(i)
                game.discard_pile.append(removed)
                break

    # Announce preparation
    user = game.get_user(player)
    if user:
        user.speak_l(
            "ageofheroes-war-prepared",
            armies=armies + heroes,
            generals=generals + hero_generals,
            heroes=0,  # Heroes already counted in armies/generals
        )

    return True


def roll_battle_dice(
    game: AgeOfHeroesGame, is_attacker: bool
) -> tuple[int, int, int]:
    """Roll dice for battle. Returns (die1, die2, bonus)."""
    war = game.war_state
    active_players = game.get_active_players()

    # Roll two dice
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    base_total = die1 + die2

    # Calculate bonuses
    bonus = 0

    if is_attacker:
        # Attacker bonus: +1 per general
        bonus += war.get_attacker_total_generals()
        war.attacker_dice = [die1, die2]
    else:
        # Defender bonus: +1 per general, +1 per fortress
        bonus += war.get_defender_total_generals()

        defender_index = war.defender_index
        if defender_index < len(active_players):
            defender = active_players[defender_index]
            if hasattr(defender, "tribe_state") and defender.tribe_state:
                bonus += defender.tribe_state.fortresses

        war.defender_dice = [die1, die2]

    game.play_sound("game_pig/dice.ogg")

    return die1, die2, bonus


def resolve_battle_round(game: AgeOfHeroesGame) -> tuple[str, int, int]:
    """Resolve one round of battle. Returns (winner, attacker_losses, defender_losses).

    Winner is 'attacker', 'defender', or 'draw'.
    """
    war = game.war_state
    active_players = game.get_active_players()

    # Roll for both sides
    att_die1, att_die2, att_bonus = roll_battle_dice(game, is_attacker=True)
    def_die1, def_die2, def_bonus = roll_battle_dice(game, is_attacker=False)

    attacker_total = att_die1 + att_die2 + att_bonus
    defender_total = def_die1 + def_die2 + def_bonus

    # Announce rolls
    if war.attacker_index < len(active_players):
        attacker = active_players[war.attacker_index]
        for p in game.players:
            user = game.get_user(p)
            if user:
                if p == attacker:
                    user.speak_l(
                        "ageofheroes-dice-roll-you",
                        total=att_die1 + att_die2,
                        bonus=att_bonus,
                    )
                else:
                    user.speak_l(
                        "ageofheroes-dice-roll",
                        name=attacker.name,
                        total=att_die1 + att_die2,
                        bonus=att_bonus,
                    )

    if war.defender_index < len(active_players):
        defender = active_players[war.defender_index]
        for p in game.players:
            user = game.get_user(p)
            if user:
                if p == defender:
                    user.speak_l(
                        "ageofheroes-dice-roll-you",
                        total=def_die1 + def_die2,
                        bonus=def_bonus,
                    )
                else:
                    user.speak_l(
                        "ageofheroes-dice-roll",
                        name=defender.name,
                        total=def_die1 + def_die2,
                        bonus=def_bonus,
                    )

    # Determine winner
    attacker_losses = 0
    defender_losses = 0

    if attacker_total > defender_total:
        # Attacker wins this round - defender loses an army
        defender_losses = 1
        winner = "attacker"
        game.play_sound("game_ageofheroes/attack_win.ogg")
    elif defender_total > attacker_total:
        # Defender wins this round - attacker loses an army
        attacker_losses = 1
        winner = "defender"
        game.play_sound("game_ageofheroes/defend_win.ogg")
    else:
        # Draw - both lose an army
        attacker_losses = 1
        defender_losses = 1
        winner = "draw"

    # Apply losses
    apply_battle_losses(game, attacker_losses, defender_losses)

    return winner, attacker_losses, defender_losses


def apply_battle_losses(
    game: AgeOfHeroesGame, attacker_losses: int, defender_losses: int
) -> None:
    """Apply army losses from battle."""
    war = game.war_state
    active_players = game.get_active_players()

    # Apply attacker losses
    if attacker_losses > 0 and war.attacker_index < len(active_players):
        attacker = active_players[war.attacker_index]
        if hasattr(attacker, "tribe_state") and attacker.tribe_state:
            # First lose heroes being used as armies
            heroes_lost = min(attacker_losses, war.attacker_heroes)
            war.attacker_heroes -= heroes_lost
            attacker_losses -= heroes_lost

            # Then lose regular armies
            if attacker_losses > 0:
                armies_lost = min(attacker_losses, war.attacker_armies)
                war.attacker_armies -= armies_lost
                attacker.tribe_state.armies -= armies_lost
                game.army_supply += armies_lost

    # Apply defender losses
    if defender_losses > 0 and war.defender_index < len(active_players):
        defender = active_players[war.defender_index]
        if hasattr(defender, "tribe_state") and defender.tribe_state:
            # First lose heroes being used as armies
            heroes_lost = min(defender_losses, war.defender_heroes)
            war.defender_heroes -= heroes_lost
            defender_losses -= heroes_lost

            # Then lose regular armies
            if defender_losses > 0:
                armies_lost = min(defender_losses, war.defender_armies)
                war.defender_armies -= armies_lost
                defender.tribe_state.armies -= armies_lost
                game.army_supply += armies_lost


def is_battle_over(game: AgeOfHeroesGame) -> bool:
    """Check if the battle is over (one side has no armies left)."""
    war = game.war_state

    attacker_armies = war.get_attacker_total_armies()
    defender_armies = war.get_defender_total_armies()

    return attacker_armies <= 0 or defender_armies <= 0


def get_battle_winner(game: AgeOfHeroesGame) -> str | None:
    """Get the winner of the battle, or None if not over."""
    if not is_battle_over(game):
        return None

    war = game.war_state
    attacker_armies = war.get_attacker_total_armies()
    defender_armies = war.get_defender_total_armies()

    if attacker_armies > 0 and defender_armies <= 0:
        return "attacker"
    elif defender_armies > 0 and attacker_armies <= 0:
        return "defender"
    else:
        # Both wiped out - defender wins by default
        return "defender"


def apply_war_outcome(game: AgeOfHeroesGame) -> None:
    """Apply the outcome of the war based on the goal."""
    war = game.war_state
    winner = get_battle_winner(game)
    active_players = game.get_active_players()

    if winner != "attacker":
        # Attacker lost or draw - no spoils
        return_surviving_forces(game)
        return

    # Attacker won - apply goal
    if war.attacker_index >= len(active_players):
        return
    if war.defender_index >= len(active_players):
        return

    attacker = active_players[war.attacker_index]
    defender = active_players[war.defender_index]

    if not hasattr(attacker, "tribe_state") or not attacker.tribe_state:
        return
    if not hasattr(defender, "tribe_state") or not defender.tribe_state:
        return

    if war.goal == WarGoal.CONQUEST:
        # Take a city
        if defender.tribe_state.cities > 0:
            defender.tribe_state.cities -= 1
            attacker.tribe_state.cities += 1
            game.broadcast_l(
                "ageofheroes-conquest-success",
                attacker=attacker.name,
                defender=defender.name,
            )
            game.play_sound("game_ageofheroes/conquest.ogg")

    elif war.goal == WarGoal.PLUNDER:
        # Steal cards
        cards_to_steal = min(2, len(defender.hand))
        if cards_to_steal > 0:
            stolen = []
            for _ in range(cards_to_steal):
                if defender.hand:
                    # Steal random card
                    idx = random.randint(0, len(defender.hand) - 1)
                    card = defender.hand.pop(idx)
                    attacker.hand.append(card)
                    stolen.append(card)

            game.broadcast_l(
                "ageofheroes-plunder-success",
                attacker=attacker.name,
                count=len(stolen),
                defender=defender.name,
            )
            game.play_sound("game_ageofheroes/plunder.ogg")

    elif war.goal == WarGoal.DESTRUCTION:
        # Destroy monument progress
        if defender.tribe_state.monument_progress > 0:
            defender.tribe_state.monument_progress -= 1
            game.broadcast_l(
                "ageofheroes-destruction-success",
                attacker=attacker.name,
                defender=defender.name,
            )
            game.play_sound("game_ageofheroes/destruction.ogg")

    return_surviving_forces(game)


def return_surviving_forces(game: AgeOfHeroesGame) -> None:
    """Return surviving armies after battle."""
    war = game.war_state
    active_players = game.get_active_players()

    # Attacker's surviving armies return
    if war.attacker_index < len(active_players):
        attacker = active_players[war.attacker_index]
        if hasattr(attacker, "tribe_state") and attacker.tribe_state:
            surviving_armies = war.attacker_armies
            surviving_generals = war.attacker_generals

            if surviving_armies > 0 or surviving_generals > 0:
                # Check if attacker has road to return immediately
                # For simplicity, always delay return
                attacker.tribe_state.returning_armies = surviving_armies
                attacker.tribe_state.returning_generals = surviving_generals

                user = game.get_user(attacker)
                if user:
                    user.speak_l(
                        "ageofheroes-army-return-delayed",
                        count=surviving_armies + surviving_generals,
                    )

    # Defender's armies stay (they're defending their home)
    # No return needed

    # Reset war state
    war.reset()


def check_fortune_reroll(
    game: AgeOfHeroesGame, player: AgeOfHeroesPlayer
) -> bool:
    """Check if player has Fortune card for reroll."""
    for card in player.hand:
        if card.card_type == CardType.EVENT and card.subtype == EventType.FORTUNE:
            return True
    return False


def use_fortune_reroll(game: AgeOfHeroesGame, player: AgeOfHeroesPlayer) -> bool:
    """Use Fortune card to reroll dice."""
    for i, card in enumerate(player.hand):
        if card.card_type == CardType.EVENT and card.subtype == EventType.FORTUNE:
            removed = player.hand.pop(i)
            game.discard_pile.append(removed)
            game.broadcast_l("ageofheroes-fortune-reroll", name=player.name)
            game.play_sound("game_ageofheroes/fortune.ogg")
            return True
    return False
