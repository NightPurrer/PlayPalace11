# Shared game messages for PlayPalace
# These messages are common across multiple games

# Game names
game-name-ninetynine = Ninety Nine

# Round and turn flow
game-round-start = Runda { $round }.
game-round-end = Runda { $round } zakończona.
game-turn-start = Tura { $player }.
game-your-turn = Twoja kolej.
game-no-turn = Obecnie brak czyjejkolwiek tury.

# Score display
game-scores-header = Obecne statystyki:
game-score-line = { $player }: { $score } points
game-final-scores-header = Finalne statystyki:

# Win/loss
game-winner = Wygrał { $player }!
game-winner-score = { $player } wygrał osiągając { $score } punktów!
game-tiebreaker = It's a tie! Tiebreaker round!
game-tiebreaker-players = It's a tie between { $players }! Tiebreaker round!
game-eliminated = { $player } został wyeliminowany z liczbą { $score } punktów.

# Common options
game-set-target-score = Maksymalna liczba punktów: { $score }
game-enter-target-score = Podaj maksymalną liczbę punktów:
game-option-changed-target = Maksymalna liczba punkót została ustawiona na { $score }.

game-set-team-mode = Team mode: { $mode }
game-select-team-mode = Select team mode
game-option-changed-team = Team mode set to { $mode }.
game-team-mode-individual = Individual
game-team-mode-x-teams-of-y = { $num_teams } teams of { $team_size }

# Boolean option values
option-on = włączone
option-off = wyłączone

# Status box
status-box-closed = Status information closed.

# Game end
game-leave = opuść grę

# Round timer
round-timer-paused = { $player } wstrzymał grę. Naciśnij P, aby rozpocząć następną rundę.
round-timer-resumed = Round timer resumed.
round-timer-countdown = Następna runda za { $seconds }...

# Dice games - keeping/releasing dice
dice-keeping = Keeping { $value }.
dice-rerolling = Rerolling { $value }.
dice-locked = That die is locked and cannot be changed.

# Dealing (card games)
game-deal-counter = Deal { $current }/{ $total }.
game-you-deal = You deal out the cards.
game-player-deals = { $player } deals out the cards.

# Card names
card-name = { $rank } of { $suit }
no-cards = No cards

# Suit names
suit-diamonds = diamonds
suit-clubs = clubs
suit-hearts = hearts
suit-spades = spades

# Rank names
rank-ace = ace
rank-ace-plural = aces
rank-two = 2
rank-two-plural = 2s
rank-three = 3
rank-three-plural = 3s
rank-four = 4
rank-four-plural = 4s
rank-five = 5
rank-five-plural = 5s
rank-six = 6
rank-six-plural = 6s
rank-seven = 7
rank-seven-plural = 7s
rank-eight = 8
rank-eight-plural = 8s
rank-nine = 9
rank-nine-plural = 9s
rank-ten = 10
rank-ten-plural = 10s
rank-jack = jack
rank-jack-plural = jacks
rank-queen = queen
rank-queen-plural = queens
rank-king = king
rank-king-plural = kings

# Poker hand descriptions
poker-high-card-with = { $high } high, with { $rest }
poker-high-card = { $high } high
poker-pair-with = Pair of { $pair }, with { $rest }
poker-pair = Pair of { $pair }
poker-two-pair-with = Two Pair, { $high } and { $low }, with { $kicker }
poker-two-pair = Two Pair, { $high } and { $low }
poker-trips-with = Three of a Kind, { $trips }, with { $rest }
poker-trips = Three of a Kind, { $trips }
poker-straight-high = { $high } high Straight
poker-flush-high-with = { $high } high Flush, with { $rest }
poker-full-house = Full House, { $trips } over { $pair }
poker-quads-with = Four of a Kind, { $quads }, with { $kicker }
poker-quads = Four of a Kind, { $quads }
poker-straight-flush-high = { $high } high Straight Flush
poker-unknown-hand = Unknown hand
