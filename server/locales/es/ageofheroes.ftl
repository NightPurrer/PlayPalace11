# Age of Heroes game messages
# A civilization-building card game for 2-6 players

# Game name
game-name-ageofheroes = Age of Heroes

# Tribes
ageofheroes-tribe-egyptians = Egipcios
ageofheroes-tribe-romans = Romanos
ageofheroes-tribe-greeks = Griegos
ageofheroes-tribe-babylonians = Babilonios
ageofheroes-tribe-celts = Celtas
ageofheroes-tribe-chinese = Chinos

# Special Resources (for monuments)
ageofheroes-special-limestone = Caliza
ageofheroes-special-concrete = Hormigón
ageofheroes-special-marble = Mármol
ageofheroes-special-bricks = Ladrillos
ageofheroes-special-sandstone = Arenisca
ageofheroes-special-granite = Granito

# Standard Resources
ageofheroes-resource-iron = Hierro
ageofheroes-resource-wood = Madera
ageofheroes-resource-grain = Grano
ageofheroes-resource-stone = Piedra
ageofheroes-resource-gold = Oro

# Events
ageofheroes-event-population-growth = Crecimiento de Población
ageofheroes-event-earthquake = Terremoto
ageofheroes-event-eruption = Erupción
ageofheroes-event-hunger = Hambre
ageofheroes-event-barbarians = Bárbaros
ageofheroes-event-olympics = Juegos Olímpicos
ageofheroes-event-hero = Héroe
ageofheroes-event-fortune = Fortuna

# Buildings
ageofheroes-building-army = Ejército
ageofheroes-building-fortress = Fortaleza
ageofheroes-building-general = General
ageofheroes-building-road = Carretera
ageofheroes-building-city = Ciudad

# Actions
ageofheroes-action-tax-collection = Recaudación de Impuestos
ageofheroes-action-construction = Construcción
ageofheroes-action-war = Guerra
ageofheroes-action-do-nothing = No Hacer Nada
ageofheroes-play = Jugar

# War goals
ageofheroes-war-conquest = Conquista
ageofheroes-war-plunder = Saqueo
ageofheroes-war-destruction = Destrucción

# Game options
ageofheroes-set-victory-cities = Ciudades para victoria: { $cities }
ageofheroes-enter-victory-cities = Ingresa el número de ciudades para ganar (3-7)
ageofheroes-set-victory-monument = Finalización del monumento: { $progress }%
ageofheroes-toggle-neighbor-roads = Carreteras solo a vecinos: { $enabled }
ageofheroes-set-max-hand = Tamaño máximo de mano: { $cards } cartas

# Option change announcements
ageofheroes-option-changed-victory-cities = La victoria requiere { $cities } ciudades.
ageofheroes-option-changed-victory-monument = Umbral de finalización del monumento establecido en { $progress }%.
ageofheroes-option-changed-neighbor-roads = Carreteras solo a vecinos { $enabled }.
ageofheroes-option-changed-max-hand = Tamaño máximo de mano establecido en { $cards } cartas.

# Setup phase
ageofheroes-setup-start = Eres el líder de la tribu { $tribe }. Tu recurso especial para monumentos es { $special }. Tira los dados para determinar el orden de turno.
ageofheroes-setup-viewer = Los jugadores están tirando dados para determinar el orden de turno.
ageofheroes-roll-dice = Tira los dados
ageofheroes-war-roll-dice = Tira los dados
ageofheroes-dice-result = Sacaste { $total } ({ $die1 } + { $die2 }).
ageofheroes-dice-result-other = { $player } sacó { $total }.
ageofheroes-dice-tie = Varios jugadores empataron con { $total }. Tirando de nuevo...
ageofheroes-first-player = { $player } sacó el más alto con { $total } y va primero.
ageofheroes-first-player-you = Con { $total } puntos, vas primero.

# Preparation phase
ageofheroes-prepare-start = Los jugadores deben jugar cartas de evento y descartar desastres.
ageofheroes-prepare-your-turn = Tienes { $count } { $count ->
    [one] carta
    *[other] cartas
} para jugar o descartar.
ageofheroes-prepare-done = Fase de preparación completa.

# Events played/discarded
ageofheroes-population-growth = { $player } juega Crecimiento de Población y construye una nueva ciudad.
ageofheroes-population-growth-you = Juegas Crecimiento de Población y construyes una nueva ciudad.
ageofheroes-discard-card = { $player } descarta { $card }.
ageofheroes-discard-card-you = Descartas { $card }.
ageofheroes-earthquake = Un terremoto golpea la tribu de { $player }; sus ejércitos entran en recuperación.
ageofheroes-earthquake-you = Un terremoto golpea tu tribu; tus ejércitos entran en recuperación.
ageofheroes-eruption = Una erupción destruye una de las ciudades de { $player }.
ageofheroes-eruption-you = Una erupción destruye una de tus ciudades.

# Disaster effects
ageofheroes-hunger-strikes = El hambre golpea.
ageofheroes-lose-card-hunger = Pierdes { $card }.
ageofheroes-barbarians-pillage = Los bárbaros atacan los recursos de { $player }.
ageofheroes-barbarians-attack = Los bárbaros atacan los recursos de { $player }.
ageofheroes-barbarians-attack-you = Los bárbaros atacan tus recursos.
ageofheroes-lose-card-barbarians = Pierdes { $card }.
ageofheroes-block-with-card = { $player } bloquea el desastre usando { $card }.
ageofheroes-block-with-card-you = Bloqueas el desastre usando { $card }.

# Targeted disaster cards (Earthquake/Eruption)
ageofheroes-select-disaster-target = Selecciona un objetivo para { $card }.
ageofheroes-no-targets = No hay objetivos válidos disponibles.
ageofheroes-earthquake-strikes-you = { $attacker } juega Terremoto contra ti. Tus ejércitos están deshabilitados.
ageofheroes-earthquake-strikes = { $attacker } juega Terremoto contra { $player }.
ageofheroes-armies-disabled = { $count } { $count ->
    [one] ejército está
    *[other] ejércitos están
} deshabilitados por un turno.
ageofheroes-eruption-strikes-you = { $attacker } juega Erupción contra ti. Una de tus ciudades es destruida.
ageofheroes-eruption-strikes = { $attacker } juega Erupción contra { $player }.
ageofheroes-city-destroyed = Una ciudad es destruida por la erupción.

# Fair phase
ageofheroes-fair-start = Amanece en el mercado.
ageofheroes-fair-draw-base = Robas { $count } { $count ->
    [one] carta
    *[other] cartas
}.
ageofheroes-fair-draw-roads = Robas { $count } { $count ->
    [one] carta adicional
    *[other] cartas adicionales
} gracias a tu red de carreteras.
ageofheroes-fair-draw-other = { $player } roba { $count } { $count ->
    [one] carta
    *[other] cartas
}.

# Trading/Auction
ageofheroes-auction-start = Comienza la subasta.
ageofheroes-offer-trade = Ofrecer intercambio
ageofheroes-offer-made = { $player } ofrece { $card } por { $wanted }.
ageofheroes-offer-made-you = Ofreces { $card } por { $wanted }.
ageofheroes-trade-accepted = { $player } acepta la oferta de { $other } e intercambia { $give } por { $receive }.
ageofheroes-trade-accepted-you = Aceptas la oferta de { $other } y recibes { $receive }.
ageofheroes-trade-cancelled = { $player } retira su oferta por { $card }.
ageofheroes-trade-cancelled-you = Retiras tu oferta por { $card }.
ageofheroes-stop-trading = Dejar de Intercambiar
ageofheroes-select-request = Estás ofreciendo { $card }. ¿Qué quieres a cambio?
ageofheroes-cancel = Cancelar
ageofheroes-left-auction = { $player } se va.
ageofheroes-left-auction-you = Te vas del mercado.
ageofheroes-any-card = Cualquier carta
ageofheroes-cannot-trade-own-special = No puedes intercambiar tu propio recurso especial para monumentos.
ageofheroes-resource-not-in-game = Este recurso especial no se está usando en este juego.

# Main play phase
ageofheroes-play-start = Fase de juego.
ageofheroes-day = Día { $day }
ageofheroes-draw-card = { $player } roba una carta del mazo.
ageofheroes-draw-card-you = Robas { $card } del mazo.
ageofheroes-your-action = ¿Qué quieres hacer?

# Tax Collection
ageofheroes-tax-collection = { $player } elige Recaudación de Impuestos: { $cities } { $cities ->
    [one] ciudad
    *[other] ciudades
} recauda { $cards } { $cards ->
    [one] carta
    *[other] cartas
}.
ageofheroes-tax-collection-you = Eliges Recaudación de Impuestos: { $cities } { $cities ->
    [one] ciudad
    *[other] ciudades
} recauda { $cards } { $cards ->
    [one] carta
    *[other] cartas
}.
ageofheroes-tax-no-city = Recaudación de Impuestos: No tienes ciudades sobrevivientes. Descarta una carta para robar una nueva.
ageofheroes-tax-no-city-done = { $player } elige Recaudación de Impuestos pero no tiene ciudades, así que intercambia una carta.
ageofheroes-tax-no-city-done-you = Recaudación de Impuestos: Intercambiaste { $card } por una carta nueva.

# Construction
ageofheroes-construction-menu = ¿Qué quieres construir?
ageofheroes-construction-done = { $player } construyó { $article } { $building }.
ageofheroes-construction-done-you = Construiste { $article } { $building }.
ageofheroes-construction-stop = Dejar de construir
ageofheroes-construction-stopped = Decidiste dejar de construir.
ageofheroes-road-select-neighbor = Selecciona a qué vecino construir una carretera.
ageofheroes-direction-left = A tu izquierda
ageofheroes-direction-right = A tu derecha
ageofheroes-road-request-sent = Solicitud de carretera enviada. Esperando aprobación del vecino.
ageofheroes-road-request-received = { $requester } solicita permiso para construir una carretera a tu tribu.
ageofheroes-road-request-denied-you = Rechazaste la solicitud de carretera.
ageofheroes-road-request-denied = { $denier } rechazó tu solicitud de carretera.
ageofheroes-road-built = { $tribe1 } y { $tribe2 } están ahora conectados por carretera.
ageofheroes-road-no-target = No hay tribus vecinas disponibles para construcción de carretera.
ageofheroes-approve = Aprobar
ageofheroes-deny = Rechazar
ageofheroes-supply-exhausted = No hay más { $building } disponibles para construir.

# Do Nothing
ageofheroes-do-nothing = { $player } pasa.
ageofheroes-do-nothing-you = Pasas...

# War
ageofheroes-war-declare = { $attacker } declara la guerra a { $defender }. Objetivo: { $goal }.
ageofheroes-war-prepare = Selecciona tus ejércitos para { $action }.
ageofheroes-war-no-army = No tienes ejércitos o cartas de héroe disponibles.
ageofheroes-war-no-targets = No hay objetivos válidos para guerra.
ageofheroes-war-no-valid-goal = No hay objetivos de guerra válidos contra este objetivo.
ageofheroes-war-select-target = Selecciona a qué jugador atacar.
ageofheroes-war-select-goal = Selecciona tu objetivo de guerra.
ageofheroes-war-prepare-attack = Selecciona tus fuerzas atacantes.
ageofheroes-war-prepare-defense = { $attacker } te está atacando; Selecciona tus fuerzas defensoras.
ageofheroes-war-select-armies = Selecciona ejércitos: { $count }
ageofheroes-war-select-generals = Selecciona generales: { $count }
ageofheroes-war-select-heroes = Selecciona héroes: { $count }
ageofheroes-war-attack = Atacar...
ageofheroes-war-defend = Defender...
ageofheroes-war-prepared = Tus fuerzas: { $armies } { $armies ->
    [one] ejército
    *[other] ejércitos
}{ $generals ->
    [0] {""}
    [one] {" y 1 general"}
    *[other] {" y { $generals } generales"}
}{ $heroes ->
    [0] {""}
    [one] {" y 1 héroe"}
    *[other] {" y { $heroes } héroes"}
}.
ageofheroes-war-roll-you = Sacas { $roll }.
ageofheroes-war-roll-other = { $player } saca { $roll }.
ageofheroes-war-bonuses-you = { $general ->
    [0] { $fortress ->
        [0] {""}
        [one] +1 de fortaleza = { $total } total
        *[other] +{ $fortress } de fortalezas = { $total } total
    }
    *[other] { $fortress ->
        [0] +{ $general } de general = { $total } total
        [one] +{ $general } de general, +1 de fortaleza = { $total } total
        *[other] +{ $general } de general, +{ $fortress } de fortalezas = { $total } total
    }
}
ageofheroes-war-bonuses-other = { $general ->
    [0] { $fortress ->
        [0] {""}
        [one] { $player }: +1 de fortaleza = { $total } total
        *[other] { $player }: +{ $fortress } de fortalezas = { $total } total
    }
    *[other] { $fortress ->
        [0] { $player }: +{ $general } de general = { $total } total
        [one] { $player }: +{ $general } de general, +1 de fortaleza = { $total } total
        *[other] { $player }: +{ $general } de general, +{ $fortress } de fortalezas = { $total } total
    }
}

# Battle
ageofheroes-battle-start = Comienza la batalla. { $att_armies } { $att_armies ->
    [one] ejército
    *[other] ejércitos
} de { $attacker } contra { $def_armies } { $def_armies ->
    [one] ejército
    *[other] ejércitos
} de { $defender }.
ageofheroes-dice-roll-detailed = { $name } saca { $dice }{ $general ->
    [0] {""}
    *[other] { " + { $general } de general" }
}{ $fortress ->
    [0] {""}
    [one] { " + 1 de fortaleza" }
    *[other] { " + { $fortress } de fortalezas" }
} = { $total }.
ageofheroes-dice-roll-detailed-you = Sacas { $dice }{ $general ->
    [0] {""}
    *[other] { " + { $general } de general" }
}{ $fortress ->
    [0] {""}
    [one] { " + 1 de fortaleza" }
    *[other] { " + { $fortress } de fortalezas" }
} = { $total }.
ageofheroes-round-attacker-wins = { $attacker } gana la ronda ({ $att_total } vs { $def_total }). { $defender } pierde un ejército.
ageofheroes-round-defender-wins = { $defender } se defiende exitosamente ({ $def_total } vs { $att_total }). { $attacker } pierde un ejército.
ageofheroes-round-draw = Ambos lados empatan en { $total }. No se pierden ejércitos.
ageofheroes-battle-victory-attacker = { $attacker } derrota a { $defender }.
ageofheroes-battle-victory-defender = { $defender } se defiende exitosamente contra { $attacker }.
ageofheroes-battle-mutual-defeat = Tanto { $attacker } como { $defender } pierden todos sus ejércitos.
ageofheroes-general-bonus = +{ $count } de { $count ->
    [one] general
    *[other] generales
}
ageofheroes-fortress-bonus = +{ $count } de defensa de fortaleza
ageofheroes-battle-winner = { $winner } gana la batalla.
ageofheroes-battle-draw = La batalla termina en empate...
ageofheroes-battle-continue = Continuar la batalla.
ageofheroes-battle-end = La batalla ha terminado.

# War outcomes
ageofheroes-conquest-success = { $attacker } conquista { $count } { $count ->
    [one] ciudad
    *[other] ciudades
} de { $defender }.
ageofheroes-plunder-success = { $attacker } saquea { $count } { $count ->
    [one] carta
    *[other] cartas
} de { $defender }.
ageofheroes-destruction-success = { $attacker } destruye { $count } { $count ->
    [one] recurso
    *[other] recursos
} del monumento de { $defender }.
ageofheroes-army-losses = { $player } pierde { $count } { $count ->
    [one] ejército
    *[other] ejércitos
}.
ageofheroes-army-losses-you = Pierdes { $count } { $count ->
    [one] ejército
    *[other] ejércitos
}.

# Army return
ageofheroes-army-return-road = Tus tropas regresan inmediatamente por carretera.
ageofheroes-army-return-delayed = { $count } { $count ->
    [one] unidad regresa
    *[other] unidades regresan
} al final de tu próximo turno.
ageofheroes-army-returned = Las tropas de { $player } han regresado de la guerra.
ageofheroes-army-returned-you = Tus tropas han regresado de la guerra.
ageofheroes-army-recover = Los ejércitos de { $player } se recuperan del terremoto.
ageofheroes-army-recover-you = Tus ejércitos se recuperan del terremoto.

# Olympics
ageofheroes-olympics-cancel = { $player } juega Juegos Olímpicos. Guerra cancelada.
ageofheroes-olympics-prompt = { $attacker } ha declarado la guerra. Tienes Juegos Olímpicos - ¿usarlos para cancelar?
ageofheroes-yes = Sí
ageofheroes-no = No

# Monument progress
ageofheroes-monument-progress = El monumento de { $player } está { $count }/5 completo.
ageofheroes-monument-progress-you = Tu monumento está { $count }/5 completo.

# Hand management
ageofheroes-discard-excess = Tienes más de { $max } cartas. Descarta { $count } { $count ->
    [one] carta
    *[other] cartas
}.
ageofheroes-discard-excess-other = { $player } debe descartar cartas en exceso.
ageofheroes-discard-more = Descarta { $count } { $count ->
    [one] carta más
    *[other] cartas más
}.

# Victory
ageofheroes-victory-cities = ¡{ $player } ha construido 5 ciudades! Imperio de Cinco Ciudades.
ageofheroes-victory-cities-you = ¡Has construido 5 ciudades! Imperio de Cinco Ciudades.
ageofheroes-victory-monument = ¡{ $player } ha completado su monumento! Portadores de Gran Cultura.
ageofheroes-victory-monument-you = ¡Has completado tu monumento! Portadores de Gran Cultura.
ageofheroes-victory-last-standing = ¡{ $player } es la última tribu en pie! El Más Persistente.
ageofheroes-victory-last-standing-you = ¡Eres la última tribu en pie! El Más Persistente.
ageofheroes-game-over = Juego Terminado.

# Elimination
ageofheroes-eliminated = { $player } ha sido eliminado.
ageofheroes-eliminated-you = Has sido eliminado.

# Hand
ageofheroes-hand-empty = No tienes cartas.
ageofheroes-hand-contents = Tu mano ({ $count } { $count ->
    [one] carta
    *[other] cartas
}): { $cards }

# Status
ageofheroes-status = { $player } ({ $tribe }): { $cities } { $cities ->
    [one] ciudad
    *[other] ciudades
}, { $armies } { $armies ->
    [one] ejército
    *[other] ejércitos
}, { $monument }/5 monumento
ageofheroes-status-detailed-header = { $player } ({ $tribe })
ageofheroes-status-cities = Ciudades: { $count }
ageofheroes-status-armies = Ejércitos: { $count }
ageofheroes-status-generals = Generales: { $count }
ageofheroes-status-fortresses = Fortalezas: { $count }
ageofheroes-status-monument = Monumento: { $count }/5
ageofheroes-status-roads = Carreteras: { $left }{ $right }
ageofheroes-status-road-left = izquierda
ageofheroes-status-road-right = derecha
ageofheroes-status-none = ninguno
ageofheroes-status-earthquake-armies = Ejércitos en recuperación: { $count }
ageofheroes-status-returning-armies = Ejércitos que regresan: { $count }
ageofheroes-status-returning-generals = Generales que regresan: { $count }

# Deck info
ageofheroes-deck-empty = No hay más cartas de { $card } en el mazo.
ageofheroes-deck-count = Cartas restantes: { $count }
ageofheroes-deck-reshuffled = La pila de descarte ha sido barajada de vuelta al mazo.

# Give up
ageofheroes-give-up-confirm = ¿Estás seguro de que quieres rendirte?
ageofheroes-gave-up = ¡{ $player } se rindió!
ageofheroes-gave-up-you = ¡Te rendiste!

# Hero card
ageofheroes-hero-use = ¿Usar como ejército o general?
ageofheroes-hero-army = Ejército
ageofheroes-hero-general = General

# Fortune card
ageofheroes-fortune-reroll = { $player } usa Fortuna para volver a tirar.
ageofheroes-fortune-prompt = Perdiste la tirada. ¿Usar Fortuna para volver a tirar?

# Disabled action reasons
ageofheroes-not-your-turn = No es tu turno.
ageofheroes-game-not-started = El juego no ha comenzado aún.
ageofheroes-wrong-phase = Esta acción no está disponible en la fase actual.
ageofheroes-no-resources = No tienes los recursos requeridos.

# Building costs (for display)
ageofheroes-cost-army = 2 Grano, Hierro
ageofheroes-cost-fortress = Hierro, Madera, Piedra
ageofheroes-cost-general = Hierro, Oro
ageofheroes-cost-road = 2 Piedra
ageofheroes-cost-city = 2 Madera, Piedra
