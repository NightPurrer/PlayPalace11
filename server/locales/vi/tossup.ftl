# Thông báo trò chơi Toss Up
# Lưu ý: Các thông báo chung như bắt đầu vòng, bắt đầu lượt, điểm mục tiêu nằm trong games.ftl

# Thông tin game
game-name-tossup = Toss Up
tossup-category = Game Xúc Xắc

# Hành động
tossup-roll-first = Gieo { $count } viên
tossup-roll-remaining = Gieo tiếp { $count } viên còn lại
tossup-bank = Chốt { $points } điểm

# Sự kiện trong game
tossup-turn-start = Lượt của { $player }. Điểm: { $score }
tossup-you-roll = Bạn gieo được: { $results }.
tossup-player-rolls = { $player } gieo được: { $results }.

# Trạng thái lượt
tossup-you-have-points = Điểm lượt này: { $turn_points }. Còn lại: { $dice_count } viên.
tossup-player-has-points = { $player } được { $turn_points } điểm lượt này. Còn { $dice_count } viên.

# Xúc xắc mới (khi gieo hết số viên hiện có)
tossup-you-get-fresh = Hết xúc xắc! Nhận { $count } viên mới.
tossup-player-gets-fresh = { $player } nhận { $count } viên mới.

# Cháy điểm (Bust)
tossup-you-bust = Cháy điểm! Bạn mất { $points } điểm của lượt này.
tossup-player-busts = { $player } bị cháy điểm và mất { $points } điểm!

# Chốt điểm
tossup-you-bank = Bạn chốt { $points } điểm. Tổng điểm: { $total }.
tossup-player-banks = { $player } chốt { $points } điểm. Tổng điểm: { $total }.

# Người thắng
tossup-winner = { $player } thắng với { $score } điểm!
tossup-tie-tiebreaker = Hòa giữa { $players }! Vào vòng phân định thắng thua!

# Tùy chọn
tossup-set-rules-variant = Biến thể luật: { $variant }
tossup-select-rules-variant = Chọn biến thể luật:
tossup-option-changed-rules = Biến thể luật đã đổi thành { $variant }

tossup-set-starting-dice = Số xúc xắc khởi đầu: { $count }
tossup-enter-starting-dice = Nhập số lượng xúc xắc khởi đầu:
tossup-option-changed-dice = Số xúc xắc khởi đầu đã đổi thành { $count }

# Các biến thể luật
tossup-rules-standard = Tiêu chuẩn
tossup-rules-playpalace = PlayPalace

# Giải thích luật
tossup-rules-standard-desc = Mỗi viên có 3 mặt Xanh, 2 Vàng, 1 Đỏ. Cháy điểm nếu không có mặt Xanh nào và có ít nhất một mặt Đỏ.
tossup-rules-playpalace-desc = Phân bố các mặt đều nhau. Cháy điểm nếu tất cả xúc xắc đều ra màu Đỏ.

# Lý do hành động bị vô hiệu hóa
tossup-need-points = Bạn cần có điểm mới được chốt.
