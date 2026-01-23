# Thông báo trò chơi Pig
# Lưu ý: Các thông báo chung như bắt đầu vòng, bắt đầu lượt, điểm mục tiêu nằm trong games.ftl

# Thông tin game
game-name-pig = Pig
pig-category = Game Xúc Xắc

# Hành động
pig-roll = Gieo xúc xắc
pig-bank = Chốt { $points } điểm

# Sự kiện trong game (Riêng cho Pig)
pig-rolls = { $player } gieo xúc xắc...
pig-roll-result = Ra { $roll }, tổng điểm lượt này là { $total }
pig-bust = Ôi không, gieo phải con 1! { $player } mất sạch { $points } điểm.
pig-bank-action = { $player } quyết định chốt { $points } điểm, nâng tổng điểm lên { $total }
pig-winner = Chúng ta đã có người chiến thắng, đó là { $player }!

# Tùy chọn riêng cho Pig
pig-set-min-bank = Điểm chốt tối thiểu: { $points }
pig-set-dice-sides = Số mặt xúc xắc: { $sides }
pig-enter-min-bank = Nhập số điểm tối thiểu để được chốt:
pig-enter-dice-sides = Nhập số mặt của xúc xắc:
pig-option-changed-min-bank = Điểm chốt tối thiểu đã đổi thành { $points }
pig-option-changed-dice = Xúc xắc giờ có { $sides } mặt

# Lý do hành động bị vô hiệu hóa
pig-need-more-points = Bạn cần thêm điểm mới được chốt.

# Lỗi xác thực
pig-error-min-bank-too-high = Điểm chốt tối thiểu phải thấp hơn điểm mục tiêu thắng.
