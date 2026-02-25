# Age of Heroes game messages
# A civilization-building card game for 2-6 players

# Game name
game-name-ageofheroes = Wiek Bohaterów

# Tribes
ageofheroes-tribe-egyptians = Egipcjanie
ageofheroes-tribe-romans = Rzymianie
ageofheroes-tribe-greeks = Grecy
ageofheroes-tribe-babylonians = Babilończycy
ageofheroes-tribe-celts = Celtowie
ageofheroes-tribe-chinese = Chińczycy

# Special Resources (for monuments)
ageofheroes-special-limestone = Wapień
ageofheroes-special-concrete = Beton
ageofheroes-special-marble = Marmur
ageofheroes-special-bricks = Cegły
ageofheroes-special-sandstone = Piaskowiec
ageofheroes-special-granite = Granit

# Standard Resources
ageofheroes-resource-iron = Żelazo
ageofheroes-resource-wood = Drewno
ageofheroes-resource-grain = Zboże
ageofheroes-resource-stone = Kamień
ageofheroes-resource-gold = Złoto

# Events
ageofheroes-event-population-growth = Wzrost Populacji
ageofheroes-event-earthquake = Trzęsienie Ziemi
ageofheroes-event-eruption = Erupcja
ageofheroes-event-hunger = Głód
ageofheroes-event-barbarians = Barbarzyńcy
ageofheroes-event-olympics = Igrzyska Olimpijskie
ageofheroes-event-hero = Bohater
ageofheroes-event-fortune = Fortuna

# Buildings
ageofheroes-building-army = Armia
ageofheroes-building-fortress = Twierdza
ageofheroes-building-general = Generał
ageofheroes-building-road = Droga
ageofheroes-building-city = Miasto

# Actions
ageofheroes-action-tax-collection = Pobór Podatków
ageofheroes-action-construction = Budowa
ageofheroes-action-war = Wojna
ageofheroes-action-do-nothing = Nic Nie Rób
ageofheroes-play = Zagraj

# War goals
ageofheroes-war-conquest = Podbój
ageofheroes-war-plunder = Grabież
ageofheroes-war-destruction = Zniszczenie

# Game options
ageofheroes-set-victory-cities = Miasta zwycięstwa: { $cities }
ageofheroes-enter-victory-cities = Wprowadź liczbę miast do wygranej (3-7)
ageofheroes-set-victory-monument = Ukończenie pomnika: { $progress }%
ageofheroes-toggle-neighbor-roads = Drogi tylko do sąsiadów: { $enabled }
ageofheroes-set-max-hand = Maksymalny rozmiar ręki: { $cards } kart

# Option change announcements
ageofheroes-option-changed-victory-cities = Zwycięstwo wymaga { $cities } miast.
ageofheroes-option-changed-victory-monument = Próg ukończenia pomnika ustawiony na { $progress }%.
ageofheroes-option-changed-neighbor-roads = Drogi tylko do sąsiadów { $enabled }.
ageofheroes-option-changed-max-hand = Maksymalny rozmiar ręki ustawiony na { $cards } kart.

# Setup phase
ageofheroes-setup-start = Jesteś przywódcą plemienia { $tribe }. Twój specjalny zasób do pomnika to { $special }. Rzuć kostkami, aby określić kolejność tur.
ageofheroes-setup-viewer = Gracze rzucają kostkami, aby określić kolejność tur.
ageofheroes-roll-dice = Rzuć kostkami
ageofheroes-war-roll-dice = Rzuć kostkami
ageofheroes-dice-result = Wyrzuciłeś { $total } ({ $die1 } + { $die2 }).
ageofheroes-dice-result-other = { $player } wyrzucił { $total }.
ageofheroes-dice-tie = Wielu graczy zremisowało z { $total }. Rzucamy ponownie...
ageofheroes-first-player = { $player } wyrzucił najwyżej z { $total } i zaczyna pierwszy.
ageofheroes-first-player-you = Z { $total } punktami, zaczynasz pierwszy.

# Preparation phase
ageofheroes-prepare-start = Gracze muszą zagrać karty wydarzeń i odrzucić katastrofy.
ageofheroes-prepare-your-turn = Masz { $count } { $count ->
    [one] kartę
    [few] karty
    *[other] kart
} do zagrania lub odrzucenia.
ageofheroes-prepare-done = Faza przygotowania zakończona.

# Events played/discarded
ageofheroes-population-growth = { $player } gra Wzrost Populacji i buduje nowe miasto.
ageofheroes-population-growth-you = Grasz Wzrost Populacji i budujesz nowe miasto.
ageofheroes-discard-card = { $player } odrzuca { $card }.
ageofheroes-discard-card-you = Odrzucasz { $card }.
ageofheroes-earthquake = Trzęsienie ziemi uderza w plemię { $player }; ich armie przechodzą w regenerację.
ageofheroes-earthquake-you = Trzęsienie ziemi uderza w twoje plemię; twoje armie przechodzą w regenerację.
ageofheroes-eruption = Erupcja niszczy jedno z miast { $player }.
ageofheroes-eruption-you = Erupcja niszczy jedno z twoich miast.

# Disaster effects
ageofheroes-hunger-strikes = Nadchodzi głód.
ageofheroes-lose-card-hunger = Tracisz { $card }.
ageofheroes-barbarians-pillage = Barbarzyńcy atakują zasoby { $player }.
ageofheroes-barbarians-attack = Barbarzyńcy atakują zasoby { $player }.
ageofheroes-barbarians-attack-you = Barbarzyńcy atakują twoje zasoby.
ageofheroes-lose-card-barbarians = Tracisz { $card }.
ageofheroes-block-with-card = { $player } blokuje katastrofę używając { $card }.
ageofheroes-block-with-card-you = Blokujesz katastrofę używając { $card }.

# Targeted disaster cards (Earthquake/Eruption)
ageofheroes-select-disaster-target = Wybierz cel dla { $card }.
ageofheroes-no-targets = Brak dostępnych celów.
ageofheroes-earthquake-strikes-you = { $attacker } gra Trzęsienie Ziemi przeciwko tobie. Twoje armie są wyłączone.
ageofheroes-earthquake-strikes = { $attacker } gra Trzęsienie Ziemi przeciwko { $player }.
ageofheroes-armies-disabled = { $count } { $count ->
    [one] armia jest
    [few] armie są
    *[other] armii jest
} wyłączonych na jedną turę.
ageofheroes-eruption-strikes-you = { $attacker } gra Erupcję przeciwko tobie. Jedno z twoich miast zostaje zniszczone.
ageofheroes-eruption-strikes = { $attacker } gra Erupcję przeciwko { $player }.
ageofheroes-city-destroyed = Miasto zostaje zniszczone przez erupcję.

# Fair phase
ageofheroes-fair-start = Świta dzień na rynku.
ageofheroes-fair-draw-base = Dobierasz { $count } { $count ->
    [one] kartę
    [few] karty
    *[other] kart
}.
ageofheroes-fair-draw-roads = Dobierasz { $count } dodatkowych { $count ->
    [one] kartę
    [few] karty
    *[other] kart
} dzięki swojej sieci dróg.
ageofheroes-fair-draw-other = { $player } dobiera { $count } { $count ->
    [one] kartę
    [few] karty
    *[other] kart
}.

# Trading/Auction
ageofheroes-auction-start = Rozpoczyna się aukcja.
ageofheroes-offer-trade = Zaproponuj wymianę
ageofheroes-offer-made = { $player } oferuje { $card } za { $wanted }.
ageofheroes-offer-made-you = Oferujesz { $card } za { $wanted }.
ageofheroes-trade-accepted = { $player } akceptuje ofertę { $other } i wymienia { $give } na { $receive }.
ageofheroes-trade-accepted-you = Akceptujesz ofertę { $other } i otrzymujesz { $receive }.
ageofheroes-trade-cancelled = { $player } wycofuje swoją ofertę za { $card }.
ageofheroes-trade-cancelled-you = Wycofujesz swoją ofertę za { $card }.
ageofheroes-stop-trading = Zakończ handel
ageofheroes-select-request = Oferujesz { $card }. Czego chcesz w zamian?
ageofheroes-cancel = Anuluj
ageofheroes-left-auction = { $player } odchodzi.
ageofheroes-left-auction-you = Odchodzisz z rynku.
ageofheroes-any-card = Dowolna karta
ageofheroes-cannot-trade-own-special = Nie możesz wymienić swojego własnego specjalnego zasobu do pomnika.
ageofheroes-resource-not-in-game = Ten specjalny zasób nie jest używany w tej grze.

# Main play phase
ageofheroes-play-start = Faza gry.
ageofheroes-day = Dzień { $day }
ageofheroes-draw-card = { $player } dobiera kartę z talii.
ageofheroes-draw-card-you = Dobierasz { $card } z talii.
ageofheroes-your-action = Co chcesz zrobić?

# Tax Collection
ageofheroes-tax-collection = { $player } wybiera Pobór Podatków: { $cities } { $cities ->
    [one] miasto
    [few] miasta
    *[other] miast
} zbiera { $cards } { $cards ->
    [one] kartę
    [few] karty
    *[other] kart
}.
ageofheroes-tax-collection-you = Wybierasz Pobór Podatków: { $cities } { $cities ->
    [one] miasto
    [few] miasta
    *[other] miast
} zbiera { $cards } { $cards ->
    [one] kartę
    [few] karty
    *[other] kart
}.
ageofheroes-tax-no-city = Pobór Podatków: Nie masz żadnych ocalałych miast. Odrzuć kartę, aby dobrać nową.
ageofheroes-tax-no-city-done = { $player } wybiera Pobór Podatków, ale nie ma miast, więc wymienia kartę.
ageofheroes-tax-no-city-done-you = Pobór Podatków: Wymieniłeś { $card } na nową kartę.

# Construction
ageofheroes-construction-menu = Co chcesz zbudować?
ageofheroes-construction-done = { $player } zbudował { $article } { $building }.
ageofheroes-construction-done-you = Zbudowałeś { $article } { $building }.
ageofheroes-construction-stop = Przestań budować
ageofheroes-construction-stopped = Zdecydowałeś się przestać budować.
ageofheroes-road-select-neighbor = Wybierz sąsiada, do którego chcesz zbudować drogę.
ageofheroes-direction-left = Na lewo od ciebie
ageofheroes-direction-right = Na prawo od ciebie
ageofheroes-road-request-sent = Prośba o drogę wysłana. Oczekiwanie na zgodę sąsiada.
ageofheroes-road-request-received = { $requester } prosi o pozwolenie na budowę drogi do twojego plemienia.
ageofheroes-road-request-denied-you = Odrzuciłeś prośbę o drogę.
ageofheroes-road-request-denied = { $denier } odrzucił twoją prośbę o drogę.
ageofheroes-road-built = { $tribe1 } i { $tribe2 } są teraz połączone drogą.
ageofheroes-road-no-target = Brak sąsiednich plemion dostępnych do budowy drogi.
ageofheroes-approve = Zatwierdź
ageofheroes-deny = Odrzuć
ageofheroes-supply-exhausted = Nie ma więcej { $building } dostępnych do budowy.

# Do Nothing
ageofheroes-do-nothing = { $player } pasuje.
ageofheroes-do-nothing-you = Pasujesz...

# War
ageofheroes-war-declare = { $attacker } wypowiada wojnę { $defender }. Cel: { $goal }.
ageofheroes-war-prepare = Wybierz swoje armie do { $action }.
ageofheroes-war-no-army = Nie masz dostępnych armii ani kart bohatera.
ageofheroes-war-no-targets = Brak dostępnych celów do wojny.
ageofheroes-war-no-valid-goal = Brak dostępnych celów wojny przeciwko temu celowi.
ageofheroes-war-select-target = Wybierz gracza do ataku.
ageofheroes-war-select-goal = Wybierz swój cel wojny.
ageofheroes-war-prepare-attack = Wybierz swoje siły atakujące.
ageofheroes-war-prepare-defense = { $attacker } cię atakuje; Wybierz swoje siły obronne.
ageofheroes-war-select-armies = Wybierz armie: { $count }
ageofheroes-war-select-generals = Wybierz generałów: { $count }
ageofheroes-war-select-heroes = Wybierz bohaterów: { $count }
ageofheroes-war-attack = Atakuj...
ageofheroes-war-defend = Broń się...
ageofheroes-war-prepared = Twoje siły: { $armies } { $armies ->
    [one] armia
    [few] armie
    *[other] armii
}{ $generals ->
    [0] {""}
    [one] {" i 1 generał"}
    [few] {" i { $generals } generałów"}
    *[other] {" i { $generals } generałów"}
}{ $heroes ->
    [0] {""}
    [one] {" i 1 bohater"}
    [few] {" i { $heroes } bohaterów"}
    *[other] {" i { $heroes } bohaterów"}
}.
ageofheroes-war-roll-you = Rzucasz { $roll }.
ageofheroes-war-roll-other = { $player } rzuca { $roll }.
ageofheroes-war-bonuses-you = { $general ->
    [0] { $fortress ->
        [0] {""}
        [1] +1 z twierdzy = { $total } razem
        *[other] +{ $fortress } z twierdz = { $total } razem
    }
    *[other] { $fortress ->
        [0] +{ $general } od generała = { $total } razem
        [1] +{ $general } od generała, +1 z twierdzy = { $total } razem
        *[other] +{ $general } od generała, +{ $fortress } z twierdz = { $total } razem
    }
}
ageofheroes-war-bonuses-other = { $general ->
    [0] { $fortress ->
        [0] {""}
        [1] { $player }: +1 z twierdzy = { $total } razem
        *[other] { $player }: +{ $fortress } z twierdz = { $total } razem
    }
    *[other] { $fortress ->
        [0] { $player }: +{ $general } od generała = { $total } razem
        [1] { $player }: +{ $general } od generała, +1 z twierdzy = { $total } razem
        *[other] { $player }: +{ $general } od generała, +{ $fortress } z twierdz = { $total } razem
    }
}

# Battle
ageofheroes-battle-start = Rozpoczyna się bitwa. { $att_armies } { $att_armies ->
    [one] armia
    [few] armie
    *[other] armii
} { $attacker } przeciwko { $def_armies } { $def_armies ->
    [one] armii
    [few] armiom
    *[other] armiom
} { $defender }.
ageofheroes-dice-roll-detailed = { $name } rzuca { $dice }{ $general ->
    [0] {""}
    *[other] { " + { $general } od generała" }
}{ $fortress ->
    [0] {""}
    [one] { " + 1 z twierdzy" }
    *[other] { " + { $fortress } z twierdz" }
} = { $total }.
ageofheroes-dice-roll-detailed-you = Rzucasz { $dice }{ $general ->
    [0] {""}
    *[other] { " + { $general } od generała" }
}{ $fortress ->
    [0] {""}
    [one] { " + 1 z twierdzy" }
    *[other] { " + { $fortress } z twierdz" }
} = { $total }.
ageofheroes-round-attacker-wins = { $attacker } wygrywa rundę ({ $att_total } vs { $def_total }). { $defender } traci armię.
ageofheroes-round-defender-wins = { $defender } broni się pomyślnie ({ $def_total } vs { $att_total }). { $attacker } traci armię.
ageofheroes-round-draw = Obie strony remisują na { $total }. Brak strat.
ageofheroes-battle-victory-attacker = { $attacker } pokonuje { $defender }.
ageofheroes-battle-victory-defender = { $defender } broni się pomyślnie przeciwko { $attacker }.
ageofheroes-battle-mutual-defeat = Zarówno { $attacker } jak i { $defender } tracą wszystkie armie.
ageofheroes-general-bonus = +{ $count } od { $count ->
    [one] generała
    [few] generałów
    *[other] generałów
}
ageofheroes-fortress-bonus = +{ $count } z obrony twierdzy
ageofheroes-battle-winner = { $winner } wygrywa bitwę.
ageofheroes-battle-draw = Bitwa kończy się remisem...
ageofheroes-battle-continue = Kontynuuj bitwę.
ageofheroes-battle-end = Bitwa się kończy.

# War outcomes
ageofheroes-conquest-success = { $attacker } podbija { $count } { $count ->
    [one] miasto
    [few] miasta
    *[other] miast
} od { $defender }.
ageofheroes-plunder-success = { $attacker } grabieży { $count } { $count ->
    [one] kartę
    [few] karty
    *[other] kart
} od { $defender }.
ageofheroes-destruction-success = { $attacker } niszczy { $count } { $count ->
    [one] zasób pomnika
    [few] zasoby pomnika
    *[other] zasobów pomnika
} { $defender }.
ageofheroes-army-losses = { $player } traci { $count } { $count ->
    [one] armię
    [few] armie
    *[other] armii
}.
ageofheroes-army-losses-you = Tracisz { $count } { $count ->
    [one] armię
    [few] armie
    *[other] armii
}.

# Army return
ageofheroes-army-return-road = Twoje wojska wracają natychmiast drogą.
ageofheroes-army-return-delayed = { $count } { $count ->
    [one] jednostka wraca
    [few] jednostki wracają
    *[other] jednostek wraca
} na końcu twojej następnej tury.
ageofheroes-army-returned = Wojska { $player } wróciły z wojny.
ageofheroes-army-returned-you = Twoje wojska wróciły z wojny.
ageofheroes-army-recover = Armie { $player } regenerują się po trzęsieniu ziemi.
ageofheroes-army-recover-you = Twoje armie regenerują się po trzęsieniu ziemi.

# Olympics
ageofheroes-olympics-cancel = { $player } gra Igrzyska Olimpijskie. Wojna anulowana.
ageofheroes-olympics-prompt = { $attacker } wypowiedział wojnę. Masz Igrzyska Olimpijskie - użyć ich do anulowania?
ageofheroes-yes = Tak
ageofheroes-no = Nie

# Monument progress
ageofheroes-monument-progress = Pomnik { $player } jest ukończony w { $count }/5.
ageofheroes-monument-progress-you = Twój pomnik jest ukończony w { $count }/5.

# Hand management
ageofheroes-discard-excess = Masz więcej niż { $max } kart. Odrzuć { $count } { $count ->
    [one] kartę
    [few] karty
    *[other] kart
}.
ageofheroes-discard-excess-other = { $player } musi odrzucić nadmiarowe karty.
ageofheroes-discard-more = Odrzuć jeszcze { $count } { $count ->
    [one] kartę
    [few] karty
    *[other] kart
}.

# Victory
ageofheroes-victory-cities = { $player } zbudował 5 miast! Imperium Pięciu Miast.
ageofheroes-victory-cities-you = Zbudowałeś 5 miast! Imperium Pięciu Miast.
ageofheroes-victory-monument = { $player } ukończył swój pomnik! Nosiciele Wielkiej Kultury.
ageofheroes-victory-monument-you = Ukończyłeś swój pomnik! Nosiciele Wielkiej Kultury.
ageofheroes-victory-last-standing = { $player } jest ostatnim stojącym plemieniem! Najbardziej Wytrwali.
ageofheroes-victory-last-standing-you = Jesteś ostatnim stojącym plemieniem! Najbardziej Wytrwali.
ageofheroes-game-over = Koniec gry.

# Elimination
ageofheroes-eliminated = { $player } został wyeliminowany.
ageofheroes-eliminated-you = Zostałeś wyeliminowany.

# Hand
ageofheroes-hand-empty = Nie masz żadnych kart.
ageofheroes-hand-contents = Twoja ręka ({ $count } { $count ->
    [one] karta
    [few] karty
    *[other] kart
}): { $cards }

# Status
ageofheroes-status = { $player } ({ $tribe }): { $cities } { $cities ->
    [one] miasto
    [few] miasta
    *[other] miast
}, { $armies } { $armies ->
    [one] armia
    [few] armie
    *[other] armii
}, { $monument }/5 pomnika
ageofheroes-status-detailed-header = { $player } ({ $tribe })
ageofheroes-status-cities = Miasta: { $count }
ageofheroes-status-armies = Armie: { $count }
ageofheroes-status-generals = Generałowie: { $count }
ageofheroes-status-fortresses = Twierdze: { $count }
ageofheroes-status-monument = Pomnik: { $count }/5
ageofheroes-status-roads = Drogi: { $left }{ $right }
ageofheroes-status-road-left = w lewo
ageofheroes-status-road-right = w prawo
ageofheroes-status-none = brak
ageofheroes-status-earthquake-armies = Regenerujące się armie: { $count }
ageofheroes-status-returning-armies = Powracające armie: { $count }
ageofheroes-status-returning-generals = Powracający generałowie: { $count }

# Deck info
ageofheroes-deck-empty = Nie ma więcej kart { $card } w talii.
ageofheroes-deck-count = Pozostałe karty: { $count }
ageofheroes-deck-reshuffled = Stos odrzutu został przetasowany do talii.

# Give up
ageofheroes-give-up-confirm = Czy na pewno chcesz się poddać?
ageofheroes-gave-up = { $player } się poddał!
ageofheroes-gave-up-you = Poddałeś się!

# Hero card
ageofheroes-hero-use = Użyć jako armię czy generała?
ageofheroes-hero-army = Armia
ageofheroes-hero-general = Generał

# Fortune card
ageofheroes-fortune-reroll = { $player } używa Fortuny do ponownego rzutu.
ageofheroes-fortune-prompt = Przegrałeś rzut. Użyć Fortuny do ponownego rzutu?

# Disabled action reasons
ageofheroes-not-your-turn = To nie twoja tura.
ageofheroes-game-not-started = Gra jeszcze się nie rozpoczęła.
ageofheroes-wrong-phase = Ta akcja nie jest dostępna w obecnej fazie.
ageofheroes-no-resources = Nie masz wymaganych zasobów.

# Building costs (for display)
ageofheroes-cost-army = 2 Zboże, Żelazo
ageofheroes-cost-fortress = Żelazo, Drewno, Kamień
ageofheroes-cost-general = Żelazo, Złoto
ageofheroes-cost-road = 2 Kamień
ageofheroes-cost-city = 2 Drewno, Kamień
