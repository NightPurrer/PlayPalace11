# Age of Heroes-Spielnachrichten
# Ein Zivilisationsaufbauspiel für 2-6 Spieler

# Spielname
game-name-ageofheroes = Age of Heroes

# Stämme
ageofheroes-tribe-egyptians = Ägypter
ageofheroes-tribe-romans = Römer
ageofheroes-tribe-greeks = Griechen
ageofheroes-tribe-babylonians = Babylonier
ageofheroes-tribe-celts = Kelten
ageofheroes-tribe-chinese = Chinesen

# Spezielle Ressourcen (für Monumente)
ageofheroes-special-limestone = Kalkstein
ageofheroes-special-concrete = Beton
ageofheroes-special-marble = Marmor
ageofheroes-special-bricks = Ziegel
ageofheroes-special-sandstone = Sandstein
ageofheroes-special-granite = Granit

# Standardressourcen
ageofheroes-resource-iron = Eisen
ageofheroes-resource-wood = Holz
ageofheroes-resource-grain = Getreide
ageofheroes-resource-stone = Stein
ageofheroes-resource-gold = Gold

# Ereignisse
ageofheroes-event-population-growth = Bevölkerungswachstum
ageofheroes-event-earthquake = Erdbeben
ageofheroes-event-eruption = Ausbruch
ageofheroes-event-hunger = Hunger
ageofheroes-event-barbarians = Barbaren
ageofheroes-event-olympics = Olympische Spiele
ageofheroes-event-hero = Held
ageofheroes-event-fortune = Glück

# Gebäude
ageofheroes-building-army = Armee
ageofheroes-building-fortress = Festung
ageofheroes-building-general = General
ageofheroes-building-road = Straße
ageofheroes-building-city = Stadt

# Aktionen
ageofheroes-action-tax-collection = Steuererhebung
ageofheroes-action-construction = Bau
ageofheroes-action-war = Krieg
ageofheroes-action-do-nothing = Nichts tun
ageofheroes-play = Spielen

# Kriegsziele
ageofheroes-war-conquest = Eroberung
ageofheroes-war-plunder = Plünderung
ageofheroes-war-destruction = Zerstörung

# Spieloptionen
ageofheroes-set-victory-cities = Siegstädte: { $cities }
ageofheroes-enter-victory-cities = Anzahl der Städte zum Sieg eingeben (3-7)
ageofheroes-set-victory-monument = Monumentfertigstellung: { $progress }%
ageofheroes-toggle-neighbor-roads = Straßen nur zu Nachbarn: { $enabled }
ageofheroes-set-max-hand = Maximale Handgröße: { $cards } Karten

# Optionsänderungsankündigungen
ageofheroes-option-changed-victory-cities = Sieg erfordert { $cities } Städte.
ageofheroes-option-changed-victory-monument = Monumentfertigstellungsschwelle auf { $progress }% gesetzt.
ageofheroes-option-changed-neighbor-roads = Straßen nur zu Nachbarn { $enabled }.
ageofheroes-option-changed-max-hand = Maximale Handgröße auf { $cards } Karten gesetzt.

# Setup-Phase
ageofheroes-setup-start = Sie sind der Anführer des { $tribe }-Stammes. Ihre spezielle Monumentressource ist { $special }. Würfeln Sie, um die Zugreihenfolge zu bestimmen.
ageofheroes-setup-viewer = Spieler würfeln, um die Zugreihenfolge zu bestimmen.
ageofheroes-roll-dice = Die Würfel werfen
ageofheroes-war-roll-dice = Die Würfel werfen
ageofheroes-dice-result = Sie würfelten { $total } ({ $die1 } + { $die2 }).
ageofheroes-dice-result-other = { $player } würfelte { $total }.
ageofheroes-dice-tie = Mehrere Spieler haben mit { $total } gleichauf. Würfeln erneut...
ageofheroes-first-player = { $player } würfelte am höchsten mit { $total } und ist als Erster dran.
ageofheroes-first-player-you = Mit { $total } Punkten sind Sie als Erster dran.

# Vorbereitungsphase
ageofheroes-prepare-start = Spieler müssen Ereigniskarten spielen und Katastrophen ablegen.
ageofheroes-prepare-your-turn = Sie haben { $count } { $count ->
    [one] Karte
    *[other] Karten
} zum Spielen oder Ablegen.
ageofheroes-prepare-done = Vorbereitungsphase abgeschlossen.

# Gespielte/abgelegte Ereignisse
ageofheroes-population-growth = { $player } spielt Bevölkerungswachstum und baut eine neue Stadt.
ageofheroes-population-growth-you = Sie spielen Bevölkerungswachstum und bauen eine neue Stadt.
ageofheroes-discard-card = { $player } legt { $card } ab.
ageofheroes-discard-card-you = Sie legen { $card } ab.
ageofheroes-earthquake = Ein Erdbeben trifft den Stamm von { $player }; ihre Armeen erholen sich.
ageofheroes-earthquake-you = Ein Erdbeben trifft Ihren Stamm; Ihre Armeen erholen sich.
ageofheroes-eruption = Ein Ausbruch zerstört eine der Städte von { $player }.
ageofheroes-eruption-you = Ein Ausbruch zerstört eine Ihrer Städte.

# Katastropheneffekte
ageofheroes-hunger-strikes = Hunger schlägt zu.
ageofheroes-lose-card-hunger = Sie verlieren { $card }.
ageofheroes-barbarians-pillage = Barbaren greifen die Ressourcen von { $player } an.
ageofheroes-barbarians-attack = Barbaren greifen die Ressourcen von { $player } an.
ageofheroes-barbarians-attack-you = Barbaren greifen Ihre Ressourcen an.
ageofheroes-lose-card-barbarians = Sie verlieren { $card }.
ageofheroes-block-with-card = { $player } blockiert die Katastrophe mit { $card }.
ageofheroes-block-with-card-you = Sie blockieren die Katastrophe mit { $card }.

# Gezielte Katastrophenkarten (Erdbeben/Ausbruch)
ageofheroes-select-disaster-target = Wählen Sie ein Ziel für { $card }.
ageofheroes-no-targets = Keine gültigen Ziele verfügbar.
ageofheroes-earthquake-strikes-you = { $attacker } spielt Erdbeben gegen Sie. Ihre Armeen sind deaktiviert.
ageofheroes-earthquake-strikes = { $attacker } spielt Erdbeben gegen { $player }.
ageofheroes-armies-disabled = { $count } { $count ->
    [one] Armee ist
    *[other] Armeen sind
} für einen Zug deaktiviert.
ageofheroes-eruption-strikes-you = { $attacker } spielt Ausbruch gegen Sie. Eine Ihrer Städte wird zerstört.
ageofheroes-eruption-strikes = { $attacker } spielt Ausbruch gegen { $player }.
ageofheroes-city-destroyed = Eine Stadt wird durch den Ausbruch zerstört.

# Marktphase
ageofheroes-fair-start = Der Tag dämmert auf dem Marktplatz.
ageofheroes-fair-draw-base = Sie ziehen { $count } { $count ->
    [one] Karte
    *[other] Karten
}.
ageofheroes-fair-draw-roads = Sie ziehen { $count } zusätzliche { $count ->
    [one] Karte
    *[other] Karten
} dank Ihres Straßennetzwerks.
ageofheroes-fair-draw-other = { $player } zieht { $count } { $count ->
    [one] Karte
    *[other] Karten
}.

# Handeln/Auktion
ageofheroes-auction-start = Auktion beginnt.
ageofheroes-offer-trade = Handel anbieten
ageofheroes-offer-made = { $player } bietet { $card } für { $wanted } an.
ageofheroes-offer-made-you = Sie bieten { $card } für { $wanted } an.
ageofheroes-trade-accepted = { $player } akzeptiert das Angebot von { $other } und tauscht { $give } für { $receive }.
ageofheroes-trade-accepted-you = Sie akzeptieren das Angebot von { $other } und erhalten { $receive }.
ageofheroes-trade-cancelled = { $player } zieht sein Angebot für { $card } zurück.
ageofheroes-trade-cancelled-you = Sie ziehen Ihr Angebot für { $card } zurück.
ageofheroes-stop-trading = Handel beenden
ageofheroes-select-request = Sie bieten { $card } an. Was wollen Sie im Gegenzug?
ageofheroes-cancel = Abbrechen
ageofheroes-left-auction = { $player } geht.
ageofheroes-left-auction-you = Sie gehen vom Marktplatz.
ageofheroes-any-card = Beliebige Karte
ageofheroes-cannot-trade-own-special = Sie können Ihre eigene spezielle Monumentressource nicht handeln.
ageofheroes-resource-not-in-game = Diese spezielle Ressource wird in diesem Spiel nicht verwendet.

# Hauptspielphase
ageofheroes-play-start = Spielphase.
ageofheroes-day = Tag { $day }
ageofheroes-draw-card = { $player } zieht eine Karte vom Stapel.
ageofheroes-draw-card-you = Sie ziehen { $card } vom Stapel.
ageofheroes-your-action = Was möchten Sie tun?

# Steuererhebung
ageofheroes-tax-collection = { $player } wählt Steuererhebung: { $cities } { $cities ->
    [one] Stadt
    *[other] Städte
} sammelt { $cards } { $cards ->
    [one] Karte
    *[other] Karten
}.
ageofheroes-tax-collection-you = Sie wählen Steuererhebung: { $cities } { $cities ->
    [one] Stadt
    *[other] Städte
} sammelt { $cards } { $cards ->
    [one] Karte
    *[other] Karten
}.
ageofheroes-tax-no-city = Steuererhebung: Sie haben keine überlebenden Städte. Legen Sie eine Karte ab, um eine neue zu ziehen.
ageofheroes-tax-no-city-done = { $player } wählt Steuererhebung, hat aber keine Städte, also tauscht er eine Karte.
ageofheroes-tax-no-city-done-you = Steuererhebung: Sie tauschten { $card } für eine neue Karte.

# Bau
ageofheroes-construction-menu = Was möchten Sie bauen?
ageofheroes-construction-done = { $player } baute { $article } { $building }.
ageofheroes-construction-done-you = Sie bauten { $article } { $building }.
ageofheroes-construction-stop = Bauen beenden
ageofheroes-construction-stopped = Sie entschieden sich, den Bau zu beenden.
ageofheroes-road-select-neighbor = Wählen Sie, zu welchem Nachbarn Sie eine Straße bauen möchten.
ageofheroes-direction-left = Zu Ihrer Linken
ageofheroes-direction-right = Zu Ihrer Rechten
ageofheroes-road-request-sent = Straßenanfrage gesendet. Warte auf Genehmigung des Nachbarn.
ageofheroes-road-request-received = { $requester } bittet um Erlaubnis, eine Straße zu Ihrem Stamm zu bauen.
ageofheroes-road-request-denied-you = Sie lehnten die Straßenanfrage ab.
ageofheroes-road-request-denied = { $denier } lehnte Ihre Straßenanfrage ab.
ageofheroes-road-built = { $tribe1 } und { $tribe2 } sind jetzt durch eine Straße verbunden.
ageofheroes-road-no-target = Keine benachbarten Stämme für Straßenbau verfügbar.
ageofheroes-approve = Genehmigen
ageofheroes-deny = Ablehnen
ageofheroes-supply-exhausted = Keine weiteren { $building } zum Bauen verfügbar.

# Nichts tun
ageofheroes-do-nothing = { $player } passt.
ageofheroes-do-nothing-you = Sie passen...

# Krieg
ageofheroes-war-declare = { $attacker } erklärt { $defender } den Krieg. Ziel: { $goal }.
ageofheroes-war-prepare = Wählen Sie Ihre Armeen für { $action }.
ageofheroes-war-no-army = Sie haben keine Armeen oder Heldenkarten verfügbar.
ageofheroes-war-no-targets = Keine gültigen Ziele für Krieg.
ageofheroes-war-no-valid-goal = Keine gültigen Kriegsziele gegen dieses Ziel.
ageofheroes-war-select-target = Wählen Sie, welchen Spieler Sie angreifen möchten.
ageofheroes-war-select-goal = Wählen Sie Ihr Kriegsziel.
ageofheroes-war-prepare-attack = Wählen Sie Ihre Angriffskräfte.
ageofheroes-war-prepare-defense = { $attacker } greift Sie an; Wählen Sie Ihre Verteidigungskräfte.
ageofheroes-war-select-armies = Armeen auswählen: { $count }
ageofheroes-war-select-generals = Generäle auswählen: { $count }
ageofheroes-war-select-heroes = Helden auswählen: { $count }
ageofheroes-war-attack = Angreifen...
ageofheroes-war-defend = Verteidigen...
ageofheroes-war-prepared = Ihre Streitkräfte: { $armies } { $armies ->
    [one] Armee
    *[other] Armeen
}{ $generals ->
    [0] {""}
    [one] {" und 1 General"}
    *[other] {" und { $generals } Generäle"}
}{ $heroes ->
    [0] {""}
    [one] {" und 1 Held"}
    *[other] {" und { $heroes } Helden"}
}.
ageofheroes-war-roll-you = Sie würfeln { $roll }.
ageofheroes-war-roll-other = { $player } würfelt { $roll }.
ageofheroes-war-bonuses-you = { $general ->
    [0] { $fortress ->
        [0] {""}
        [1] +1 von Festung = { $total } gesamt
        *[other] +{ $fortress } von Festungen = { $total } gesamt
    }
    *[other] { $fortress ->
        [0] +{ $general } von General = { $total } gesamt
        [1] +{ $general } von General, +1 von Festung = { $total } gesamt
        *[other] +{ $general } von General, +{ $fortress } von Festungen = { $total } gesamt
    }
}
ageofheroes-war-bonuses-other = { $general ->
    [0] { $fortress ->
        [0] {""}
        [1] { $player }: +1 von Festung = { $total } gesamt
        *[other] { $player }: +{ $fortress } von Festungen = { $total } gesamt
    }
    *[other] { $fortress ->
        [0] { $player }: +{ $general } von General = { $total } gesamt
        [1] { $player }: +{ $general } von General, +1 von Festung = { $total } gesamt
        *[other] { $player }: +{ $general } von General, +{ $fortress } von Festungen = { $total } gesamt
    }
}

# Schlacht
ageofheroes-battle-start = Schlacht beginnt. { $attacker }s { $att_armies } { $att_armies ->
    [one] Armee
    *[other] Armeen
} gegen { $defender }s { $def_armies } { $def_armies ->
    [one] Armee
    *[other] Armeen
}.
ageofheroes-dice-roll-detailed = { $name } würfelt { $dice }{ $general ->
    [0] {""}
    *[other] { " + { $general } von General" }
}{ $fortress ->
    [0] {""}
    [one] { " + 1 von Festung" }
    *[other] { " + { $fortress } von Festungen" }
} = { $total }.
ageofheroes-dice-roll-detailed-you = Sie würfeln { $dice }{ $general ->
    [0] {""}
    *[other] { " + { $general } von General" }
}{ $fortress ->
    [0] {""}
    [one] { " + 1 von Festung" }
    *[other] { " + { $fortress } von Festungen" }
} = { $total }.
ageofheroes-round-attacker-wins = { $attacker } gewinnt die Runde ({ $att_total } gegen { $def_total }). { $defender } verliert eine Armee.
ageofheroes-round-defender-wins = { $defender } verteidigt erfolgreich ({ $def_total } gegen { $att_total }). { $attacker } verliert eine Armee.
ageofheroes-round-draw = Beide Seiten unentschieden bei { $total }. Keine Armeen verloren.
ageofheroes-battle-victory-attacker = { $attacker } besiegt { $defender }.
ageofheroes-battle-victory-defender = { $defender } verteidigt erfolgreich gegen { $attacker }.
ageofheroes-battle-mutual-defeat = Sowohl { $attacker } als auch { $defender } verlieren alle Armeen.
ageofheroes-general-bonus = +{ $count } von { $count ->
    [one] General
    *[other] Generälen
}
ageofheroes-fortress-bonus = +{ $count } von Festungsverteidigung
ageofheroes-battle-winner = { $winner } gewinnt die Schlacht.
ageofheroes-battle-draw = Die Schlacht endet unentschieden...
ageofheroes-battle-continue = Schlacht fortsetzen.
ageofheroes-battle-end = Die Schlacht ist vorbei.

# Kriegsergebnisse
ageofheroes-conquest-success = { $attacker } erobert { $count } { $count ->
    [one] Stadt
    *[other] Städte
} von { $defender }.
ageofheroes-plunder-success = { $attacker } plündert { $count } { $count ->
    [one] Karte
    *[other] Karten
} von { $defender }.
ageofheroes-destruction-success = { $attacker } zerstört { $count } von { $defender }s Monument-{ $count ->
    [one] ressource
    *[other] ressourcen
}.
ageofheroes-army-losses = { $player } verliert { $count } { $count ->
    [one] Armee
    *[other] Armeen
}.
ageofheroes-army-losses-you = Sie verlieren { $count } { $count ->
    [one] Armee
    *[other] Armeen
}.

# Armeerückkehr
ageofheroes-army-return-road = Ihre Truppen kehren sofort über die Straße zurück.
ageofheroes-army-return-delayed = { $count } { $count ->
    [one] Einheit kehrt zurück
    *[other] Einheiten kehren zurück
} am Ende Ihres nächsten Zugs.
ageofheroes-army-returned = Die Truppen von { $player } sind vom Krieg zurückgekehrt.
ageofheroes-army-returned-you = Ihre Truppen sind vom Krieg zurückgekehrt.
ageofheroes-army-recover = Die Armeen von { $player } erholen sich vom Erdbeben.
ageofheroes-army-recover-you = Ihre Armeen erholen sich vom Erdbeben.

# Olympiade
ageofheroes-olympics-cancel = { $player } spielt Olympische Spiele. Krieg abgebrochen.
ageofheroes-olympics-prompt = { $attacker } hat den Krieg erklärt. Sie haben Olympische Spiele - verwenden, um abzubrechen?
ageofheroes-yes = Ja
ageofheroes-no = Nein

# Monumentfortschritt
ageofheroes-monument-progress = Das Monument von { $player } ist { $count }/5 fertig.
ageofheroes-monument-progress-you = Ihr Monument ist { $count }/5 fertig.

# Handverwaltung
ageofheroes-discard-excess = Sie haben mehr als { $max } Karten. Legen Sie { $count } { $count ->
    [one] Karte
    *[other] Karten
} ab.
ageofheroes-discard-excess-other = { $player } muss überschüssige Karten ablegen.
ageofheroes-discard-more = Legen Sie { $count } weitere { $count ->
    [one] Karte
    *[other] Karten
} ab.

# Sieg
ageofheroes-victory-cities = { $player } hat 5 Städte gebaut! Reich der Fünf Städte.
ageofheroes-victory-cities-you = Sie haben 5 Städte gebaut! Reich der Fünf Städte.
ageofheroes-victory-monument = { $player } hat sein Monument fertiggestellt! Träger großer Kultur.
ageofheroes-victory-monument-you = Sie haben Ihr Monument fertiggestellt! Träger großer Kultur.
ageofheroes-victory-last-standing = { $player } ist der letzte überlebende Stamm! Der Beharrlichste.
ageofheroes-victory-last-standing-you = Sie sind der letzte überlebende Stamm! Der Beharrlichste.
ageofheroes-game-over = Spiel vorbei.

# Eliminierung
ageofheroes-eliminated = { $player } wurde eliminiert.
ageofheroes-eliminated-you = Sie wurden eliminiert.

# Hand
ageofheroes-hand-empty = Sie haben keine Karten.
ageofheroes-hand-contents = Ihre Hand ({ $count } { $count ->
    [one] Karte
    *[other] Karten
}): { $cards }

# Status
ageofheroes-status = { $player } ({ $tribe }): { $cities } { $cities ->
    [one] Stadt
    *[other] Städte
}, { $armies } { $armies ->
    [one] Armee
    *[other] Armeen
}, { $monument }/5 Monument
ageofheroes-status-detailed-header = { $player } ({ $tribe })
ageofheroes-status-cities = Städte: { $count }
ageofheroes-status-armies = Armeen: { $count }
ageofheroes-status-generals = Generäle: { $count }
ageofheroes-status-fortresses = Festungen: { $count }
ageofheroes-status-monument = Monument: { $count }/5
ageofheroes-status-roads = Straßen: { $left }{ $right }
ageofheroes-status-road-left = links
ageofheroes-status-road-right = rechts
ageofheroes-status-none = keine
ageofheroes-status-earthquake-armies = Erholende Armeen: { $count }
ageofheroes-status-returning-armies = Zurückkehrende Armeen: { $count }
ageofheroes-status-returning-generals = Zurückkehrende Generäle: { $count }

# Stapelinfo
ageofheroes-deck-empty = Keine weiteren { $card }-Karten im Stapel.
ageofheroes-deck-count = Verbleibende Karten: { $count }
ageofheroes-deck-reshuffled = Der Ablagestapel wurde in den Stapel gemischt.

# Aufgeben
ageofheroes-give-up-confirm = Sind Sie sicher, dass Sie aufgeben möchten?
ageofheroes-gave-up = { $player } gab auf!
ageofheroes-gave-up-you = Sie gaben auf!

# Heldenkarte
ageofheroes-hero-use = Als Armee oder General verwenden?
ageofheroes-hero-army = Armee
ageofheroes-hero-general = General

# Glückskarte
ageofheroes-fortune-reroll = { $player } verwendet Glück, um neu zu würfeln.
ageofheroes-fortune-prompt = Sie verloren den Wurf. Glück verwenden, um neu zu würfeln?

# Gründe für deaktivierte Aktionen
ageofheroes-not-your-turn = Sie sind nicht am Zug.
ageofheroes-game-not-started = Das Spiel hat noch nicht begonnen.
ageofheroes-wrong-phase = Diese Aktion ist in der aktuellen Phase nicht verfügbar.
ageofheroes-no-resources = Sie haben nicht die erforderlichen Ressourcen.

# Baukosten (zur Anzeige)
ageofheroes-cost-army = 2 Getreide, Eisen
ageofheroes-cost-fortress = Eisen, Holz, Stein
ageofheroes-cost-general = Eisen, Gold
ageofheroes-cost-road = 2 Stein
ageofheroes-cost-city = 2 Holz, Stein
