# Age of Heroes game messages
# A civilization-building card game for 2-6 players

# Game name
game-name-ageofheroes = Age of Heroes

# Tribes
ageofheroes-tribe-egyptians = Egyptians
ageofheroes-tribe-romans = Romans
ageofheroes-tribe-greeks = Greeks
ageofheroes-tribe-babylonians = Babylonians
ageofheroes-tribe-celts = Celts
ageofheroes-tribe-chinese = Chinese

# Special Resources (for monuments)
ageofheroes-special-limestone = Limestone
ageofheroes-special-concrete = Concrete
ageofheroes-special-marble = Marble
ageofheroes-special-bricks = Bricks
ageofheroes-special-sandstone = Sandstone
ageofheroes-special-granite = Granite

# Standard Resources
ageofheroes-resource-iron = Iron
ageofheroes-resource-wood = Wood
ageofheroes-resource-grain = Grain
ageofheroes-resource-stone = Stone
ageofheroes-resource-gold = Gold

# Events
ageofheroes-event-population-growth = Population Growth
ageofheroes-event-earthquake = Earthquake
ageofheroes-event-eruption = Eruption
ageofheroes-event-hunger = Hunger
ageofheroes-event-barbarians = Barbarians
ageofheroes-event-olympics = Olympic Games
ageofheroes-event-hero = Hero
ageofheroes-event-fortune = Fortune

# Buildings
ageofheroes-building-army = Army
ageofheroes-building-fortress = Fortress
ageofheroes-building-general = General
ageofheroes-building-road = Road
ageofheroes-building-city = City

# Actions
ageofheroes-action-tax-collection = Tax Collection
ageofheroes-action-construction = Construction
ageofheroes-action-war = War
ageofheroes-action-do-nothing = Do Nothing

# War goals
ageofheroes-war-conquest = Conquest
ageofheroes-war-plunder = Plunder
ageofheroes-war-destruction = Destruction

# Game options
ageofheroes-set-victory-cities = Victory cities: { $cities }
ageofheroes-enter-victory-cities = Enter number of cities to win (3-7)
ageofheroes-set-victory-monument = Monument completion: { $progress }%
ageofheroes-toggle-neighbor-roads = Roads only to neighbors: { $enabled }
ageofheroes-set-max-hand = Maximum hand size: { $cards } cards

# Option change announcements
ageofheroes-option-changed-victory-cities = Victory requires { $cities } cities.
ageofheroes-option-changed-victory-monument = Monument completion threshold set to { $progress }%.
ageofheroes-option-changed-neighbor-roads = Roads only to neighbors { $enabled }.
ageofheroes-option-changed-max-hand = Maximum hand size set to { $cards } cards.

# Setup phase
ageofheroes-setup-start = You are the leader of the { $tribe } tribe. Your special monument resource is { $special }. Roll the dice to determine turn order.
ageofheroes-setup-viewer = Players are rolling dice to determine turn order.
ageofheroes-roll-dice = Roll the dice
ageofheroes-dice-result = You rolled { $total } ({ $die1 } + { $die2 }).
ageofheroes-dice-result-other = { $player } rolled { $total }.
ageofheroes-dice-tie = Multiple players tied with { $total }. Rolling again...
ageofheroes-first-player = { $player } rolled highest with { $total } and goes first!
ageofheroes-first-player-you = With { $total } points, you go first!

# Preparation phase
ageofheroes-prepare-start = Players must play event cards and discard disasters.
ageofheroes-prepare-your-turn = You have { $count } { $count ->
    [one] card
    *[other] cards
} to play or discard.
ageofheroes-prepare-done = Preparation phase complete.

# Events played/discarded
ageofheroes-population-growth = { $player } plays Population Growth and builds a new city.
ageofheroes-population-growth-you = You play Population Growth and build a new city.
ageofheroes-discard-card = { $player } discards { $card }.
ageofheroes-discard-card-you = You discard { $card }.
ageofheroes-earthquake = An earthquake strikes { $player }'s tribe; their armies go into recovery.
ageofheroes-earthquake-you = An earthquake strikes your tribe; your armies go into recovery.
ageofheroes-eruption = Aneruption destroys one of { $player }'s cities.
ageofheroes-eruption-you = An eruption destroys one of your cities.

# Fair phase
ageofheroes-fair-start = The day dawns at the marketplace. Players draw cards based on their road network.
ageofheroes-fair-draw = You draw { $count } { $count ->
    [one] card
    *[other] cards
} from the deck.
ageofheroes-fair-draw-other = { $player } draws { $count } { $count ->
    [one] card
    *[other] cards
}.

# Trading/Auction
ageofheroes-auction-start = Auction begins.
ageofheroes-offer-trade = Offer to trade
ageofheroes-offer-made = { $player } offers { $card } for { $wanted }.
ageofheroes-offer-made-you = You offer { $card } for { $wanted }.
ageofheroes-trade-accepted = { $player } accepts { $other }'s offer and trades { $give } for { $receive }.
ageofheroes-trade-accepted-you = You accept { $other }'s offer and receive { $receive }.
ageofheroes-trade-cancelled = { $player } withdraws their offer for { $card }.
ageofheroes-trade-cancelled-you = You withdraw your offer for { $card }.
ageofheroes-stop-trading = Stop Trading
ageofheroes-left-auction = { $player } departs.
ageofheroes-left-auction-you = You depart from the marketplace.
ageofheroes-any-card = Any card
ageofheroes-cannot-trade-own-special = You cannot trade your own special monument resource.
ageofheroes-resource-not-in-game = This special resource is not being used in this game.

# Main play phase
ageofheroes-play-start = Play phase.
ageofheroes-day = Day { $day }
ageofheroes-draw-card = { $player } draws a card from the deck.
ageofheroes-draw-card-you = You draw { $card } from the deck.
ageofheroes-your-action = What do you want to do?

# Tax Collection
ageofheroes-tax-collection = { $player } has { $cities } { $cities ->
    [one] city
    *[other] cities
} and collects { $cards } { $cards ->
    [one] card
    *[other] cards
}.
ageofheroes-tax-collection-you = You have { $cities } { $cities ->
    [one] city
    *[other] cities
} and collect { $cards } { $cards ->
    [one] card
    *[other] cards
}.
ageofheroes-tax-no-city = You have no surviving cities. Discard a card to draw a new one.
ageofheroes-tax-no-city-done = { $player } exchanged a card since they have no cities.
ageofheroes-tax-no-city-done-you = You exchanged { $card } for a new card.

# Construction
ageofheroes-construction-menu = What do you want to build?
ageofheroes-construction-done = { $player } built a { $building }.
ageofheroes-construction-done-you = You built a { $building }.
ageofheroes-construction-stop = Stop building
ageofheroes-construction-stopped = You decided to stop building.
ageofheroes-road-request = { $player } requests permission to build a road to your tribe. Accept?
ageofheroes-road-accepted = { $player } agreed to build a road with you.
ageofheroes-road-rejected = { $player } declined your road request.
ageofheroes-road-built = { $tribe1 } and { $tribe2 } are now connected by road.
ageofheroes-road-no-target = No neighboring tribes available for road construction.
ageofheroes-supply-exhausted = No more { $building } available to build.

# Do Nothing
ageofheroes-do-nothing = { $player } passes.
ageofheroes-do-nothing-you = You pass...

# War
ageofheroes-war-declare = { $attacker } declares war on { $defender }! Goal: { $goal }.
ageofheroes-war-prepare = Select your armies for { $action }.
ageofheroes-war-no-army = You have no armies available.
ageofheroes-war-select-armies = Select armies: { $count }
ageofheroes-war-select-generals = Select generals: { $count }
ageofheroes-war-select-heroes = Select heroes: { $count }
ageofheroes-war-attack = Attack...
ageofheroes-war-defend = Defend...
ageofheroes-war-prepared = Your forces: { $armies } { $armies ->
    [one] army
    *[other] armies
}{ $generals ->
    [0] {""}
    [one] {" and 1 general"}
    *[other] {" and { $generals } generals"}
}{ $heroes ->
    [0] {""}
    [one] {" and 1 hero"}
    *[other] {" and { $heroes } heroes"}
}.

# Battle
ageofheroes-battle-start = { $attacker }'s { $attack_armies } { $attack_armies ->
    [one] army
    *[other] armies
} attacks { $defender }'s { $defend_armies } { $defend_armies ->
    [one] army
    *[other] armies
}!
ageofheroes-battle-defenseless = { $attacker }'s { $attack_armies } { $attack_armies ->
    [one] army
    *[other] armies
} attacks the defenseless { $defender }! The outcome is certain...
ageofheroes-dice-roll = { $player } rolls { $total }{ $bonus ->
    [0] {""}
    *[other] { " (+{ $bonus } from bonuses)" }
}.
ageofheroes-dice-roll-you = You roll { $total }{ $bonus ->
    [0] {""}
    *[other] { " (+{ $bonus } from bonuses)" }
}.
ageofheroes-general-bonus = +{ $count } from { $count ->
    [one] general
    *[other] generals
}
ageofheroes-fortress-bonus = +{ $count } from fortress defense
ageofheroes-battle-winner = { $winner } wins the battle.
ageofheroes-battle-draw = The battle ends in a draw...
ageofheroes-battle-continue = Continue the battle.
ageofheroes-battle-end = The battle is over.

# War outcomes
ageofheroes-conquest-success = { $attacker } conquers one of { $defender }'s cities.
ageofheroes-plunder-success = { $attacker } plunders { $count } { $count ->
    [one] card
    *[other] cards
} from { $defender }.
ageofheroes-destruction-success = { $attacker } destroys { $defender }'s monument progress.
ageofheroes-army-losses = { $player } loses { $count } { $count ->
    [one] army
    *[other] armies
}.
ageofheroes-army-losses-you = You lose { $count } { $count ->
    [one] army
    *[other] armies
}.

# Army return
ageofheroes-army-return-road = Your troops return immediately via road.
ageofheroes-army-return-delayed = { $count } { $count ->
    [one] unit returns
    *[other] units return
} at the end of your next turn.
ageofheroes-army-returned = { $player }'s troops have returned from war.
ageofheroes-army-returned-you = Your troops have returned from war.
ageofheroes-army-recover = { $player }'s armies recover from the earthquake.
ageofheroes-army-recover-you = Your armies recover from the earthquake.

# Olympics
ageofheroes-olympics-cancel = { $player } plays Olympic Games. The armies are much too interested in watching these games, so they accidentally forget to fight each other.
ageofheroes-olympics-prompt = { $attacker } has declared war! You have Olympic Games - use it to cancel?
ageofheroes-yes = Yes
ageofheroes-no = No

# Monument progress
ageofheroes-monument-progress = { $player }'s monument is { $percent }% complete ({ $count }/5).
ageofheroes-monument-progress-you = Your monument is { $percent }% complete ({ $count }/5).

# Hand management
ageofheroes-discard-excess = You have more than { $max } cards. Discard { $count } { $count ->
    [one] card
    *[other] cards
}.
ageofheroes-discard-excess-other = { $player } must discard excess cards.

# Victory
ageofheroes-victory-cities = { $player } has built 5 cities! Empire of Five Cities.
ageofheroes-victory-cities-you = You have built 5 cities! Empire of Five Cities.
ageofheroes-victory-monument = { $player } has completed their monument! Carriers of Great Culture.
ageofheroes-victory-monument-you = You have completed your monument! Carriers of Great Culture.
ageofheroes-victory-last-standing = { $player } is the last tribe standing! The Most Persistent.
ageofheroes-victory-last-standing-you = You are the last tribe standing! The Most Persistent.
ageofheroes-game-over = Game Over.

# Elimination
ageofheroes-eliminated = { $player } has been eliminated.
ageofheroes-eliminated-you = You have been eliminated.

# Status
ageofheroes-status = { $player } ({ $tribe }): { $cities } { $cities ->
    [one] city
    *[other] cities
}, { $armies } { $armies ->
    [one] army
    *[other] armies
}, { $monument }/5 monument
ageofheroes-status-detailed-header = { $player } ({ $tribe })
ageofheroes-status-cities = Cities: { $count }
ageofheroes-status-armies = Armies: { $count }
ageofheroes-status-generals = Generals: { $count }
ageofheroes-status-fortresses = Fortresses: { $count }
ageofheroes-status-monument = Monument: { $count }/5 ({ $percent }%)
ageofheroes-status-roads = Roads: { $left }{ $right }
ageofheroes-status-road-left = left
ageofheroes-status-road-right = right
ageofheroes-status-none = none
ageofheroes-status-earthquake-armies = Recovering armies: { $count }
ageofheroes-status-returning-armies = Returning armies: { $count }
ageofheroes-status-returning-generals = Returning generals: { $count }

# Deck info
ageofheroes-deck-empty = No more { $card } cards in the deck.
ageofheroes-deck-count = Cards remaining: { $count }
ageofheroes-deck-reshuffled = The discard pile has been reshuffled into the deck.

# Give up
ageofheroes-give-up-confirm = Are you sure you want to give up?
ageofheroes-gave-up = { $player } gave up!
ageofheroes-gave-up-you = You gave up!

# Hero card
ageofheroes-hero-use = Use as army or general?
ageofheroes-hero-army = Army
ageofheroes-hero-general = General

# Fortune card
ageofheroes-fortune-reroll = { $player } uses Fortune to reroll!
ageofheroes-fortune-prompt = You lost the roll. Use Fortune to reroll?

# Disabled action reasons
ageofheroes-not-your-turn = It's not your turn.
ageofheroes-game-not-started = The game hasn't started yet.
ageofheroes-wrong-phase = This action is not available in the current phase.
ageofheroes-no-resources = You don't have the required resources.

# Building costs (for display)
ageofheroes-cost-army = Iron + 2 Grain
ageofheroes-cost-fortress = Iron + Wood + Stone
ageofheroes-cost-general = Iron + Gold
ageofheroes-cost-road = 2 Stone
ageofheroes-cost-city = 2 Wood + Stone
