# Rules Of Light Turret
PlayPalace team, 2026.

## TL;DR
Light Turret is a resource management game for 2 to 4 players, blending risk and reward in a way that feels a bit like a push-your-luck game with a strategic twist. The concept is simple: you have a turret, and you shoot it to accumulate light and coins. But be careful - if your light exceeds your turret's power capacity, you're eliminated.

The goal is to finish the game with the most light. You can spend coins on upgrades to raise your power limit, giving yourself more room to keep shooting, but upgrades carry a 25% chance of backfiring and adding light to your turret instead. The game runs for a set number of rounds, and whoever has the most light at the end wins.

## Gameplay
The game is divided into rounds, in which every surviving player takes a turn. On your turn, you have two choices: shoot the turret or buy an upgrade.

### Shooting
Shooting the turret is the core action. When you shoot, you gain a random amount of light (between 1 and 4) and earn coins equal to twice the light gained. So if you gain 3 light, you also pocket 6 coins.

If your total light exceeds your power, you're eliminated on the spot. Your light total still counts toward the final standings, but you can no longer take turns.

### Upgrading
If you have at least 10 coins, you can spend them on a power upgrade instead of shooting. A successful upgrade increases your power by a random amount between 2 and 8, giving you more headroom before elimination.

However, there's a 25% chance that the upgrade goes wrong. When it backfires, instead of gaining power, a random amount of light (between 1 and 5) gets added to your turret. This can even eliminate you if it pushes your light over your power limit.

### Game End
The game ends when one of two conditions is met:

* The maximum number of rounds has been reached (default: 50 rounds, configurable from 10 to 200).
* All players have been eliminated.

When the game ends, the player with the most accumulated light wins. In the event of a tie, it is declared as such.

### Example Turn
You are playing with the default starting power of 10. You currently have 6 light and 8 coins. It's your turn.

You decide to shoot. The turret fires and you gain 3 light, bringing you to 9, and you earn 6 coins, bringing your total to 14. You're close to the edge now - one more bad shot and you could be eliminated.

Next round, you decide to buy an upgrade for 10 coins. The upgrade succeeds, granting you 5 extra power. Your power is now 15, and you still have 9 light and 4 coins. You've given yourself some breathing room.

The round after that, another player shoots and gains 4 light, pushing them to 11 - but their power is only 10. They're eliminated. Meanwhile, you can keep shooting comfortably for a while.

### Scoring
Your score is simply your total accumulated light at the end of the game. Every point of light you gain from shooting (1-4 per shot) and from upgrade accidents (1-5 per accident) adds to your final total.

The player with the highest light total wins. Eliminated players are still ranked by their light total, so getting eliminated doesn't necessarily mean you lose - it just means you can't gain any more light.

## Game Options
Before starting, the host can configure two settings:

* **Starting Power**: How much power each player begins with. Default is 10, configurable from 5 to 30. Higher values mean more room before elimination.
* **Max Rounds**: How many rounds the game lasts. Default is 50, configurable from 10 to 200. More rounds means more opportunities to accumulate light.

## Keyboard Shortcuts
Shortcuts specific to the game of Light Turret:
* Space: Shoot the turret.
* U: Buy an upgrade (costs 10 coins).
* C: Check stats for all players (available to spectators too).

## Game Theory / Tips
* Keep an eye on the gap between your light and power. If you're within 4 points of your limit, seriously consider buying an upgrade before shooting again. One unlucky 4-light shot could end your game.
* Coins are only useful for upgrades, and upgrades cost 10 coins. Since each shot gives you twice the light in coins (2-8 coins per shot), it typically takes 2-3 shots to afford an upgrade. Plan accordingly.
* The upgrade backfire chance is 25%, which is significant. That is part of the luck of Light Turret!
* Being eliminated isn't always the end of the world. I have personally seen games where the victor was not the last one standing. They are rare; they do happen.
