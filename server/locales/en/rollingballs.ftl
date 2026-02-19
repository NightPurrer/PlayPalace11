# Rolling Balls game messages
# Note: Common messages like round-start, turn-start are in games.ftl

# Game info
game-name-rollingballs = Rolling Balls

# Turn actions
rb-take = Take { $count } { $count ->
    [one] ball
   *[other] balls
}
rb-reshuffle-action = Reshuffle pipe ({ $remaining } uses remaining)
rb-view-pipe-action = View pipe ({ $remaining } uses remaining)

# Take ball events
rb-you-take = You take { $count } { $count ->
    [one] ball
   *[other] balls
}!
rb-player-takes = { $player } takes { $count } { $count ->
    [one] ball
   *[other] balls
}!
rb-ball-plus = Ball { $num }: { $description }! Plus { $value } points!
rb-ball-minus = Ball { $num }: { $description }! Minus { $value } points!
rb-ball-zero = Ball { $num }: { $description }! No change!
rb-new-score = { $player }'s score: { $score } points.

# Reshuffle events
rb-you-reshuffle = You reshuffle the pipe!
rb-player-reshuffles = { $player } reshuffles the pipe!
rb-reshuffled = The pipe has been reshuffled!
rb-reshuffle-penalty = { $player } loses { $points } { $points ->
    [one] point
   *[other] points
} for reshuffling.

# View pipe
rb-view-pipe-header = Viewing the pipe. There are { $count } balls:
rb-view-pipe-ball = Ball { $num }: { $description }. Value: { $value } points.

# Game start
rb-pipe-filled = The pipe has been filled with { $count } balls!
rb-balls-remaining = { $count } balls remain in the pipe.

# Game end
rb-pipe-empty = The pipe is empty!
rb-score-line = { $player }: { $score } points.
rb-winner = The winner is { $player } with { $score } points!
rb-you-win = You win with { $score } points!
rb-tie = It's a tie between { $players } with { $score } points!

# Options
rb-set-min-take = Minimum balls required to take each turn: { $count }
rb-enter-min-take = Enter the minimum number of balls to take (1-5):
rb-option-changed-min-take = Minimum balls to take set to { $count }.

rb-set-max-take = Maximum balls allowed to take each turn: { $count }
rb-enter-max-take = Enter the maximum number of balls to take (1-5):
rb-option-changed-max-take = Maximum balls to take set to { $count }.

rb-set-view-pipe-limit = View pipe limit: { $count }
rb-enter-view-pipe-limit = Enter view pipe limit (0 to disable, max 100):
rb-option-changed-view-pipe-limit = View pipe limit set to { $count }.

rb-set-reshuffle-limit = Reshuffle limit: { $count }
rb-enter-reshuffle-limit = Enter reshuffle limit (0 to disable, max 100):
rb-option-changed-reshuffle-limit = Reshuffle limit set to { $count }.

rb-set-reshuffle-penalty = Reshuffle penalty: { $points }
rb-enter-reshuffle-penalty = Enter reshuffle penalty (0-5):
rb-option-changed-reshuffle-penalty = Reshuffle penalty set to { $points }.

rb-set-ball-pack = Ball pack: { $pack }
rb-select-ball-pack = Select a ball pack:
rb-option-changed-ball-pack = Ball pack set to { $pack }.

# Disabled reasons
rb-not-enough-balls = Not enough balls in the pipe.
rb-no-reshuffles-left = No reshuffles remaining.
rb-already-reshuffled = You already reshuffled this turn.
rb-no-views-left = No pipe views remaining.
