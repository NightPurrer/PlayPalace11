# Rules Of Yahtzee
PlayPalace team, 2026.

## TL;DR
Yahtzee is a classic dice game that has been a household staple since it was commercially released in 1956 by game entrepreneur Edwin S. Lowe. It is one of the most widely played dice games in the world, and chances are good you have encountered it in one form or another.

The goal is to roll five dice and fill in 13 scoring categories on your scoresheet. Each category can only be used once, so choosing when and where to score is the heart of the strategy. The player with the highest total score at the end wins.

## Gameplay
The game supports 1 to 4 players. Everyone takes turns in order, and the game ends once every player has filled all 13 categories on their scoresheet -- that is, after 13 rounds.

On your turn, you roll all five dice. You then get up to two additional rolls (three total per turn). Before each reroll, you may choose which dice to keep and which to reroll. You can keep any combination you like -- all of them, none of them, or anything in between.

After your rolls are done (either because you have used all three or because you are satisfied with what you have), you must choose one of your open scoring categories to record a score in. The score is calculated based on the dice you currently have and the rules of the category you choose. If your dice do not match the category at all, you score zero in that category -- but you still must pick one. This is sometimes called "scratching" a category, and it is an important part of the game's strategy.

Once you have scored, your turn ends and play passes to the next player.

You can optionally play multiple consecutive games in a single session. The number of games can be set in the game options (from 1 to 10).

### Example Turn
You are the first player and it is the start of the game. You roll all five dice and get 3-3-3-5-2.

Three threes looks promising for the Three of a Kind category. You decide to keep the three threes and reroll the 5 and the 2. Your second roll gives you 3-6 for the two rerolled dice, so your hand is now 3-3-3-3-6. Four of a kind!

You still have one roll left. You could keep all four threes and reroll the 6, hoping for a fifth 3 and a Yahtzee (worth 50 points). Or you could play it safe. You decide to go for it -- you reroll the 6 and get a 1. No Yahtzee this time, but 3-3-3-3-1 is still a solid hand.

Now you choose where to score. Four of a Kind would give you the sum of all dice: 3+3+3+3+1 = 13 points. But you could also score in the Fours category for 0 (no fours), the Threes category for 12 (four threes counting 3 each), or Chance for 13 (sum of all dice). You decide to take Threes for 12 points, saving Four of a Kind and Chance for turns where they might pay off more.

### Scoring
Your scoresheet is divided into an Upper Section and a Lower Section.

#### Upper Section
In the upper section, you simply count and add up the dice that match the category's number:

* Ones: Sum of all ones (e.g., 1-1-3-4-6 scores 2)
* Twos: Sum of all twos (e.g., 2-2-2-5-6 scores 6)
* Threes: Sum of all threes (e.g., 3-3-4-5-6 scores 6)
* Fours: Sum of all fours (e.g., 1-4-4-4-5 scores 12)
* Fives: Sum of all fives (e.g., 2-5-5-5-5 scores 20)
* Sixes: Sum of all sixes (e.g., 1-2-6-6-6 scores 18)

**Upper Section Bonus:** If your upper section total is 63 or more, you earn a bonus of 35 points. A handy way to think about it: you need an average of three-of-each across all six upper categories (3x1 + 3x2 + 3x3 + 3x4 + 3x5 + 3x6 = 63). Anything above that is gravy.

#### Lower Section
The lower section has specific combination requirements:

* Three of a Kind: At least three dice showing the same value. Score is the sum of all five dice.
* Four of a Kind: At least four dice showing the same value. Score is the sum of all five dice.
* Full House: Three of one value and two of another (a five-of-a-kind also counts). Score is 25 points.
* Small Straight: Four consecutive dice (e.g., 1-2-3-4, 2-3-4-5, or 3-4-5-6). Score is 30 points.
* Large Straight: Five consecutive dice (1-2-3-4-5 or 2-3-4-5-6). Score is 40 points.
* Yahtzee: All five dice showing the same value. Score is 50 points.
* Chance: Any combination of dice. Score is the sum of all five dice. This is your safety net when nothing else fits well.

#### Yahtzee Bonus
If you roll a Yahtzee and you have already scored 50 in the Yahtzee category, you earn a Yahtzee Bonus of 100 points. You can earn multiple Yahtzee Bonuses in a single game. Note that you must have previously scored a 50 in the Yahtzee category -- if you scratched Yahtzee with a zero earlier, subsequent Yahtzees do not earn the bonus.

Even when claiming a Yahtzee Bonus, you still must choose an open category to score in for that turn.

## Keyboard Shortcuts
Shortcuts specific to the game of Yahtzee:
* R: Roll the dice.
* 1-5: Toggle keeping/rerolling individual dice (by position). After rolling, press a number key to keep that die, or press it again to set it back to reroll.
* D: View the current dice and which ones are being kept.
* C: View the current player's scoresheet.

## Game Theory / Tips
* Always keep the upper bonus in mind. Falling short of 63 in the upper section means missing out on 35 free points. If you are behind on a particular upper category, consider filling it when you get a decent roll rather than gambling for something flashy in the lower section.
* Do not waste Chance early. Chance is your best friend when you have a high-sum roll that does not fit anywhere else neatly. If you burn it on a low total early in the game, you may regret it later when you have no good options.
* Yahtzee is worth going for, but not at all costs. If you already have three or four of a kind after your first roll, it is absolutely worth chasing on your remaining rolls. But do not reroll a perfectly good Full House or Large Straight just because a Yahtzee would score more.
* Scratch strategically. When you have to take a zero somewhere, try to waste a category where the expected value is low anyway. Ones is a common scratch target since even three ones is only worth 3 points. Similarly, scratching the lower section categories that you are unlikely to fill naturally is better than wasting a high-value upper category.
* Full House and straights are all-or-nothing. Since they pay a flat bonus (25, 30, or 40) rather than scaling with dice values, do not over-invest in chasing them when you could be scoring solid points elsewhere. On the other hand, if you are one die away from a Large Straight, that single reroll is almost always worth it.
