# Rules Of Pirates
PlayPalace team, 2026.

## TL;DR
Pirates of the Lost Seas is an RPG-style adventure game for 2 to 5 players. You sail across a 40-tile map spanning four randomly selected oceans, collecting gems and battling other pirates with cannonballs. As you play, you earn experience points (XP) and level up, unlocking increasingly powerful skills along the way.

The goal is to have the highest score when all 18 gems have been collected. Your score comes entirely from the gems you hold at the end of the game, so attacking other players and stealing their gems is sometimes just as valid a strategy as exploring the map yourself.

It was originally created by Rory Michie in 2017 and has gone through many iterations since then.

## Gameplay
The game is divided into rounds, and within each round every player takes one turn. On your turn, you choose an action: sail to an adjacent tile, fire a cannonball at a nearby opponent, or use one of your unlocked skills.

### The Map
The map consists of 40 tiles arranged in a line, divided into 4 oceans of 10 tiles each. At the start of the game, 4 oceans are randomly chosen from a pool of named seas (such as "Battle Bay", "Developer's Deep", and "Gamer's Gulf", among others). Each player begins at a random position on the map.

As you and other players explore tiles, those tiles become "charted". You can use the Sailor's Instinct skill (once unlocked) to view which of the 8 map sectors have been charted and to what extent.

### Movement
On your turn, you can sail left or right. At the start of the game you can only move 1 tile at a time. As you level up, you unlock faster movement:

* **Level 0+:** Sail 1 tile left or right
* **Level 15+:** Sail up to 2 tiles left or right
* **Level 150+:** Sail up to 3 tiles left or right

You cannot sail beyond the edges of the map (tile 1 or tile 40). Moving ends your turn, and if you land on a tile that contains a gem, you automatically collect it.

### Gems
18 gems are scattered randomly across the 40 tiles at the start of the game. Each gem has a name and a point value:

#### Common Gems (1 point each)
* Opal
* Ruby
* Garnet
* Diamond
* Sapphire
* Emerald
* Amethyst
* Golden Ring
* Moonstone
* Lapis Lazuli
* Amber
* Citrine
* Large Plastic Gem (what is this doing here!)

#### Rare Gems (2 points each)
* Gem of the Palace
* Awesome Blue Bastardstone
* Awesome Red Ppulpstone
* Awesome Red Gorestone

#### Legendary Gem (3 points)
* Definitely Not Cursed Black Pearl (tm)

When you land on a tile with a gem, you collect it automatically. The gem's value is added to your score. Gems can also be stolen from other players through combat (see below).

The game ends when all 18 gems have been collected. The player with the highest score wins. In the event of a tie, a random tiebreaker determines the winner.

### Combat
You can fire a cannonball at any player within 5 tiles of your position (or 10 tiles if you have the Double Devastation buff active). Combat works as follows:

1. **Attack roll:** You roll a six-sided die. Any active attack bonuses (from skills like Sword Fighter or Skilled Captain) are added to your roll.
2. **Defense roll:** The defender rolls a six-sided die. Any active defense bonuses (from skills like Push or Skilled Captain) are added to their roll.
3. **Outcome:** If the attack roll is strictly greater than the defense roll, it's a hit. Otherwise, it's a miss.

**On a hit:** You earn 50-150 XP (before multipliers). You then perform a boarding action:

* **Push:** Shove the defender 3-8 tiles in a chosen direction (left or right). They cannot be pushed past the map edges.
* **Steal:** If gem stealing is enabled and the defender has gems, you can attempt to steal one. A new pair of rolls is made: your steal roll (d6 + attack bonus, if the "with roll bonus" option is on) versus their defense roll (d6 + defense bonus, if applicable). If your roll is higher, you take a random gem from them. If it fails, nothing happens.

**On a miss:** The defender earns 30-100 XP (before multipliers) for successfully fending off the attack.

Attacking ends your turn.

### The Golden Moon
Every 3rd round, the Golden Moon rises. While the Golden Moon is active, all XP gains are tripled. This applies to XP from both combat and gem collection. The moon check action tells you what percentage of gems have been collected so far, displayed as the moon's "brightness".

### Leveling and XP
You earn XP from two main sources:

* **Finding a gem:** 150-300 base XP
* **Winning a combat attack:** 50-150 base XP
* **Successfully defending against an attack:** 30-100 base XP

XP is multiplied by any active multipliers: the Golden Moon (3x during every 3rd round) and the host-configurable combat/gem XP multiplier options.

The XP required to reach a given level is: **level x 20**. So level 1 requires 20 XP, level 10 requires 200 XP, level 25 requires 500 XP, and so on.

### Skills
Skills unlock as you level up. Each skill has unique mechanics. Here is the full list, in order of unlock level:

| Level | Skill | Type | Description |
|-------|-------|------|-------------|
| 0 | Cannonball Shot | Attack | Fire a cannonball at a player within range (5 tiles, or 10 with Double Devastation). |
| 10 | Sailor's Instinct | Info | Opens a status box showing your position and the charting status of all 8 map sectors. |
| 25 | Portal | Cooldown (3 turns) | Teleport to a random position in an ocean occupied by another player. Ends your turn. |
| 40 | Gem Seeker | Limited (3 uses per game) | Reveals the location of one uncollected gem. Does not end your turn. |
| 60 | Sword Fighter | Buff (3 turns, 8-turn cooldown) | Grants +4 to attack rolls for 3 turns. Ends your turn when activated. |
| 75 | Push | Buff (4 turns, 8-turn cooldown) | Grants +3 to defense rolls for 4 turns. Ends your turn when activated. |
| 90 | Skilled Captain | Buff (4 turns, 8-turn cooldown) | Grants +2 to both attack and defense rolls for 4 turns. Ends your turn when activated. |
| 125 | Battleship | Cooldown (2 turns) | Fire two cannonballs in a single turn. Cannot be used while Double Devastation is active. |
| 200 | Double Devastation | Buff (3 turns, 10-turn cooldown) | Doubles your attack range from 5 to 10 tiles for 3 turns. Ends your turn when activated. |

Buff cooldowns tick down at the start of each of your turns. Activating a buff skill consumes your turn for that round.

### Example Turn
It's round 4 and you're at position 17 in Developer's Deep. You're level 62 and have collected a Ruby (1 point) and an Awesome Blue Bastardstone (2 points) so far, for a total of 3 points.

Another player, Captain Bot, is at position 19 with 5 points worth of gems. You decide this is a good time to go on the offensive.

You activate Sword Fighter from the skill menu. This gives you +4 to attack rolls for the next 3 turns, but it costs you this turn.

Next round, it's your turn again. Captain Bot is still within 5 tiles, so you fire a cannonball. You roll a 3, plus your +4 Sword Fighter bonus, giving you an attack total of 7. Captain Bot rolls a 4 for defense with no bonuses. 7 beats 4 -- it's a hit! You choose to attempt a gem steal. Your steal roll comes up 5 (+4 bonus = 9) against their defense of 2. You successfully steal their Emerald (1 point), bringing your score to 4.

### Game Options
The host can configure the following options before starting:

* **Combat XP Multiplier** (0.1 - 3.0, default 1.0): Scales XP earned from combat.
* **Find Gem XP Multiplier** (0.1 - 3.0, default 1.0): Scales XP earned from finding gems.
* **Gem Stealing** (default: "With roll bonus"): Controls whether gem stealing is allowed and whether combat bonuses apply to steal rolls. Options are "With roll bonus", "No roll bonus", and "Disabled".

## Keyboard Shortcuts
Shortcuts specific to the game of Pirates:

* P: Check your current position and which ocean you're in.
* S: Check the status of all players (level, XP, score, and gems).
* Shift+S: Show a detailed status box with the same information.
* M: Check the Golden Moon brightness (only available when the Golden Moon is active).
* K: Open the skill menu to use an available skill.

## Game Theory / Tips
* Early on, focus on exploration rather than combat. Gems are your only source of points, and combat exists to redistribute them -- you can't create points out of thin air by attacking.
* Don't activate buff skills unless you have a clear plan to use them. Sword Fighter and Push both cost you a turn to activate, so burning one with no target nearby is wasteful.
* The Golden Moon (every 3rd round) is a huge deal for leveling. If you can time a gem collection or a fight during a Golden Moon round, you'll gain triple XP and potentially unlock new skills much faster.
* Portal is excellent for chasing down a leading player. If someone has a big gem haul and is far away, portal into their ocean and start firing.
* Battleship is devastating in the late game. Two attacks in one turn means two chances to steal gems. Pair it with Sword Fighter for maximum effectiveness.
* Pay attention to other players' buff timers. If someone just activated Push (+3 defense), wait a few turns before attacking them -- your odds improve significantly once it wears off.
* At very high levels, the ability to move 3 tiles per turn makes you much more able to cut across the uncharted sectors of the map. Beware that you do not pass over gems, however.
