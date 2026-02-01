# Yahtzee game messages

# Game info
game-name-yahtzee = Yahtzee

# Actions - Rolling
yahtzee-roll = Volver a tirar ({ $count } restantes)
yahtzee-roll-all = Tirar dados

# Upper section scoring categories
yahtzee-score-ones = Unos por { $points } puntos
yahtzee-score-twos = Doses por { $points } puntos
yahtzee-score-threes = Treses por { $points } puntos
yahtzee-score-fours = Cuatros por { $points } puntos
yahtzee-score-fives = Cincos por { $points } puntos
yahtzee-score-sixes = Seises por { $points } puntos

# Lower section scoring categories
yahtzee-score-three-kind = Trío por { $points } puntos
yahtzee-score-four-kind = Póker por { $points } puntos
yahtzee-score-full-house = Full House por { $points } puntos
yahtzee-score-small-straight = Escalera Pequeña por { $points } puntos
yahtzee-score-large-straight = Escalera Grande por { $points } puntos
yahtzee-score-yahtzee = Yahtzee por { $points } puntos
yahtzee-score-chance = Azar por { $points } puntos

# Game events
yahtzee-you-rolled = Sacaste: { $dice }. Tiradas restantes: { $remaining }
yahtzee-player-rolled = { $player } sacó: { $dice }. Tiradas restantes: { $remaining }

# Scoring announcements
yahtzee-you-scored = Anotaste { $points } puntos en { $category }.
yahtzee-player-scored = { $player } anotó { $points } en { $category }.

# Yahtzee bonus
yahtzee-you-bonus = ¡Bonificación de Yahtzee! +100 puntos
yahtzee-player-bonus = ¡{ $player } obtuvo una bonificación de Yahtzee! +100 puntos

# Upper section bonus
yahtzee-you-upper-bonus = ¡Bonificación de sección superior! +35 puntos ({ $total } en sección superior)
yahtzee-player-upper-bonus = ¡{ $player } ganó la bonificación de sección superior! +35 puntos
yahtzee-you-upper-bonus-missed = Perdiste la bonificación de sección superior ({ $total } en sección superior, se necesitaban 63).
yahtzee-player-upper-bonus-missed = { $player } perdió la bonificación de sección superior.

# Scoring mode
yahtzee-choose-category = Elige una categoría para anotar.
yahtzee-continuing = Continuando turno.

# Status checks
yahtzee-check-scoresheet = Ver tarjeta de puntuación
yahtzee-view-dice = Ver mano
yahtzee-your-dice = Tus dados: { $dice }.
yahtzee-your-dice-kept = Tus dados: { $dice }. Manteniendo: { $kept }
yahtzee-not-rolled = Aún no has tirado.

# Scoresheet display
yahtzee-scoresheet-header = Tarjeta de Puntuación de { $player }
yahtzee-scoresheet-upper = Sección Superior:
yahtzee-scoresheet-lower = Sección Inferior:
yahtzee-scoresheet-category-filled = { $category }: { $points }
yahtzee-scoresheet-category-open = { $category }: -
yahtzee-scoresheet-upper-total-bonus = Total Superior: { $total } (BONIFICACIÓN: +35)
yahtzee-scoresheet-upper-total-needed = Total Superior: { $total } ({ $needed } más para bonificación)
yahtzee-scoresheet-yahtzee-bonus = Bonificaciones de Yahtzee: { $count } x 100 = { $total }
yahtzee-scoresheet-grand-total = PUNTUACIÓN TOTAL: { $total }

# Category names (for announcements)
yahtzee-category-ones = Unos
yahtzee-category-twos = Doses
yahtzee-category-threes = Treses
yahtzee-category-fours = Cuatros
yahtzee-category-fives = Cincos
yahtzee-category-sixes = Seises
yahtzee-category-three-kind = Trío
yahtzee-category-four-kind = Póker
yahtzee-category-full-house = Full House
yahtzee-category-small-straight = Escalera Pequeña
yahtzee-category-large-straight = Escalera Grande
yahtzee-category-yahtzee = Yahtzee
yahtzee-category-chance = Azar

# Game end
yahtzee-winner = ¡{ $player } gana con { $score } puntos!
yahtzee-winners-tie = ¡Es un empate! ¡{ $players } todos anotaron { $score } puntos!

# Options
yahtzee-set-rounds = Número de juegos: { $rounds }
yahtzee-enter-rounds = Ingresa el número de juegos (1-10):
yahtzee-option-changed-rounds = Número de juegos establecido en { $rounds }.

# Disabled action reasons
yahtzee-no-rolls-left = No te quedan tiradas.
yahtzee-roll-first = Necesitas tirar primero.
yahtzee-category-filled = Esa categoría ya está llena.
