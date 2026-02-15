# Rules Of Ludo
PlayPalace team, 2026.

## TL;DR
Ludo is a race game where each player tries to move four tokens from their yard, around the main track, and into home before everyone else.

You roll a die, move one valid token, and use 6s to bring new tokens onto the board and earn extra turns. You can capture opponents on unsafe squares to send their tokens back to the yard.

The first player to finish all four tokens wins.

## Gameplay
PlayPalace Ludo supports **2 to 4 players**.

At the start, each player is assigned a color and receives four tokens, all beginning in the yard.

On your turn:

1. Roll the die.
2. If no token can legally move for that roll, your turn ends.
3. If exactly one token can move, it moves automatically.
4. If multiple tokens can move, choose which token to move.

### Movement Rules
* A token in the **yard** can only enter play on a roll of **6**.
* When entering play, the token goes to your color's start square.
* Tokens on the **track** move forward by the rolled value and wrap around the board.
* After passing your home entry, the token moves into your **home column**.
* Reaching the end of the home column exactly finishes the token.

### Captures And Safe Squares
If your moved token lands on an opponent token on the track, that opponent token is captured and sent back to the yard.

Captures do **not** happen on safe squares. Safe squares are:

* Fixed safe squares: **9, 22, 35, 48**.
* Optional start-square safety (host option): each player's starting square also counts as safe.

### Rolling 6 And Extra Turns
Rolling a 6 grants an extra turn after your move, but beware, rolling 3 6's in a row will end your turn and negate all of your rols for that turn.

## Winning
Each token that reaches the end of home counts as finished.

The first player to finish all 4 tokens wins immediately.

## Game Options
* **Max consecutive sixes:** How many consecutive 6s are allowed before penalty rollback (default 3, range 0-5; 0 disables the penalty).
* **Safe start squares:** If enabled, starting squares are safe from captures.

## Keyboard Shortcuts
Shortcuts specific to Ludo:

* **R:** Roll die.
* **1-4:** Move token 1 through token 4 (when selection is needed).
* **V:** View board status (all players, token states, and last roll).

## Game Theory / Tips
* Getting at least one token onto the board early improves your chance to use future rolls efficiently.
* Splitting tokens can increase flexibility, but clustered tokens can apply stronger capture pressure.
* Keep track of safe squares and try to end moves on or near them when under threat.
