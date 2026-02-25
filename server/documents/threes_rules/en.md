# Rules Of Threes
PlayPalace team, 2026.

## TL;DR
Threes is a classic low-score dice game where the goal is to accumulate the *fewest* points possible. It is one of those beautifully simple games that anyone can pick up in a minute but that still rewards careful decision-making.

You roll five dice and must keep at least one after each roll. Threes are worth zero points, so they are your best friends. Everything else counts at face value -- and you definitely do not want to be stuck holding fives and sixes. The player with the lowest total score after all rounds wins.

## Gameplay
A game of Threes is played over a configurable number of rounds (1 to 20; the default is 10). Every player takes one turn per round, and at the end of all rounds the player with the lowest cumulative score wins.

### Your Turn
On your turn you start with five fresh dice. Press **R** to roll them.

After each roll you must **keep at least one die** before rolling again. Keeping a die locks it in -- it cannot be rerolled for the rest of the turn. Use the number keys **1-5** to toggle which dice you want to keep or put back (see the Keyboard Shortcuts section for details).

You then roll the remaining dice and repeat the process: keep at least one, then roll again.

Your turn ends in one of two ways:

1. **All five dice are locked.** This happens naturally as you keep dice across successive rolls. Once every die is decided, your score is calculated automatically.
2. **Only one unlocked die remains.** When you are down to a single die, it is automatically scored -- there is nothing left to decide.

At any point after your first roll, if all of your dice are either kept or locked, you can press **B** to bank and end your turn immediately.

### Example Turn
It is round 1, and you are up first.

You press **R** and roll: 3, 5, 2, 6, 3. Nice -- two threes! You keep both threes (0 points each).

You roll the remaining three dice: 4, 1, 6. You keep the 1 (only 1 point) by pressing the key for that die.

You roll the last two dice: 3, 5. Another three! You keep the 3 (0 points). Only one die is left, so the turn ends automatically.

Your final dice are: 3, 1, 3, 5, 3. Your turn score is 1 + 5 = **6 points** (the threes contribute nothing). Not bad at all!

### Scoring
Scoring in Threes is refreshingly straightforward:

* **Threes (3s) = 0 points.** This is the core rule that gives the game its name. Always keep your threes.
* **All other dice = face value.** A 1 costs you 1 point, a 2 costs 2, a 4 costs 4, a 5 costs 5, and a 6 costs 6.
* **Five sixes = "Shooting the Moon" = -30 points.** If you manage to end your turn with all five dice showing 6, you are rewarded with negative 30 points -- a massive swing that subtracts from your total. This is extremely rare and extremely satisfying.

Your turn score is added to your cumulative total. After all rounds are complete, the player with the **lowest** total score wins. In the event of a tie, the tied players share the victory.

## Keyboard Shortcuts
Shortcuts specific to the game of Threes:

* **R**: Roll the dice.
* **B**: Bank your score and end your turn (available once all dice are decided).
* **H**: Check your current hand (hear your dice and their statuses).
* **1-5**: Toggle keeping/rerolling dice by position (in the default dice-index keeping style).
* **1-6**: Reroll a kept die by face value (in the Quentin C dice-values keeping style).
* **Shift+1-6**: Keep a die by face value (in the Quentin C dice-values keeping style).

## Game Theory / Tips
* Always keep threes immediately. They cost you nothing and reduce the number of dice you need to worry about.
* Ones and twos are your next-best friends. If you do not have a three to keep, a 1 or 2 is a very cheap hold. Consider keeping ones every time, if you have a comfortable lead.
* If you are well ahead (i.e., well below the other players), you can afford to play conservatively. If you are behind, a moon-shot gamble might be your only path to victory.
