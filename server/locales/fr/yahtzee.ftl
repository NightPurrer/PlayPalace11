# Messages du jeu Yahtzee

# Informations sur le jeu
game-name-yahtzee = Yahtzee

# Actions - Lancer
yahtzee-roll = Relancer ({ $count } restant)
yahtzee-roll-all = Lancer les dés

# Catégories de score de la section supérieure
yahtzee-score-ones = As pour { $points } points
yahtzee-score-twos = Deux pour { $points } points
yahtzee-score-threes = Trois pour { $points } points
yahtzee-score-fours = Quatre pour { $points } points
yahtzee-score-fives = Cinq pour { $points } points
yahtzee-score-sixes = Six pour { $points } points

# Catégories de score de la section inférieure
yahtzee-score-three-kind = Brelan pour { $points } points
yahtzee-score-four-kind = Carré pour { $points } points
yahtzee-score-full-house = Full pour { $points } points
yahtzee-score-small-straight = Petite suite pour { $points } points
yahtzee-score-large-straight = Grande suite pour { $points } points
yahtzee-score-yahtzee = Yahtzee pour { $points } points
yahtzee-score-chance = Chance pour { $points } points

# Événements de jeu
yahtzee-you-rolled = Vous avez lancé : { $dice }. Lancers restants : { $remaining }
yahtzee-player-rolled = { $player } a lancé : { $dice }. Lancers restants : { $remaining }

# Annonces de score
yahtzee-you-scored = Vous avez marqué { $points } points en { $category }.
yahtzee-player-scored = { $player } a marqué { $points } en { $category }.

# Bonus Yahtzee
yahtzee-you-bonus = Bonus Yahtzee ! +100 points
yahtzee-player-bonus = { $player } a obtenu un bonus Yahtzee ! +100 points

# Bonus de la section supérieure
yahtzee-you-upper-bonus = Bonus de la section supérieure ! +35 points ({ $total } dans la section supérieure)
yahtzee-player-upper-bonus = { $player } a gagné le bonus de la section supérieure ! +35 points
yahtzee-you-upper-bonus-missed = Vous avez raté le bonus de la section supérieure ({ $total } dans la section supérieure, besoin de 63).
yahtzee-player-upper-bonus-missed = { $player } a raté le bonus de la section supérieure.

# Mode de score
yahtzee-choose-category = Choisissez une catégorie pour marquer.
yahtzee-continuing = Continuation du tour.

# Vérifications de statut
yahtzee-check-scoresheet = Vérifier la feuille de score
yahtzee-view-dice = Vérifier la main
yahtzee-your-dice = Vos dés : { $dice }.
yahtzee-your-dice-kept = Vos dés : { $dice }. Gardés : { $kept }
yahtzee-not-rolled = Vous n'avez pas encore lancé.

# Affichage de la feuille de score
yahtzee-scoresheet-header = Feuille de score de { $player }
yahtzee-scoresheet-upper = Section supérieure :
yahtzee-scoresheet-lower = Section inférieure :
yahtzee-scoresheet-category-filled = { $category } : { $points }
yahtzee-scoresheet-category-open = { $category } : -
yahtzee-scoresheet-upper-total-bonus = Total supérieur : { $total } (BONUS : +35)
yahtzee-scoresheet-upper-total-needed = Total supérieur : { $total } ({ $needed } de plus pour le bonus)
yahtzee-scoresheet-yahtzee-bonus = Bonus Yahtzee : { $count } x 100 = { $total }
yahtzee-scoresheet-grand-total = SCORE TOTAL : { $total }

# Noms de catégories (pour les annonces)
yahtzee-category-ones = As
yahtzee-category-twos = Deux
yahtzee-category-threes = Trois
yahtzee-category-fours = Quatre
yahtzee-category-fives = Cinq
yahtzee-category-sixes = Six
yahtzee-category-three-kind = Brelan
yahtzee-category-four-kind = Carré
yahtzee-category-full-house = Full
yahtzee-category-small-straight = Petite suite
yahtzee-category-large-straight = Grande suite
yahtzee-category-yahtzee = Yahtzee
yahtzee-category-chance = Chance

# Fin de jeu
yahtzee-winner = { $player } gagne avec { $score } points !
yahtzee-winners-tie = Égalité ! { $players } ont tous marqué { $score } points !

# Options
yahtzee-set-rounds = Nombre de parties : { $rounds }
yahtzee-enter-rounds = Entrez le nombre de parties (1-10) :
yahtzee-option-changed-rounds = Nombre de parties défini sur { $rounds }.

# Raisons d'action désactivée
yahtzee-no-rolls-left = Vous n'avez plus de lancers.
yahtzee-roll-first = Vous devez d'abord lancer.
yahtzee-category-filled = Cette catégorie est déjà remplie.
