# Thông báo trò chơi Farkle

# Thông tin game
game-name-farkle = Farkle

# Hành động - Gieo và Chốt
farkle-roll = Gieo { $count } { $count ->
    [one] viên
   *[other] viên
}
farkle-bank = Chốt { $points } điểm

# Hành động chọn tổ hợp điểm (khớp với bản v10)
farkle-take-single-one = Lấy con 1 lẻ được { $points } điểm
farkle-take-single-five = Lấy con 5 lẻ được { $points } điểm
farkle-take-three-kind = Lấy bộ ba con { $number } được { $points } điểm
farkle-take-four-kind = Lấy tứ quý { $number } được { $points } điểm
farkle-take-five-kind = Lấy ngũ quý { $number } được { $points } điểm
farkle-take-six-kind = Lấy lục quý { $number } được { $points } điểm
farkle-take-small-straight = Lấy Sảnh nhỏ được { $points } điểm
farkle-take-large-straight = Lấy Sảnh lớn được { $points } điểm
farkle-take-three-pairs = Lấy 3 đôi được { $points } điểm
farkle-take-double-triplets = Lấy 2 bộ ba được { $points } điểm
farkle-take-full-house = Lấy Cù lũ được { $points } điểm

# Sự kiện trong game
farkle-rolls = { $player } gieo { $count } { $count ->
    [one] viên
   *[other] viên
}...
farkle-roll-result = { $dice }
farkle-farkle = CHÁY ĐIỂM! { $player } mất { $points } điểm
farkle-takes-combo = { $player } lấy { $combo } được { $points } điểm
farkle-you-take-combo = Bạn lấy { $combo } được { $points } điểm
farkle-hot-dice = Ăn trọn! (Hot dice)
farkle-banks = { $player } chốt { $points } điểm, tổng cộng có { $total }
farkle-winner = { $player } thắng với { $score } điểm!
farkle-winners-tie = Hòa nhau rồi! Những người thắng: { $players }

# Kiểm tra điểm lượt này
farkle-turn-score = Lượt này { $player } đang có { $points } điểm.
farkle-no-turn = Hiện không có ai đang chơi lượt của mình.

# Tùy chọn riêng cho Farkle
farkle-set-target-score = Điểm mục tiêu: { $score }
farkle-enter-target-score = Nhập điểm mục tiêu (500-5000):
farkle-option-changed-target = Điểm mục tiêu đã đặt là { $score }.

# Lý do hành động bị vô hiệu hóa
farkle-must-take-combo = Bạn phải chọn tổ hợp ăn điểm trước.
farkle-cannot-bank = Bạn không thể chốt điểm lúc này.
