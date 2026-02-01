# Yahtzee 游戏消息 (简体中文)

# 游戏信息
game-name-yahtzee = 快艇骰子

# 操作 - 掷骰
yahtzee-roll = 重掷（剩余 { $count } 次）
yahtzee-roll-all = 掷骰子

# 上半部分计分类别
yahtzee-score-ones = 一点得 { $points } 分
yahtzee-score-twos = 二点得 { $points } 分
yahtzee-score-threes = 三点得 { $points } 分
yahtzee-score-fours = 四点得 { $points } 分
yahtzee-score-fives = 五点得 { $points } 分
yahtzee-score-sixes = 六点得 { $points } 分

# 下半部分计分类别
yahtzee-score-three-kind = 三条得 { $points } 分
yahtzee-score-four-kind = 四条得 { $points } 分
yahtzee-score-full-house = 葫芦得 { $points } 分
yahtzee-score-small-straight = 小顺子得 { $points } 分
yahtzee-score-large-straight = 大顺子得 { $points } 分
yahtzee-score-yahtzee = Yahtzee得 { $points } 分
yahtzee-score-chance = 机会得 { $points } 分

# 游戏事件
yahtzee-you-rolled = 你掷出了：{ $dice }。剩余掷骰次数：{ $remaining }
yahtzee-player-rolled = { $player } 掷出了：{ $dice }。剩余掷骰次数：{ $remaining }

# 计分公告
yahtzee-you-scored = 你在 { $category } 得了 { $points } 分。
yahtzee-player-scored = { $player } 在 { $category } 得了 { $points } 分。

# Yahtzee奖励
yahtzee-you-bonus = Yahtzee奖励！+100分
yahtzee-player-bonus = { $player } 获得了Yahtzee奖励！+100分

# 上半部分奖励
yahtzee-you-upper-bonus = 上半部分奖励！+35分（上半部分共 { $total } 分）
yahtzee-player-upper-bonus = { $player } 获得了上半部分奖励！+35分
yahtzee-you-upper-bonus-missed = 你错过了上半部分奖励（上半部分 { $total } 分，需要63分）。
yahtzee-player-upper-bonus-missed = { $player } 错过了上半部分奖励。

# 计分模式
yahtzee-choose-category = 选择一个类别计分。
yahtzee-continuing = 继续回合。

# 状态检查
yahtzee-check-scoresheet = 查看计分卡
yahtzee-view-dice = 查看手牌
yahtzee-your-dice = 你的骰子：{ $dice }。
yahtzee-your-dice-kept = 你的骰子：{ $dice }。保留：{ $kept }
yahtzee-not-rolled = 你还没有掷骰子。

# 计分卡显示
yahtzee-scoresheet-header = { $player } 的计分卡
yahtzee-scoresheet-upper = 上半部分：
yahtzee-scoresheet-lower = 下半部分：
yahtzee-scoresheet-category-filled = { $category }：{ $points }
yahtzee-scoresheet-category-open = { $category }：-
yahtzee-scoresheet-upper-total-bonus = 上半部分总计：{ $total }（奖励：+35）
yahtzee-scoresheet-upper-total-needed = 上半部分总计：{ $total }（还需 { $needed } 分获得奖励）
yahtzee-scoresheet-yahtzee-bonus = Yahtzee奖励：{ $count } x 100 = { $total }
yahtzee-scoresheet-grand-total = 总分：{ $total }

# 类别名称（用于公告）
yahtzee-category-ones = 一点
yahtzee-category-twos = 二点
yahtzee-category-threes = 三点
yahtzee-category-fours = 四点
yahtzee-category-fives = 五点
yahtzee-category-sixes = 六点
yahtzee-category-three-kind = 三条
yahtzee-category-four-kind = 四条
yahtzee-category-full-house = 葫芦
yahtzee-category-small-straight = 小顺子
yahtzee-category-large-straight = 大顺子
yahtzee-category-yahtzee = Yahtzee
yahtzee-category-chance = 机会

# 游戏结束
yahtzee-winner = { $player } 以 { $score } 分获胜！
yahtzee-winners-tie = 平局！{ $players } 都获得了 { $score } 分！

# 选项
yahtzee-set-rounds = 游戏局数：{ $rounds }
yahtzee-enter-rounds = 输入游戏局数（1-10）：
yahtzee-option-changed-rounds = 游戏局数设置为 { $rounds }。

# 操作禁用原因
yahtzee-no-rolls-left = 你没有掷骰次数了。
yahtzee-roll-first = 你需要先掷骰子。
yahtzee-category-filled = 该类别已经填写。
