# Age of Heroes game messages
# A civilization-building card game for 2-6 players

# Game name
game-name-ageofheroes = L'Âge des Héros

# Tribes
ageofheroes-tribe-egyptians = Égyptiens
ageofheroes-tribe-romans = Romains
ageofheroes-tribe-greeks = Grecs
ageofheroes-tribe-babylonians = Babyloniens
ageofheroes-tribe-celts = Celtes
ageofheroes-tribe-chinese = Chinois

# Special Resources (for monuments)
ageofheroes-special-limestone = Calcaire
ageofheroes-special-concrete = Béton
ageofheroes-special-marble = Marbre
ageofheroes-special-bricks = Briques
ageofheroes-special-sandstone = Grès
ageofheroes-special-granite = Granit

# Standard Resources
ageofheroes-resource-iron = Fer
ageofheroes-resource-wood = Bois
ageofheroes-resource-grain = Blé
ageofheroes-resource-stone = Pierre
ageofheroes-resource-gold = Or

# Events
ageofheroes-event-population-growth = Croissance de Population
ageofheroes-event-earthquake = Tremblement de Terre
ageofheroes-event-eruption = Éruption
ageofheroes-event-hunger = Famine
ageofheroes-event-barbarians = Barbares
ageofheroes-event-olympics = Jeux Olympiques
ageofheroes-event-hero = Héros
ageofheroes-event-fortune = Fortune

# Buildings
ageofheroes-building-army = Armée
ageofheroes-building-fortress = Forteresse
ageofheroes-building-general = Général
ageofheroes-building-road = Route
ageofheroes-building-city = Cité

# Actions
ageofheroes-action-tax-collection = Collecte d'Impôts
ageofheroes-action-construction = Construction
ageofheroes-action-war = Guerre
ageofheroes-action-do-nothing = Ne Rien Faire
ageofheroes-play = Jouer

# War goals
ageofheroes-war-conquest = Conquête
ageofheroes-war-plunder = Pillage
ageofheroes-war-destruction = Destruction

# Game options
ageofheroes-set-victory-cities = Cités pour victoire : { $cities }
ageofheroes-enter-victory-cities = Entrez le nombre de cités pour gagner (3-7)
ageofheroes-set-victory-monument = Achèvement du monument : { $progress }%
ageofheroes-toggle-neighbor-roads = Routes uniquement aux voisins : { $enabled }
ageofheroes-set-max-hand = Taille maximale de main : { $cards } cartes

# Option change announcements
ageofheroes-option-changed-victory-cities = La victoire requiert { $cities } cités.
ageofheroes-option-changed-victory-monument = Seuil d'achèvement du monument fixé à { $progress }%.
ageofheroes-option-changed-neighbor-roads = Routes uniquement aux voisins { $enabled }.
ageofheroes-option-changed-max-hand = Taille maximale de main fixée à { $cards } cartes.

# Setup phase
ageofheroes-setup-start = Vous êtes le chef de la tribu des { $tribe }. Votre ressource spéciale de monument est { $special }. Lancez les dés pour déterminer l'ordre de jeu.
ageofheroes-setup-viewer = Les joueurs lancent les dés pour déterminer l'ordre de jeu.
ageofheroes-roll-dice = Lancer les dés
ageofheroes-war-roll-dice = Lancer les dés
ageofheroes-dice-result = Vous avez obtenu { $total } ({ $die1 } + { $die2 }).
ageofheroes-dice-result-other = { $player } a obtenu { $total }.
ageofheroes-dice-tie = Plusieurs joueurs sont à égalité avec { $total }. Nouveau lancer...
ageofheroes-first-player = { $player } a obtenu le score le plus élevé avec { $total } et commence.
ageofheroes-first-player-you = Avec { $total } points, vous commencez.

# Preparation phase
ageofheroes-prepare-start = Les joueurs doivent jouer les cartes événement et défausser les catastrophes.
ageofheroes-prepare-your-turn = Vous avez { $count } { $count ->
    [0] carte
    [1] carte
    *[other] cartes
} à jouer ou défausser.
ageofheroes-prepare-done = Phase de préparation terminée.

# Events played/discarded
ageofheroes-population-growth = { $player } joue Croissance de Population et construit une nouvelle cité.
ageofheroes-population-growth-you = Vous jouez Croissance de Population et construisez une nouvelle cité.
ageofheroes-discard-card = { $player } défausse { $card }.
ageofheroes-discard-card-you = Vous défaussez { $card }.
ageofheroes-earthquake = Un tremblement de terre frappe la tribu de { $player } ; ses armées entrent en convalescence.
ageofheroes-earthquake-you = Un tremblement de terre frappe votre tribu ; vos armées entrent en convalescence.
ageofheroes-eruption = Une éruption détruit l'une des cités de { $player }.
ageofheroes-eruption-you = Une éruption détruit l'une de vos cités.

# Disaster effects
ageofheroes-hunger-strikes = La famine frappe.
ageofheroes-lose-card-hunger = Vous perdez { $card }.
ageofheroes-barbarians-pillage = Les barbares attaquent les ressources de { $player }.
ageofheroes-barbarians-attack = Les barbares attaquent les ressources de { $player }.
ageofheroes-barbarians-attack-you = Les barbares attaquent vos ressources.
ageofheroes-lose-card-barbarians = Vous perdez { $card }.
ageofheroes-block-with-card = { $player } bloque la catastrophe en utilisant { $card }.
ageofheroes-block-with-card-you = Vous bloquez la catastrophe en utilisant { $card }.

# Targeted disaster cards (Earthquake/Eruption)
ageofheroes-select-disaster-target = Sélectionnez une cible pour { $card }.
ageofheroes-no-targets = Aucune cible valide disponible.
ageofheroes-earthquake-strikes-you = { $attacker } joue Tremblement de Terre contre vous. Vos armées sont désactivées.
ageofheroes-earthquake-strikes = { $attacker } joue Tremblement de Terre contre { $player }.
ageofheroes-armies-disabled = { $count } { $count ->
    [0] armée est
    [1] armée est
    *[other] armées sont
} désactivée(s) pour un tour.
ageofheroes-eruption-strikes-you = { $attacker } joue Éruption contre vous. L'une de vos cités est détruite.
ageofheroes-eruption-strikes = { $attacker } joue Éruption contre { $player }.
ageofheroes-city-destroyed = Une cité est détruite par l'éruption.

# Fair phase
ageofheroes-fair-start = Le jour se lève sur le marché.
ageofheroes-fair-draw-base = Vous piochez { $count } { $count ->
    [0] carte
    [1] carte
    *[other] cartes
}.
ageofheroes-fair-draw-roads = Vous piochez { $count } { $count ->
    [0] carte supplémentaire
    [1] carte supplémentaire
    *[other] cartes supplémentaires
} grâce à votre réseau routier.
ageofheroes-fair-draw-other = { $player } pioche { $count } { $count ->
    [0] carte
    [1] carte
    *[other] cartes
}.

# Trading/Auction
ageofheroes-auction-start = Les enchères commencent.
ageofheroes-offer-trade = Proposer un échange
ageofheroes-offer-made = { $player } propose { $card } contre { $wanted }.
ageofheroes-offer-made-you = Vous proposez { $card } contre { $wanted }.
ageofheroes-trade-accepted = { $player } accepte l'offre de { $other } et échange { $give } contre { $receive }.
ageofheroes-trade-accepted-you = Vous acceptez l'offre de { $other } et recevez { $receive }.
ageofheroes-trade-cancelled = { $player } retire son offre pour { $card }.
ageofheroes-trade-cancelled-you = Vous retirez votre offre pour { $card }.
ageofheroes-stop-trading = Arrêter les Échanges
ageofheroes-select-request = Vous proposez { $card }. Que voulez-vous en retour ?
ageofheroes-cancel = Annuler
ageofheroes-left-auction = { $player } quitte le marché.
ageofheroes-left-auction-you = Vous quittez le marché.
ageofheroes-any-card = N'importe quelle carte
ageofheroes-cannot-trade-own-special = Vous ne pouvez pas échanger votre propre ressource spéciale de monument.
ageofheroes-resource-not-in-game = Cette ressource spéciale n'est pas utilisée dans cette partie.

# Main play phase
ageofheroes-play-start = Phase de jeu.
ageofheroes-day = Jour { $day }
ageofheroes-draw-card = { $player } pioche une carte du paquet.
ageofheroes-draw-card-you = Vous piochez { $card } du paquet.
ageofheroes-your-action = Que voulez-vous faire ?

# Tax Collection
ageofheroes-tax-collection = { $player } choisit Collecte d'Impôts : { $cities } { $cities ->
    [0] cité
    [1] cité
    *[other] cités
} collecte { $cards } { $cards ->
    [0] carte
    [1] carte
    *[other] cartes
}.
ageofheroes-tax-collection-you = Vous choisissez Collecte d'Impôts : { $cities } { $cities ->
    [0] cité
    [1] cité
    *[other] cités
} collecte { $cards } { $cards ->
    [0] carte
    [1] carte
    *[other] cartes
}.
ageofheroes-tax-no-city = Collecte d'Impôts : Vous n'avez aucune cité survivante. Défaussez une carte pour en piocher une nouvelle.
ageofheroes-tax-no-city-done = { $player } choisit Collecte d'Impôts mais n'a aucune cité, il échange donc une carte.
ageofheroes-tax-no-city-done-you = Collecte d'Impôts : Vous avez échangé { $card } contre une nouvelle carte.

# Construction
ageofheroes-construction-menu = Que voulez-vous construire ?
ageofheroes-construction-done = { $player } a construit { $article } { $building }.
ageofheroes-construction-done-you = Vous avez construit { $article } { $building }.
ageofheroes-construction-stop = Arrêter la construction
ageofheroes-construction-stopped = Vous avez décidé d'arrêter la construction.
ageofheroes-road-select-neighbor = Sélectionnez le voisin vers lequel construire une route.
ageofheroes-direction-left = À votre gauche
ageofheroes-direction-right = À votre droite
ageofheroes-road-request-sent = Demande de route envoyée. En attente de l'approbation du voisin.
ageofheroes-road-request-received = { $requester } demande la permission de construire une route vers votre tribu.
ageofheroes-road-request-denied-you = Vous avez refusé la demande de route.
ageofheroes-road-request-denied = { $denier } a refusé votre demande de route.
ageofheroes-road-built = { $tribe1 } et { $tribe2 } sont maintenant connectés par une route.
ageofheroes-road-no-target = Aucune tribu voisine disponible pour la construction de route.
ageofheroes-approve = Approuver
ageofheroes-deny = Refuser
ageofheroes-supply-exhausted = Plus de { $building } disponibles à construire.

# Do Nothing
ageofheroes-do-nothing = { $player } passe son tour.
ageofheroes-do-nothing-you = Vous passez votre tour...

# War
ageofheroes-war-declare = { $attacker } déclare la guerre à { $defender }. Objectif : { $goal }.
ageofheroes-war-prepare = Sélectionnez vos armées pour { $action }.
ageofheroes-war-no-army = Vous n'avez aucune armée ou carte héros disponible.
ageofheroes-war-no-targets = Aucune cible valide pour la guerre.
ageofheroes-war-no-valid-goal = Aucun objectif de guerre valide contre cette cible.
ageofheroes-war-select-target = Sélectionnez le joueur à attaquer.
ageofheroes-war-select-goal = Sélectionnez votre objectif de guerre.
ageofheroes-war-prepare-attack = Sélectionnez vos forces d'attaque.
ageofheroes-war-prepare-defense = { $attacker } vous attaque ; Sélectionnez vos forces de défense.
ageofheroes-war-select-armies = Sélectionner les armées : { $count }
ageofheroes-war-select-generals = Sélectionner les généraux : { $count }
ageofheroes-war-select-heroes = Sélectionner les héros : { $count }
ageofheroes-war-attack = Attaquer...
ageofheroes-war-defend = Défendre...
ageofheroes-war-prepared = Vos forces : { $armies } { $armies ->
    [0] armée
    [1] armée
    *[other] armées
}{ $generals ->
    [0] {""}
    [1] {" et 1 général"}
    *[other] {" et { $generals } généraux"}
}{ $heroes ->
    [0] {""}
    [1] {" et 1 héros"}
    *[other] {" et { $heroes } héros"}
}.
ageofheroes-war-roll-you = Vous obtenez { $roll }.
ageofheroes-war-roll-other = { $player } obtient { $roll }.
ageofheroes-war-bonuses-you = { $general ->
    [0] { $fortress ->
        [0] {""}
        [1] +1 de forteresse = { $total } total
        *[other] +{ $fortress } de forteresses = { $total } total
    }
    *[other] { $fortress ->
        [0] +{ $general } de général = { $total } total
        [1] +{ $general } de général, +1 de forteresse = { $total } total
        *[other] +{ $general } de général, +{ $fortress } de forteresses = { $total } total
    }
}
ageofheroes-war-bonuses-other = { $general ->
    [0] { $fortress ->
        [0] {""}
        [1] { $player } : +1 de forteresse = { $total } total
        *[other] { $player } : +{ $fortress } de forteresses = { $total } total
    }
    *[other] { $fortress ->
        [0] { $player } : +{ $general } de général = { $total } total
        [1] { $player } : +{ $general } de général, +1 de forteresse = { $total } total
        *[other] { $player } : +{ $general } de général, +{ $fortress } de forteresses = { $total } total
    }
}

# Battle
ageofheroes-battle-start = La bataille commence. { $attacker } avec { $att_armies } { $att_armies ->
    [0] armée
    [1] armée
    *[other] armées
} contre { $defender } avec { $def_armies } { $def_armies ->
    [0] armée
    [1] armée
    *[other] armées
}.
ageofheroes-dice-roll-detailed = { $name } obtient { $dice }{ $general ->
    [0] {""}
    *[other] { " + { $general } de général" }
}{ $fortress ->
    [0] {""}
    [1] { " + 1 de forteresse" }
    *[other] { " + { $fortress } de forteresses" }
} = { $total }.
ageofheroes-dice-roll-detailed-you = Vous obtenez { $dice }{ $general ->
    [0] {""}
    *[other] { " + { $general } de général" }
}{ $fortress ->
    [0] {""}
    [1] { " + 1 de forteresse" }
    *[other] { " + { $fortress } de forteresses" }
} = { $total }.
ageofheroes-round-attacker-wins = { $attacker } gagne le round ({ $att_total } contre { $def_total }). { $defender } perd une armée.
ageofheroes-round-defender-wins = { $defender } défend avec succès ({ $def_total } contre { $att_total }). { $attacker } perd une armée.
ageofheroes-round-draw = Les deux camps sont à égalité à { $total }. Aucune armée perdue.
ageofheroes-battle-victory-attacker = { $attacker } vainc { $defender }.
ageofheroes-battle-victory-defender = { $defender } défend avec succès contre { $attacker }.
ageofheroes-battle-mutual-defeat = { $attacker } et { $defender } perdent toutes leurs armées.
ageofheroes-general-bonus = +{ $count } de { $count ->
    [0] général
    [1] général
    *[other] généraux
}
ageofheroes-fortress-bonus = +{ $count } de défense de forteresse
ageofheroes-battle-winner = { $winner } remporte la bataille.
ageofheroes-battle-draw = La bataille se termine par un match nul...
ageofheroes-battle-continue = Continuer la bataille.
ageofheroes-battle-end = La bataille est terminée.

# War outcomes
ageofheroes-conquest-success = { $attacker } conquiert { $count } { $count ->
    [0] cité
    [1] cité
    *[other] cités
} de { $defender }.
ageofheroes-plunder-success = { $attacker } pille { $count } { $count ->
    [0] carte
    [1] carte
    *[other] cartes
} de { $defender }.
ageofheroes-destruction-success = { $attacker } détruit { $count } { $count ->
    [0] ressource
    [1] ressource
    *[other] ressources
} de monument de { $defender }.
ageofheroes-army-losses = { $player } perd { $count } { $count ->
    [0] armée
    [1] armée
    *[other] armées
}.
ageofheroes-army-losses-you = Vous perdez { $count } { $count ->
    [0] armée
    [1] armée
    *[other] armées
}.

# Army return
ageofheroes-army-return-road = Vos troupes reviennent immédiatement par la route.
ageofheroes-army-return-delayed = { $count } { $count ->
    [0] unité revient
    [1] unité revient
    *[other] unités reviennent
} à la fin de votre prochain tour.
ageofheroes-army-returned = Les troupes de { $player } sont revenues de la guerre.
ageofheroes-army-returned-you = Vos troupes sont revenues de la guerre.
ageofheroes-army-recover = Les armées de { $player } se remettent du tremblement de terre.
ageofheroes-army-recover-you = Vos armées se remettent du tremblement de terre.

# Olympics
ageofheroes-olympics-cancel = { $player } joue Jeux Olympiques. Guerre annulée.
ageofheroes-olympics-prompt = { $attacker } a déclaré la guerre. Vous avez les Jeux Olympiques - l'utiliser pour annuler ?
ageofheroes-yes = Oui
ageofheroes-no = Non

# Monument progress
ageofheroes-monument-progress = Le monument de { $player } est { $count }/5 complet.
ageofheroes-monument-progress-you = Votre monument est { $count }/5 complet.

# Hand management
ageofheroes-discard-excess = Vous avez plus de { $max } cartes. Défaussez { $count } { $count ->
    [0] carte
    [1] carte
    *[other] cartes
}.
ageofheroes-discard-excess-other = { $player } doit défausser des cartes en excès.
ageofheroes-discard-more = Défaussez encore { $count } { $count ->
    [0] carte
    [1] carte
    *[other] cartes
}.

# Victory
ageofheroes-victory-cities = { $player } a construit 5 cités ! Empire des Cinq Cités.
ageofheroes-victory-cities-you = Vous avez construit 5 cités ! Empire des Cinq Cités.
ageofheroes-victory-monument = { $player } a achevé son monument ! Porteurs de Grande Culture.
ageofheroes-victory-monument-you = Vous avez achevé votre monument ! Porteurs de Grande Culture.
ageofheroes-victory-last-standing = { $player } est la dernière tribu debout ! Le Plus Persévérant.
ageofheroes-victory-last-standing-you = Vous êtes la dernière tribu debout ! Le Plus Persévérant.
ageofheroes-game-over = Partie terminée.

# Elimination
ageofheroes-eliminated = { $player } a été éliminé.
ageofheroes-eliminated-you = Vous avez été éliminé.

# Hand
ageofheroes-hand-empty = Vous n'avez aucune carte.
ageofheroes-hand-contents = Votre main ({ $count } { $count ->
    [0] carte
    [1] carte
    *[other] cartes
}) : { $cards }

# Status
ageofheroes-status = { $player } ({ $tribe }) : { $cities } { $cities ->
    [0] cité
    [1] cité
    *[other] cités
}, { $armies } { $armies ->
    [0] armée
    [1] armée
    *[other] armées
}, { $monument }/5 monument
ageofheroes-status-detailed-header = { $player } ({ $tribe })
ageofheroes-status-cities = Cités : { $count }
ageofheroes-status-armies = Armées : { $count }
ageofheroes-status-generals = Généraux : { $count }
ageofheroes-status-fortresses = Forteresses : { $count }
ageofheroes-status-monument = Monument : { $count }/5
ageofheroes-status-roads = Routes : { $left }{ $right }
ageofheroes-status-road-left = gauche
ageofheroes-status-road-right = droite
ageofheroes-status-none = aucune
ageofheroes-status-earthquake-armies = Armées en convalescence : { $count }
ageofheroes-status-returning-armies = Armées de retour : { $count }
ageofheroes-status-returning-generals = Généraux de retour : { $count }

# Deck info
ageofheroes-deck-empty = Plus de cartes { $card } dans le paquet.
ageofheroes-deck-count = Cartes restantes : { $count }
ageofheroes-deck-reshuffled = La défausse a été mélangée dans le paquet.

# Give up
ageofheroes-give-up-confirm = Êtes-vous sûr de vouloir abandonner ?
ageofheroes-gave-up = { $player } a abandonné !
ageofheroes-gave-up-you = Vous avez abandonné !

# Hero card
ageofheroes-hero-use = Utiliser comme armée ou général ?
ageofheroes-hero-army = Armée
ageofheroes-hero-general = Général

# Fortune card
ageofheroes-fortune-reroll = { $player } utilise Fortune pour relancer.
ageofheroes-fortune-prompt = Vous avez perdu le lancer. Utiliser Fortune pour relancer ?

# Disabled action reasons
ageofheroes-not-your-turn = Ce n'est pas votre tour.
ageofheroes-game-not-started = La partie n'a pas encore commencé.
ageofheroes-wrong-phase = Cette action n'est pas disponible dans la phase actuelle.
ageofheroes-no-resources = Vous n'avez pas les ressources requises.

# Building costs (for display)
ageofheroes-cost-army = 2 Blé, Fer
ageofheroes-cost-fortress = Fer, Bois, Pierre
ageofheroes-cost-general = Fer, Or
ageofheroes-cost-road = 2 Pierre
ageofheroes-cost-city = 2 Bois, Pierre
