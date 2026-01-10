# Chaos Bear 游戏消息 (简体中文)

# 游戏名称
game-name-chaosbear = 混沌熊

# 操作
chaosbear-roll-dice = 掷骰子
chaosbear-draw-card = 抽一张牌
chaosbear-check-status = 查看状态

# 游戏介绍（3条独立消息，如v10）
chaosbear-intro-1 = 混沌熊开始了！所有玩家从熊前方30格处出发。
chaosbear-intro-2 = 掷骰子向前移动，在5的倍数格时抽牌获得特殊效果。
chaosbear-intro-3 = 不要让熊抓住你！

# 回合公告
chaosbear-turn = { $player } 的回合；第 { $position } 格。

# 掷骰
chaosbear-roll = { $player } 掷出了 { $roll }。
chaosbear-position = { $player } 现在在第 { $position } 格。

# 抽牌
chaosbear-draws-card = { $player } 抽了一张牌。
chaosbear-card-impulsion = 冲刺！{ $player } 向前移动3格到第 { $position } 格！
chaosbear-card-super-impulsion = 超级冲刺！{ $player } 向前移动5格到第 { $position } 格！
chaosbear-card-tiredness = 疲劳！熊的能量减1。现在有 { $energy } 点能量。
chaosbear-card-hunger = 饥饿！熊的能量加1。现在有 { $energy } 点能量。
chaosbear-card-backward = 后推！{ $player } 退回到第 { $position } 格。
chaosbear-card-random-gift = 随机礼物！
chaosbear-gift-back = { $player } 退到了第 { $position } 格。
chaosbear-gift-forward = { $player } 前进到了第 { $position } 格！

# 熊的回合
chaosbear-bear-roll = 熊掷出了 { $roll } + { $energy } 点能量 = { $total }。
chaosbear-bear-energy-up = 熊掷出了3，获得1点能量！
chaosbear-bear-position = 熊现在在第 { $position } 格！
chaosbear-player-caught = 熊抓住了 { $player }！{ $player } 被淘汰了！
chaosbear-bear-feast = 熊在饱餐一顿后失去了3点能量！

# 状态检查
chaosbear-status-player-alive = { $player }：第 { $position } 格。
chaosbear-status-player-caught = { $player }：在第 { $position } 格被抓。
chaosbear-status-bear = 熊在第 { $position } 格，有 { $energy } 点能量。

# 游戏结束
chaosbear-winner = { $player } 存活并获胜！到达了第 { $position } 格！
chaosbear-tie = 在第 { $position } 格平局！

# 操作禁用原因
chaosbear-you-are-caught = 你已经被熊抓住了。
chaosbear-not-on-multiple = 你只能在5的倍数格时抽牌。
