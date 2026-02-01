# Yahtzee-Spielnachrichten

# Spielinformationen
game-name-yahtzee = Yahtzee

# Aktionen - Würfeln
yahtzee-roll = Neu würfeln ({ $count } übrig)
yahtzee-roll-all = Würfel werfen

# Oberer Bereich Bewertungskategorien
yahtzee-score-ones = Einsen für { $points } Punkte
yahtzee-score-twos = Zweien für { $points } Punkte
yahtzee-score-threes = Dreien für { $points } Punkte
yahtzee-score-fours = Vieren für { $points } Punkte
yahtzee-score-fives = Fünfen für { $points } Punkte
yahtzee-score-sixes = Sechsen für { $points } Punkte

# Unterer Bereich Bewertungskategorien
yahtzee-score-three-kind = Drilling für { $points } Punkte
yahtzee-score-four-kind = Vierling für { $points } Punkte
yahtzee-score-full-house = Full House für { $points } Punkte
yahtzee-score-small-straight = Kleine Straße für { $points } Punkte
yahtzee-score-large-straight = Große Straße für { $points } Punkte
yahtzee-score-yahtzee = Yahtzee für { $points } Punkte
yahtzee-score-chance = Chance für { $points } Punkte

# Spielereignisse
yahtzee-you-rolled = Sie würfelten: { $dice }. Verbleibende Würfe: { $remaining }
yahtzee-player-rolled = { $player } würfelte: { $dice }. Verbleibende Würfe: { $remaining }

# Punkteankündigungen
yahtzee-you-scored = Sie erzielten { $points } Punkte in { $category }.
yahtzee-player-scored = { $player } erzielte { $points } in { $category }.

# Yahtzee-Bonus
yahtzee-you-bonus = Yahtzee-Bonus! +100 Punkte
yahtzee-player-bonus = { $player } erhielt einen Yahtzee-Bonus! +100 Punkte

# Oberer Bereich Bonus
yahtzee-you-upper-bonus = Oberer Bereich Bonus! +35 Punkte ({ $total } im oberen Bereich)
yahtzee-player-upper-bonus = { $player } erhielt den Bonus für den oberen Bereich! +35 Punkte
yahtzee-you-upper-bonus-missed = Sie verpassten den Bonus für den oberen Bereich ({ $total } im oberen Bereich, benötigt 63).
yahtzee-player-upper-bonus-missed = { $player } verpasste den Bonus für den oberen Bereich.

# Bewertungsmodus
yahtzee-choose-category = Wählen Sie eine Kategorie zum Bewerten.
yahtzee-continuing = Zug fortsetzen.

# Statusprüfungen
yahtzee-check-scoresheet = Wertungsblatt prüfen
yahtzee-view-dice = Hand prüfen
yahtzee-your-dice = Ihre Würfel: { $dice }.
yahtzee-your-dice-kept = Ihre Würfel: { $dice }. Behalten: { $kept }
yahtzee-not-rolled = Sie haben noch nicht gewürfelt.

# Wertungsblattanzeige
yahtzee-scoresheet-header = Wertungsblatt von { $player }
yahtzee-scoresheet-upper = Oberer Bereich:
yahtzee-scoresheet-lower = Unterer Bereich:
yahtzee-scoresheet-category-filled = { $category }: { $points }
yahtzee-scoresheet-category-open = { $category }: -
yahtzee-scoresheet-upper-total-bonus = Oberer Bereich Gesamt: { $total } (BONUS: +35)
yahtzee-scoresheet-upper-total-needed = Oberer Bereich Gesamt: { $total } ({ $needed } mehr für Bonus)
yahtzee-scoresheet-yahtzee-bonus = Yahtzee-Boni: { $count } × 100 = { $total }
yahtzee-scoresheet-grand-total = GESAMTPUNKTZAHL: { $total }

# Kategoriennamen (für Ankündigungen)
yahtzee-category-ones = Einsen
yahtzee-category-twos = Zweien
yahtzee-category-threes = Dreien
yahtzee-category-fours = Vieren
yahtzee-category-fives = Fünfen
yahtzee-category-sixes = Sechsen
yahtzee-category-three-kind = Drilling
yahtzee-category-four-kind = Vierling
yahtzee-category-full-house = Full House
yahtzee-category-small-straight = Kleine Straße
yahtzee-category-large-straight = Große Straße
yahtzee-category-yahtzee = Yahtzee
yahtzee-category-chance = Chance

# Spielende
yahtzee-winner = { $player } gewinnt mit { $score } Punkten!
yahtzee-winners-tie = Es ist ein Unentschieden! { $players } erzielten alle { $score } Punkte!

# Optionen
yahtzee-set-rounds = Anzahl der Spiele: { $rounds }
yahtzee-enter-rounds = Anzahl der Spiele eingeben (1-10):
yahtzee-option-changed-rounds = Anzahl der Spiele auf { $rounds } gesetzt.

# Gründe für deaktivierte Aktionen
yahtzee-no-rolls-left = Sie haben keine Würfe mehr.
yahtzee-roll-first = Sie müssen zuerst würfeln.
yahtzee-category-filled = Diese Kategorie ist bereits ausgefüllt.
