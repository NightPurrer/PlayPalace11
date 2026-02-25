# Age of Heroes game messages
# A civilization-building card game for 2-6 players

# Game name
game-name-ageofheroes = 英雄时代

# Tribes
ageofheroes-tribe-egyptians = 埃及人
ageofheroes-tribe-romans = 罗马人
ageofheroes-tribe-greeks = 希腊人
ageofheroes-tribe-babylonians = 巴比伦人
ageofheroes-tribe-celts = 凯尔特人
ageofheroes-tribe-chinese = 中国人

# Special Resources (for monuments)
ageofheroes-special-limestone = 石灰石
ageofheroes-special-concrete = 混凝土
ageofheroes-special-marble = 大理石
ageofheroes-special-bricks = 砖块
ageofheroes-special-sandstone = 砂岩
ageofheroes-special-granite = 花岗岩

# Standard Resources
ageofheroes-resource-iron = 铁
ageofheroes-resource-wood = 木材
ageofheroes-resource-grain = 粮食
ageofheroes-resource-stone = 石头
ageofheroes-resource-gold = 黄金

# Events
ageofheroes-event-population-growth = 人口增长
ageofheroes-event-earthquake = 地震
ageofheroes-event-eruption = 火山喷发
ageofheroes-event-hunger = 饥荒
ageofheroes-event-barbarians = 野蛮人
ageofheroes-event-olympics = 奥林匹克运动会
ageofheroes-event-hero = 英雄
ageofheroes-event-fortune = 命运

# Buildings
ageofheroes-building-army = 军队
ageofheroes-building-fortress = 要塞
ageofheroes-building-general = 将军
ageofheroes-building-road = 道路
ageofheroes-building-city = 城市

# Actions
ageofheroes-action-tax-collection = 征税
ageofheroes-action-construction = 建设
ageofheroes-action-war = 战争
ageofheroes-action-do-nothing = 什么都不做
ageofheroes-play = 出牌

# War goals
ageofheroes-war-conquest = 征服
ageofheroes-war-plunder = 掠夺
ageofheroes-war-destruction = 毁灭

# Game options
ageofheroes-set-victory-cities = 胜利城市数：{ $cities }
ageofheroes-enter-victory-cities = 输入获胜所需的城市数量（3-7）
ageofheroes-set-victory-monument = 纪念碑完成度：{ $progress }%
ageofheroes-toggle-neighbor-roads = 仅建造通向邻居的道路：{ $enabled }
ageofheroes-set-max-hand = 最大手牌数：{ $cards }张

# Option change announcements
ageofheroes-option-changed-victory-cities = 胜利需要{ $cities }座城市。
ageofheroes-option-changed-victory-monument = 纪念碑完成度阈值设置为{ $progress }%。
ageofheroes-option-changed-neighbor-roads = 仅建造通向邻居的道路{ $enabled }。
ageofheroes-option-changed-max-hand = 最大手牌数设置为{ $cards }张。

# Setup phase
ageofheroes-setup-start = 你是{ $tribe }部落的领袖。你的特殊纪念碑资源是{ $special }。掷骰子来决定回合顺序。
ageofheroes-setup-viewer = 玩家正在掷骰子决定回合顺序。
ageofheroes-roll-dice = 掷骰子
ageofheroes-war-roll-dice = 掷骰子
ageofheroes-dice-result = 你掷出了{ $total }（{ $die1 } + { $die2 }）。
ageofheroes-dice-result-other = { $player }掷出了{ $total }。
ageofheroes-dice-tie = 多名玩家以{ $total }平局。重新掷骰子...
ageofheroes-first-player = { $player }掷出最高点数{ $total }，先手行动。
ageofheroes-first-player-you = 以{ $total }点，你先手行动。

# Preparation phase
ageofheroes-prepare-start = 玩家必须打出事件卡并弃掉灾难卡。
ageofheroes-prepare-your-turn = 你有{ $count }{ $count ->
    [one] 张卡牌
    *[other] 张卡牌
}可以打出或弃掉。
ageofheroes-prepare-done = 准备阶段完成。

# Events played/discarded
ageofheroes-population-growth = { $player }打出人口增长并建造一座新城市。
ageofheroes-population-growth-you = 你打出人口增长并建造一座新城市。
ageofheroes-discard-card = { $player }弃掉{ $card }。
ageofheroes-discard-card-you = 你弃掉{ $card }。
ageofheroes-earthquake = 地震袭击了{ $player }的部落；他们的军队进入恢复状态。
ageofheroes-earthquake-you = 地震袭击了你的部落；你的军队进入恢复状态。
ageofheroes-eruption = 火山喷发摧毁了{ $player }的一座城市。
ageofheroes-eruption-you = 火山喷发摧毁了你的一座城市。

# Disaster effects
ageofheroes-hunger-strikes = 饥荒来袭。
ageofheroes-lose-card-hunger = 你失去{ $card }。
ageofheroes-barbarians-pillage = 野蛮人攻击{ $player }的资源。
ageofheroes-barbarians-attack = 野蛮人攻击{ $player }的资源。
ageofheroes-barbarians-attack-you = 野蛮人攻击你的资源。
ageofheroes-lose-card-barbarians = 你失去{ $card }。
ageofheroes-block-with-card = { $player }使用{ $card }阻止了灾难。
ageofheroes-block-with-card-you = 你使用{ $card }阻止了灾难。

# Targeted disaster cards (Earthquake/Eruption)
ageofheroes-select-disaster-target = 选择{ $card }的目标。
ageofheroes-no-targets = 没有有效目标可用。
ageofheroes-earthquake-strikes-you = { $attacker }对你使用地震。你的军队被禁用。
ageofheroes-earthquake-strikes = { $attacker }对{ $player }使用地震。
ageofheroes-armies-disabled = { $count }{ $count ->
    [one] 支军队
    *[other] 支军队
}被禁用一回合。
ageofheroes-eruption-strikes-you = { $attacker }对你使用火山喷发。你的一座城市被摧毁。
ageofheroes-eruption-strikes = { $attacker }对{ $player }使用火山喷发。
ageofheroes-city-destroyed = 一座城市被火山喷发摧毁。

# Fair phase
ageofheroes-fair-start = 市场的一天开始了。
ageofheroes-fair-draw-base = 你抽取{ $count }{ $count ->
    [one] 张卡牌
    *[other] 张卡牌
}。
ageofheroes-fair-draw-roads = 由于你的道路网络，你额外抽取{ $count }{ $count ->
    [one] 张卡牌
    *[other] 张卡牌
}。
ageofheroes-fair-draw-other = { $player }抽取{ $count }{ $count ->
    [one] 张卡牌
    *[other] 张卡牌
}。

# Trading/Auction
ageofheroes-auction-start = 拍卖开始。
ageofheroes-offer-trade = 提出交易
ageofheroes-offer-made = { $player }提出用{ $card }交换{ $wanted }。
ageofheroes-offer-made-you = 你提出用{ $card }交换{ $wanted }。
ageofheroes-trade-accepted = { $player }接受{ $other }的提议，用{ $give }交换{ $receive }。
ageofheroes-trade-accepted-you = 你接受{ $other }的提议并获得{ $receive }。
ageofheroes-trade-cancelled = { $player }撤回了对{ $card }的提议。
ageofheroes-trade-cancelled-you = 你撤回了对{ $card }的提议。
ageofheroes-stop-trading = 停止交易
ageofheroes-select-request = 你正在提供{ $card }。你想要什么作为交换？
ageofheroes-cancel = 取消
ageofheroes-left-auction = { $player }离开了。
ageofheroes-left-auction-you = 你离开了市场。
ageofheroes-any-card = 任意卡牌
ageofheroes-cannot-trade-own-special = 你不能交易你自己的特殊纪念碑资源。
ageofheroes-resource-not-in-game = 这个特殊资源在本局游戏中未使用。

# Main play phase
ageofheroes-play-start = 游戏阶段。
ageofheroes-day = 第{ $day }天
ageofheroes-draw-card = { $player }从牌堆抽一张卡牌。
ageofheroes-draw-card-you = 你从牌堆抽到{ $card }。
ageofheroes-your-action = 你想做什么？

# Tax Collection
ageofheroes-tax-collection = { $player }选择征税：{ $cities }{ $cities ->
    [one] 座城市
    *[other] 座城市
}收集{ $cards }{ $cards ->
    [one] 张卡牌
    *[other] 张卡牌
}。
ageofheroes-tax-collection-you = 你选择征税：{ $cities }{ $cities ->
    [one] 座城市
    *[other] 座城市
}收集{ $cards }{ $cards ->
    [one] 张卡牌
    *[other] 张卡牌
}。
ageofheroes-tax-no-city = 征税：你没有幸存的城市。弃掉一张卡牌以抽取新卡。
ageofheroes-tax-no-city-done = { $player }选择征税但没有城市，因此交换了一张卡牌。
ageofheroes-tax-no-city-done-you = 征税：你用{ $card }交换了一张新卡牌。

# Construction
ageofheroes-construction-menu = 你想建造什么？
ageofheroes-construction-done = { $player }建造了{ $article }{ $building }。
ageofheroes-construction-done-you = 你建造了{ $article }{ $building }。
ageofheroes-construction-stop = 停止建造
ageofheroes-construction-stopped = 你决定停止建造。
ageofheroes-road-select-neighbor = 选择要建造道路通往哪个邻居。
ageofheroes-direction-left = 你的左边
ageofheroes-direction-right = 你的右边
ageofheroes-road-request-sent = 道路请求已发送。等待邻居批准。
ageofheroes-road-request-received = { $requester }请求允许建造通往你部落的道路。
ageofheroes-road-request-denied-you = 你拒绝了道路请求。
ageofheroes-road-request-denied = { $denier }拒绝了你的道路请求。
ageofheroes-road-built = { $tribe1 }和{ $tribe2 }现在通过道路连接。
ageofheroes-road-no-target = 没有相邻部落可用于建造道路。
ageofheroes-approve = 批准
ageofheroes-deny = 拒绝
ageofheroes-supply-exhausted = 没有更多{ $building }可供建造。

# Do Nothing
ageofheroes-do-nothing = { $player }跳过。
ageofheroes-do-nothing-you = 你跳过...

# War
ageofheroes-war-declare = { $attacker }向{ $defender }宣战。目标：{ $goal }。
ageofheroes-war-prepare = 选择你的军队进行{ $action }。
ageofheroes-war-no-army = 你没有可用的军队或英雄卡。
ageofheroes-war-no-targets = 没有有效的战争目标。
ageofheroes-war-no-valid-goal = 对此目标没有有效的战争目标。
ageofheroes-war-select-target = 选择要攻击的玩家。
ageofheroes-war-select-goal = 选择你的战争目标。
ageofheroes-war-prepare-attack = 选择你的进攻部队。
ageofheroes-war-prepare-defense = { $attacker }正在攻击你；选择你的防御部队。
ageofheroes-war-select-armies = 选择军队：{ $count }
ageofheroes-war-select-generals = 选择将军：{ $count }
ageofheroes-war-select-heroes = 选择英雄：{ $count }
ageofheroes-war-attack = 攻击...
ageofheroes-war-defend = 防御...
ageofheroes-war-prepared = 你的部队：{ $armies }{ $armies ->
    [one] 支军队
    *[other] 支军队
}{ $generals ->
    [0] {""}
    [one] {"和1名将军"}
    *[other] {"和{ $generals }名将军"}
}{ $heroes ->
    [0] {""}
    [one] {"和1名英雄"}
    *[other] {"和{ $heroes }名英雄"}
}。
ageofheroes-war-roll-you = 你掷出{ $roll }。
ageofheroes-war-roll-other = { $player }掷出{ $roll }。
ageofheroes-war-bonuses-you = { $general ->
    [0] { $fortress ->
        [0] {""}
        [1] 要塞+1 = 总计{ $total }
        *[other] 要塞+{ $fortress } = 总计{ $total }
    }
    *[other] { $fortress ->
        [0] 将军+{ $general } = 总计{ $total }
        [1] 将军+{ $general }，要塞+1 = 总计{ $total }
        *[other] 将军+{ $general }，要塞+{ $fortress } = 总计{ $total }
    }
}
ageofheroes-war-bonuses-other = { $general ->
    [0] { $fortress ->
        [0] {""}
        [1] { $player }：要塞+1 = 总计{ $total }
        *[other] { $player }：要塞+{ $fortress } = 总计{ $total }
    }
    *[other] { $fortress ->
        [0] { $player }：将军+{ $general } = 总计{ $total }
        [1] { $player }：将军+{ $general }，要塞+1 = 总计{ $total }
        *[other] { $player }：将军+{ $general }，要塞+{ $fortress } = 总计{ $total }
    }
}

# Battle
ageofheroes-battle-start = 战斗开始。{ $attacker }的{ $att_armies }{ $att_armies ->
    [one] 支军队
    *[other] 支军队
}对阵{ $defender }的{ $def_armies }{ $def_armies ->
    [one] 支军队
    *[other] 支军队
}。
ageofheroes-dice-roll-detailed = { $name }掷出{ $dice }{ $general ->
    [0] {""}
    *[other] { " + 将军{ $general }" }
}{ $fortress ->
    [0] {""}
    [one] { " + 要塞1" }
    *[other] { " + 要塞{ $fortress }" }
} = { $total }。
ageofheroes-dice-roll-detailed-you = 你掷出{ $dice }{ $general ->
    [0] {""}
    *[other] { " + 将军{ $general }" }
}{ $fortress ->
    [0] {""}
    [one] { " + 要塞1" }
    *[other] { " + 要塞{ $fortress }" }
} = { $total }。
ageofheroes-round-attacker-wins = { $attacker }赢得这回合（{ $att_total } vs { $def_total }）。{ $defender }失去一支军队。
ageofheroes-round-defender-wins = { $defender }成功防御（{ $def_total } vs { $att_total }）。{ $attacker }失去一支军队。
ageofheroes-round-draw = 双方平局{ $total }。没有军队损失。
ageofheroes-battle-victory-attacker = { $attacker }击败{ $defender }。
ageofheroes-battle-victory-defender = { $defender }成功抵御{ $attacker }。
ageofheroes-battle-mutual-defeat = { $attacker }和{ $defender }都失去所有军队。
ageofheroes-general-bonus = +{ $count }来自{ $count ->
    [one] 将军
    *[other] 将军
}
ageofheroes-fortress-bonus = +{ $count }来自要塞防御
ageofheroes-battle-winner = { $winner }赢得战斗。
ageofheroes-battle-draw = 战斗以平局结束...
ageofheroes-battle-continue = 继续战斗。
ageofheroes-battle-end = 战斗结束。

# War outcomes
ageofheroes-conquest-success = { $attacker }从{ $defender }征服{ $count }{ $count ->
    [one] 座城市
    *[other] 座城市
}。
ageofheroes-plunder-success = { $attacker }从{ $defender }掠夺{ $count }{ $count ->
    [one] 张卡牌
    *[other] 张卡牌
}。
ageofheroes-destruction-success = { $attacker }摧毁{ $defender }的{ $count }{ $count ->
    [one] 个纪念碑资源
    *[other] 个纪念碑资源
}。
ageofheroes-army-losses = { $player }失去{ $count }{ $count ->
    [one] 支军队
    *[other] 支军队
}。
ageofheroes-army-losses-you = 你失去{ $count }{ $count ->
    [one] 支军队
    *[other] 支军队
}。

# Army return
ageofheroes-army-return-road = 你的部队立即通过道路返回。
ageofheroes-army-return-delayed = { $count }{ $count ->
    [one] 个单位
    *[other] 个单位
}将在你的下一回合结束时返回。
ageofheroes-army-returned = { $player }的部队已从战争中返回。
ageofheroes-army-returned-you = 你的部队已从战争中返回。
ageofheroes-army-recover = { $player }的军队从地震中恢复。
ageofheroes-army-recover-you = 你的军队从地震中恢复。

# Olympics
ageofheroes-olympics-cancel = { $player }打出奥林匹克运动会。战争取消。
ageofheroes-olympics-prompt = { $attacker }已宣战。你有奥林匹克运动会 - 使用它来取消吗？
ageofheroes-yes = 是
ageofheroes-no = 否

# Monument progress
ageofheroes-monument-progress = { $player }的纪念碑完成度为{ $count }/5。
ageofheroes-monument-progress-you = 你的纪念碑完成度为{ $count }/5。

# Hand management
ageofheroes-discard-excess = 你有超过{ $max }张卡牌。弃掉{ $count }{ $count ->
    [one] 张卡牌
    *[other] 张卡牌
}。
ageofheroes-discard-excess-other = { $player }必须弃掉多余的卡牌。
ageofheroes-discard-more = 再弃掉{ $count }{ $count ->
    [one] 张卡牌
    *[other] 张卡牌
}。

# Victory
ageofheroes-victory-cities = { $player }建造了5座城市！五城帝国。
ageofheroes-victory-cities-you = 你建造了5座城市！五城帝国。
ageofheroes-victory-monument = { $player }完成了他们的纪念碑！伟大文化的传承者。
ageofheroes-victory-monument-you = 你完成了你的纪念碑！伟大文化的传承者。
ageofheroes-victory-last-standing = { $player }是最后幸存的部落！最坚韧者。
ageofheroes-victory-last-standing-you = 你是最后幸存的部落！最坚韧者。
ageofheroes-game-over = 游戏结束。

# Elimination
ageofheroes-eliminated = { $player }被淘汰。
ageofheroes-eliminated-you = 你被淘汰了。

# Hand
ageofheroes-hand-empty = 你没有卡牌。
ageofheroes-hand-contents = 你的手牌（{ $count }{ $count ->
    [one] 张卡牌
    *[other] 张卡牌
}）：{ $cards }

# Status
ageofheroes-status = { $player }（{ $tribe }）：{ $cities }{ $cities ->
    [one] 座城市
    *[other] 座城市
}，{ $armies }{ $armies ->
    [one] 支军队
    *[other] 支军队
}，纪念碑{ $monument }/5
ageofheroes-status-detailed-header = { $player }（{ $tribe }）
ageofheroes-status-cities = 城市：{ $count }
ageofheroes-status-armies = 军队：{ $count }
ageofheroes-status-generals = 将军：{ $count }
ageofheroes-status-fortresses = 要塞：{ $count }
ageofheroes-status-monument = 纪念碑：{ $count }/5
ageofheroes-status-roads = 道路：{ $left }{ $right }
ageofheroes-status-road-left = 左
ageofheroes-status-road-right = 右
ageofheroes-status-none = 无
ageofheroes-status-earthquake-armies = 恢复中的军队：{ $count }
ageofheroes-status-returning-armies = 返回中的军队：{ $count }
ageofheroes-status-returning-generals = 返回中的将军：{ $count }

# Deck info
ageofheroes-deck-empty = 牌堆中没有更多{ $card }卡牌。
ageofheroes-deck-count = 剩余卡牌：{ $count }
ageofheroes-deck-reshuffled = 弃牌堆已被洗入牌堆。

# Give up
ageofheroes-give-up-confirm = 你确定要放弃吗？
ageofheroes-gave-up = { $player }放弃了！
ageofheroes-gave-up-you = 你放弃了！

# Hero card
ageofheroes-hero-use = 用作军队还是将军？
ageofheroes-hero-army = 军队
ageofheroes-hero-general = 将军

# Fortune card
ageofheroes-fortune-reroll = { $player }使用命运重新掷骰子。
ageofheroes-fortune-prompt = 你输掉了掷骰。使用命运重新掷骰吗？

# Disabled action reasons
ageofheroes-not-your-turn = 还没到你的回合。
ageofheroes-game-not-started = 游戏尚未开始。
ageofheroes-wrong-phase = 此操作在当前阶段不可用。
ageofheroes-no-resources = 你没有所需的资源。

# Building costs (for display)
ageofheroes-cost-army = 2粮食，铁
ageofheroes-cost-fortress = 铁，木材，石头
ageofheroes-cost-general = 铁，黄金
ageofheroes-cost-road = 2石头
ageofheroes-cost-city = 2木材，石头
