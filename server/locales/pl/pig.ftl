# Pig game messages
# Note: Common messages like round-start, turn-start, target-score are in games.ftl

# Game info
game-name-pig = Pig (Świnia)
pig-category = Gry kościane

# Actions
pig-roll = Rzuć kostką
pig-bank = Bankuj { $points } PKT.

# Game events (Pig-specific)
pig-rolls = { $player } rzuca kostką...
pig-roll-result = Wyrzuca { $roll }, łącznie ma { $total }
pig-bust = O nie! 1! { $player } traci { $points } punktów.
pig-bank-action = { $player } bankuje { $points }, łącznie ma teraz { $total }
pig-winner = Mamy zwycięzcę, jest nim { $player }!

# Pig-specific options
pig-set-min-bank = Minimalna liczba punktów do zabankowania: { $points }
pig-set-dice-sides = Ścianki kości: { $sides }
pig-enter-min-bank = Wpisz minimalną liczbę punktów możliwą do zabankowania:
pig-enter-dice-sides = Podaj liczbę ścianek kości:
pig-option-changed-min-bank = Minimalna liczba punktów do zabankowania została ustawiona na { $points }
pig-option-changed-dice = Od teraz liczba ścianek kości wynosi { $sides }

# Disabled reasons
pig-need-more-points = Aby zabankować, musisz zdobyć więcej punktów.

# Validation errors
pig-error-min-bank-too-high = Minimalna liczba punktów do zabankowania musi być mniejsza niż wynik docelowy.
