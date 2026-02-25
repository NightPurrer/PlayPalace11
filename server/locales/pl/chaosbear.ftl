# Chaos Bear game messages

# Game name
game-name-chaosbear = Niedźwiedź chaosu

# Actions
chaosbear-roll-dice = Rzuć kostką
chaosbear-draw-card = Dobierz kartę
chaosbear-check-status = Sprawdź status

# Game intro (3 separate messages like v10)
chaosbear-intro-1 = Gra Niedźwiedź chaosu się rozpoczęła! Wszyscy gracze startują 30 pól od niedźwiedzia.
chaosbear-intro-2 = Rzuć kostką, aby poruszać się naprzód, i dobieraj karty na każdej wielokrotności liczby 5.
chaosbear-intro-3 = Nie pozwól, aby niedźwiedź Cię złapał!

# Turn announcement
chaosbear-turn = Kolej { $player }; pozycja { $position }.

# Rolling
chaosbear-roll = { $player } wyrzuca { $roll }.
chaosbear-position = { $player } jest teraz na pozycji { $position }.

# Drawing cards
chaosbear-draws-card = { $player } dobiera kartę.
chaosbear-card-impulsion = Impuls! { $player } przenosi się o 3 pola w przód, na pozycję { $position }!
chaosbear-card-super-impulsion = Super impuls! { $player } przenosi się o 5 pól naprzód na pozycję { $position }!
chaosbear-card-tiredness = Zmęczenie! Energia niedźwiedzia minus 1. Ma teraz { $energy } energii.
chaosbear-card-hunger = Głód!! Energia niedźwiedzia plus 1. Ma teraz { $energy } energii.
chaosbear-card-backward = Pchnięcie w tył! { $player } cofa się na pozycję { $position }.
chaosbear-card-random-gift = Losowy prezent!
chaosbear-gift-back = { $player } wraca na pozycję { $position }.
chaosbear-gift-forward = { $player } idzie w przód na pozycję { $position }!

# Bear turn
chaosbear-bear-roll = Niedźwiedź wyrzuca { $roll }, plus energia { $energy }, razem { $total }.
chaosbear-bear-energy-up = Niedźwiedź wyrzuca 3 i zyskuje 1 energii!
chaosbear-bear-position = Niedźwiedź jest teraz na pozycji { $position }!
chaosbear-player-caught = Niedźwiedź łapie { $player }! { $player } został pokonany!
chaosbear-bear-feast = Niedźwiedź traci 3 energii po pożarciu swojej ofiary!

# Status check
chaosbear-status-player-alive = { $player }: na pozycji { $position }.
chaosbear-status-player-caught = { $player }: złapany na pozycji { $position }.
chaosbear-status-bear = Niedźwiedź jest na pozycji { $position } i ma { $energy } energii.

# End game
chaosbear-winner = { $player } przetrwał i wygrywa! Osiągnął pozycję { $position }!
chaosbear-tie = Remis na pozycji { $position }!

# Disabled action reasons
chaosbear-you-are-caught = Zostałeś złapany przez niedźwiedzia.
chaosbear-not-on-multiple = Możesz dobierać karty tylko na polach będących wielokrotnością 5.
