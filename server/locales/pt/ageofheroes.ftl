# Age of Heroes game messages
# A civilization-building card game for 2-6 players

# Game name
game-name-ageofheroes = Era dos Heróis

# Tribes
ageofheroes-tribe-egyptians = Egípcios
ageofheroes-tribe-romans = Romanos
ageofheroes-tribe-greeks = Gregos
ageofheroes-tribe-babylonians = Babilônios
ageofheroes-tribe-celts = Celtas
ageofheroes-tribe-chinese = Chineses

# Special Resources (for monuments)
ageofheroes-special-limestone = Calcário
ageofheroes-special-concrete = Concreto
ageofheroes-special-marble = Mármore
ageofheroes-special-bricks = Tijolos
ageofheroes-special-sandstone = Arenito
ageofheroes-special-granite = Granito

# Standard Resources
ageofheroes-resource-iron = Ferro
ageofheroes-resource-wood = Madeira
ageofheroes-resource-grain = Grão
ageofheroes-resource-stone = Pedra
ageofheroes-resource-gold = Ouro

# Events
ageofheroes-event-population-growth = Crescimento Populacional
ageofheroes-event-earthquake = Terremoto
ageofheroes-event-eruption = Erupção
ageofheroes-event-hunger = Fome
ageofheroes-event-barbarians = Bárbaros
ageofheroes-event-olympics = Jogos Olímpicos
ageofheroes-event-hero = Herói
ageofheroes-event-fortune = Fortuna

# Buildings
ageofheroes-building-army = Exército
ageofheroes-building-fortress = Fortaleza
ageofheroes-building-general = General
ageofheroes-building-road = Estrada
ageofheroes-building-city = Cidade

# Actions
ageofheroes-action-tax-collection = Coleta de Impostos
ageofheroes-action-construction = Construção
ageofheroes-action-war = Guerra
ageofheroes-action-do-nothing = Não Fazer Nada
ageofheroes-play = Jogar

# War goals
ageofheroes-war-conquest = Conquista
ageofheroes-war-plunder = Pilhagem
ageofheroes-war-destruction = Destruição

# Game options
ageofheroes-set-victory-cities = Cidades da vitória: { $cities }
ageofheroes-enter-victory-cities = Digite o número de cidades para vencer (3-7)
ageofheroes-set-victory-monument = Conclusão do monumento: { $progress }%
ageofheroes-toggle-neighbor-roads = Estradas apenas para vizinhos: { $enabled }
ageofheroes-set-max-hand = Tamanho máximo da mão: { $cards } cartas

# Option change announcements
ageofheroes-option-changed-victory-cities = Vitória requer { $cities } cidades.
ageofheroes-option-changed-victory-monument = Limite de conclusão do monumento definido para { $progress }%.
ageofheroes-option-changed-neighbor-roads = Estradas apenas para vizinhos { $enabled }.
ageofheroes-option-changed-max-hand = Tamanho máximo da mão definido para { $cards } cartas.

# Setup phase
ageofheroes-setup-start = Você é o líder da tribo { $tribe }. Seu recurso especial de monumento é { $special }. Role os dados para determinar a ordem dos turnos.
ageofheroes-setup-viewer = Os jogadores estão rolando os dados para determinar a ordem dos turnos.
ageofheroes-roll-dice = Role os dados
ageofheroes-war-roll-dice = Role os dados
ageofheroes-dice-result = Você tirou { $total } ({ $die1 } + { $die2 }).
ageofheroes-dice-result-other = { $player } tirou { $total }.
ageofheroes-dice-tie = Vários jogadores empataram com { $total }. Rolando novamente...
ageofheroes-first-player = { $player } tirou o maior com { $total } e joga primeiro.
ageofheroes-first-player-you = Com { $total } pontos, você joga primeiro.

# Preparation phase
ageofheroes-prepare-start = Os jogadores devem jogar cartas de evento e descartar desastres.
ageofheroes-prepare-your-turn = Você tem { $count } { $count ->
    [one] carta
    *[other] cartas
} para jogar ou descartar.
ageofheroes-prepare-done = Fase de preparação concluída.

# Events played/discarded
ageofheroes-population-growth = { $player } joga Crescimento Populacional e constrói uma nova cidade.
ageofheroes-population-growth-you = Você joga Crescimento Populacional e constrói uma nova cidade.
ageofheroes-discard-card = { $player } descarta { $card }.
ageofheroes-discard-card-you = Você descarta { $card }.
ageofheroes-earthquake = Um terremoto atinge a tribo de { $player }; seus exércitos entram em recuperação.
ageofheroes-earthquake-you = Um terremoto atinge sua tribo; seus exércitos entram em recuperação.
ageofheroes-eruption = Uma erupção destrói uma das cidades de { $player }.
ageofheroes-eruption-you = Uma erupção destrói uma de suas cidades.

# Disaster effects
ageofheroes-hunger-strikes = A fome ataca.
ageofheroes-lose-card-hunger = Você perde { $card }.
ageofheroes-barbarians-pillage = Bárbaros atacam os recursos de { $player }.
ageofheroes-barbarians-attack = Bárbaros atacam os recursos de { $player }.
ageofheroes-barbarians-attack-you = Bárbaros atacam seus recursos.
ageofheroes-lose-card-barbarians = Você perde { $card }.
ageofheroes-block-with-card = { $player } bloqueia o desastre usando { $card }.
ageofheroes-block-with-card-you = Você bloqueia o desastre usando { $card }.

# Targeted disaster cards (Earthquake/Eruption)
ageofheroes-select-disaster-target = Selecione um alvo para { $card }.
ageofheroes-no-targets = Nenhum alvo válido disponível.
ageofheroes-earthquake-strikes-you = { $attacker } joga Terremoto contra você. Seus exércitos estão desativados.
ageofheroes-earthquake-strikes = { $attacker } joga Terremoto contra { $player }.
ageofheroes-armies-disabled = { $count } { $count ->
    [one] exército está
    *[other] exércitos estão
} desativados por um turno.
ageofheroes-eruption-strikes-you = { $attacker } joga Erupção contra você. Uma de suas cidades é destruída.
ageofheroes-eruption-strikes = { $attacker } joga Erupção contra { $player }.
ageofheroes-city-destroyed = Uma cidade é destruída pela erupção.

# Fair phase
ageofheroes-fair-start = O dia amanhece no mercado.
ageofheroes-fair-draw-base = Você compra { $count } { $count ->
    [one] carta
    *[other] cartas
}.
ageofheroes-fair-draw-roads = Você compra { $count } { $count ->
    [one] carta adicional
    *[other] cartas adicionais
} graças à sua rede de estradas.
ageofheroes-fair-draw-other = { $player } compra { $count } { $count ->
    [one] carta
    *[other] cartas
}.

# Trading/Auction
ageofheroes-auction-start = O leilão começa.
ageofheroes-offer-trade = Oferecer troca
ageofheroes-offer-made = { $player } oferece { $card } por { $wanted }.
ageofheroes-offer-made-you = Você oferece { $card } por { $wanted }.
ageofheroes-trade-accepted = { $player } aceita a oferta de { $other } e troca { $give } por { $receive }.
ageofheroes-trade-accepted-you = Você aceita a oferta de { $other } e recebe { $receive }.
ageofheroes-trade-cancelled = { $player } retira sua oferta por { $card }.
ageofheroes-trade-cancelled-you = Você retira sua oferta por { $card }.
ageofheroes-stop-trading = Parar de Negociar
ageofheroes-select-request = Você está oferecendo { $card }. O que você quer em troca?
ageofheroes-cancel = Cancelar
ageofheroes-left-auction = { $player } parte.
ageofheroes-left-auction-you = Você parte do mercado.
ageofheroes-any-card = Qualquer carta
ageofheroes-cannot-trade-own-special = Você não pode trocar seu próprio recurso especial de monumento.
ageofheroes-resource-not-in-game = Este recurso especial não está sendo usado neste jogo.

# Main play phase
ageofheroes-play-start = Fase de jogo.
ageofheroes-day = Dia { $day }
ageofheroes-draw-card = { $player } compra uma carta do baralho.
ageofheroes-draw-card-you = Você compra { $card } do baralho.
ageofheroes-your-action = O que você quer fazer?

# Tax Collection
ageofheroes-tax-collection = { $player } escolhe Coleta de Impostos: { $cities } { $cities ->
    [one] cidade
    *[other] cidades
} coletam { $cards } { $cards ->
    [one] carta
    *[other] cartas
}.
ageofheroes-tax-collection-you = Você escolhe Coleta de Impostos: { $cities } { $cities ->
    [one] cidade
    *[other] cidades
} coletam { $cards } { $cards ->
    [one] carta
    *[other] cartas
}.
ageofheroes-tax-no-city = Coleta de Impostos: Você não tem cidades sobreviventes. Descarte uma carta para comprar uma nova.
ageofheroes-tax-no-city-done = { $player } escolhe Coleta de Impostos, mas não tem cidades, então troca uma carta.
ageofheroes-tax-no-city-done-you = Coleta de Impostos: Você trocou { $card } por uma nova carta.

# Construction
ageofheroes-construction-menu = O que você quer construir?
ageofheroes-construction-done = { $player } construiu { $article } { $building }.
ageofheroes-construction-done-you = Você construiu { $article } { $building }.
ageofheroes-construction-stop = Parar de construir
ageofheroes-construction-stopped = Você decidiu parar de construir.
ageofheroes-road-select-neighbor = Selecione para qual vizinho construir uma estrada.
ageofheroes-direction-left = À sua esquerda
ageofheroes-direction-right = À sua direita
ageofheroes-road-request-sent = Pedido de estrada enviado. Aguardando aprovação do vizinho.
ageofheroes-road-request-received = { $requester } solicita permissão para construir uma estrada para sua tribo.
ageofheroes-road-request-denied-you = Você recusou o pedido de estrada.
ageofheroes-road-request-denied = { $denier } recusou seu pedido de estrada.
ageofheroes-road-built = { $tribe1 } e { $tribe2 } agora estão conectadas por estrada.
ageofheroes-road-no-target = Nenhuma tribo vizinha disponível para construção de estrada.
ageofheroes-approve = Aprovar
ageofheroes-deny = Recusar
ageofheroes-supply-exhausted = Não há mais { $building } disponível para construir.

# Do Nothing
ageofheroes-do-nothing = { $player } passa.
ageofheroes-do-nothing-you = Você passa...

# War
ageofheroes-war-declare = { $attacker } declara guerra a { $defender }. Objetivo: { $goal }.
ageofheroes-war-prepare = Selecione seus exércitos para { $action }.
ageofheroes-war-no-army = Você não tem exércitos ou cartas de herói disponíveis.
ageofheroes-war-no-targets = Nenhum alvo válido para guerra.
ageofheroes-war-no-valid-goal = Nenhum objetivo de guerra válido contra este alvo.
ageofheroes-war-select-target = Selecione qual jogador atacar.
ageofheroes-war-select-goal = Selecione seu objetivo de guerra.
ageofheroes-war-prepare-attack = Selecione suas forças de ataque.
ageofheroes-war-prepare-defense = { $attacker } está atacando você; Selecione suas forças de defesa.
ageofheroes-war-select-armies = Selecione exércitos: { $count }
ageofheroes-war-select-generals = Selecione generais: { $count }
ageofheroes-war-select-heroes = Selecione heróis: { $count }
ageofheroes-war-attack = Atacar...
ageofheroes-war-defend = Defender...
ageofheroes-war-prepared = Suas forças: { $armies } { $armies ->
    [one] exército
    *[other] exércitos
}{ $generals ->
    [0] {""}
    [one] {" e 1 general"}
    *[other] {" e { $generals } generais"}
}{ $heroes ->
    [0] {""}
    [one] {" e 1 herói"}
    *[other] {" e { $heroes } heróis"}
}.
ageofheroes-war-roll-you = Você tira { $roll }.
ageofheroes-war-roll-other = { $player } tira { $roll }.
ageofheroes-war-bonuses-you = { $general ->
    [0] { $fortress ->
        [0] {""}
        [1] +1 da fortaleza = { $total } total
        *[other] +{ $fortress } das fortalezas = { $total } total
    }
    *[other] { $fortress ->
        [0] +{ $general } do general = { $total } total
        [1] +{ $general } do general, +1 da fortaleza = { $total } total
        *[other] +{ $general } do general, +{ $fortress } das fortalezas = { $total } total
    }
}
ageofheroes-war-bonuses-other = { $general ->
    [0] { $fortress ->
        [0] {""}
        [1] { $player }: +1 da fortaleza = { $total } total
        *[other] { $player }: +{ $fortress } das fortalezas = { $total } total
    }
    *[other] { $fortress ->
        [0] { $player }: +{ $general } do general = { $total } total
        [1] { $player }: +{ $general } do general, +1 da fortaleza = { $total } total
        *[other] { $player }: +{ $general } do general, +{ $fortress } das fortalezas = { $total } total
    }
}

# Battle
ageofheroes-battle-start = A batalha começa. { $att_armies } { $att_armies ->
    [one] exército
    *[other] exércitos
} de { $attacker } contra { $def_armies } { $def_armies ->
    [one] exército
    *[other] exércitos
} de { $defender }.
ageofheroes-dice-roll-detailed = { $name } tira { $dice }{ $general ->
    [0] {""}
    *[other] { " + { $general } do general" }
}{ $fortress ->
    [0] {""}
    [one] { " + 1 da fortaleza" }
    *[other] { " + { $fortress } das fortalezas" }
} = { $total }.
ageofheroes-dice-roll-detailed-you = Você tira { $dice }{ $general ->
    [0] {""}
    *[other] { " + { $general } do general" }
}{ $fortress ->
    [0] {""}
    [one] { " + 1 da fortaleza" }
    *[other] { " + { $fortress } das fortalezas" }
} = { $total }.
ageofheroes-round-attacker-wins = { $attacker } vence a rodada ({ $att_total } vs { $def_total }). { $defender } perde um exército.
ageofheroes-round-defender-wins = { $defender } defende com sucesso ({ $def_total } vs { $att_total }). { $attacker } perde um exército.
ageofheroes-round-draw = Ambos os lados empatam em { $total }. Nenhum exército perdido.
ageofheroes-battle-victory-attacker = { $attacker } derrota { $defender }.
ageofheroes-battle-victory-defender = { $defender } defende com sucesso contra { $attacker }.
ageofheroes-battle-mutual-defeat = Tanto { $attacker } quanto { $defender } perdem todos os exércitos.
ageofheroes-general-bonus = +{ $count } de { $count ->
    [one] general
    *[other] generais
}
ageofheroes-fortress-bonus = +{ $count } de defesa da fortaleza
ageofheroes-battle-winner = { $winner } vence a batalha.
ageofheroes-battle-draw = A batalha termina em empate...
ageofheroes-battle-continue = Continuar a batalha.
ageofheroes-battle-end = A batalha acabou.

# War outcomes
ageofheroes-conquest-success = { $attacker } conquista { $count } { $count ->
    [one] cidade
    *[other] cidades
} de { $defender }.
ageofheroes-plunder-success = { $attacker } pilha { $count } { $count ->
    [one] carta
    *[other] cartas
} de { $defender }.
ageofheroes-destruction-success = { $attacker } destrói { $count } { $count ->
    [one] recurso de monumento
    *[other] recursos de monumento
} de { $defender }.
ageofheroes-army-losses = { $player } perde { $count } { $count ->
    [one] exército
    *[other] exércitos
}.
ageofheroes-army-losses-you = Você perde { $count } { $count ->
    [one] exército
    *[other] exércitos
}.

# Army return
ageofheroes-army-return-road = Suas tropas retornam imediatamente pela estrada.
ageofheroes-army-return-delayed = { $count } { $count ->
    [one] unidade retorna
    *[other] unidades retornam
} no final do seu próximo turno.
ageofheroes-army-returned = As tropas de { $player } retornaram da guerra.
ageofheroes-army-returned-you = Suas tropas retornaram da guerra.
ageofheroes-army-recover = Os exércitos de { $player } se recuperam do terremoto.
ageofheroes-army-recover-you = Seus exércitos se recuperam do terremoto.

# Olympics
ageofheroes-olympics-cancel = { $player } joga Jogos Olímpicos. Guerra cancelada.
ageofheroes-olympics-prompt = { $attacker } declarou guerra. Você tem Jogos Olímpicos - usar para cancelar?
ageofheroes-yes = Sim
ageofheroes-no = Não

# Monument progress
ageofheroes-monument-progress = O monumento de { $player } está { $count }/5 completo.
ageofheroes-monument-progress-you = Seu monumento está { $count }/5 completo.

# Hand management
ageofheroes-discard-excess = Você tem mais de { $max } cartas. Descarte { $count } { $count ->
    [one] carta
    *[other] cartas
}.
ageofheroes-discard-excess-other = { $player } deve descartar cartas em excesso.
ageofheroes-discard-more = Descarte mais { $count } { $count ->
    [one] carta
    *[other] cartas
}.

# Victory
ageofheroes-victory-cities = { $player } construiu 5 cidades! Império das Cinco Cidades.
ageofheroes-victory-cities-you = Você construiu 5 cidades! Império das Cinco Cidades.
ageofheroes-victory-monument = { $player } completou seu monumento! Portadores da Grande Cultura.
ageofheroes-victory-monument-you = Você completou seu monumento! Portadores da Grande Cultura.
ageofheroes-victory-last-standing = { $player } é a última tribo em pé! Os Mais Persistentes.
ageofheroes-victory-last-standing-you = Você é a última tribo em pé! Os Mais Persistentes.
ageofheroes-game-over = Fim de jogo.

# Elimination
ageofheroes-eliminated = { $player } foi eliminado.
ageofheroes-eliminated-you = Você foi eliminado.

# Hand
ageofheroes-hand-empty = Você não tem cartas.
ageofheroes-hand-contents = Sua mão ({ $count } { $count ->
    [one] carta
    *[other] cartas
}): { $cards }

# Status
ageofheroes-status = { $player } ({ $tribe }): { $cities } { $cities ->
    [one] cidade
    *[other] cidades
}, { $armies } { $armies ->
    [one] exército
    *[other] exércitos
}, { $monument }/5 monumento
ageofheroes-status-detailed-header = { $player } ({ $tribe })
ageofheroes-status-cities = Cidades: { $count }
ageofheroes-status-armies = Exércitos: { $count }
ageofheroes-status-generals = Generais: { $count }
ageofheroes-status-fortresses = Fortalezas: { $count }
ageofheroes-status-monument = Monumento: { $count }/5
ageofheroes-status-roads = Estradas: { $left }{ $right }
ageofheroes-status-road-left = esquerda
ageofheroes-status-road-right = direita
ageofheroes-status-none = nenhuma
ageofheroes-status-earthquake-armies = Exércitos em recuperação: { $count }
ageofheroes-status-returning-armies = Exércitos retornando: { $count }
ageofheroes-status-returning-generals = Generais retornando: { $count }

# Deck info
ageofheroes-deck-empty = Não há mais cartas de { $card } no baralho.
ageofheroes-deck-count = Cartas restantes: { $count }
ageofheroes-deck-reshuffled = A pilha de descarte foi embaralhada de volta no baralho.

# Give up
ageofheroes-give-up-confirm = Tem certeza que quer desistir?
ageofheroes-gave-up = { $player } desistiu!
ageofheroes-gave-up-you = Você desistiu!

# Hero card
ageofheroes-hero-use = Usar como exército ou general?
ageofheroes-hero-army = Exército
ageofheroes-hero-general = General

# Fortune card
ageofheroes-fortune-reroll = { $player } usa Fortuna para rolar novamente.
ageofheroes-fortune-prompt = Você perdeu a rolagem. Usar Fortuna para rolar novamente?

# Disabled action reasons
ageofheroes-not-your-turn = Não é sua vez.
ageofheroes-game-not-started = O jogo ainda não começou.
ageofheroes-wrong-phase = Esta ação não está disponível na fase atual.
ageofheroes-no-resources = Você não tem os recursos necessários.

# Building costs (for display)
ageofheroes-cost-army = 2 Grão, Ferro
ageofheroes-cost-fortress = Ferro, Madeira, Pedra
ageofheroes-cost-general = Ferro, Ouro
ageofheroes-cost-road = 2 Pedra
ageofheroes-cost-city = 2 Madeira, Pedra
