# Thông báo trò chơi Scopa
# Lưu ý: Các thông báo chung như bắt đầu vòng, bắt đầu lượt, điểm mục tiêu, chế độ đội nằm trong games.ftl

# Tên trò chơi
game-name-scopa = Scopa

# Sự kiện trong game
scopa-initial-table = Bài trên bàn: { $cards }
scopa-no-initial-table = Không có bài trên bàn khi bắt đầu.
scopa-you-collect = Bạn ăn { $cards } bằng lá { $card }
scopa-player-collects = { $player } ăn { $cards } bằng lá { $card }
scopa-you-put-down = Bạn hạ xuống lá { $card }.
scopa-player-puts-down = { $player } hạ xuống lá { $card }.
scopa-scopa-suffix =  - SCOPA!
scopa-clear-table-suffix = , quét sạch bàn.
scopa-remaining-cards = { $player } nhận số bài còn lại trên bàn.
scopa-scoring-round = Vòng tính điểm...
scopa-most-cards = { $player } được 1 điểm vì nhiều bài nhất ({ $count } lá).
scopa-most-cards-tie = Số lượng bài bằng nhau - không ai có điểm.
scopa-most-diamonds = { $player } được 1 điểm vì nhiều Rô nhất ({ $count } lá).
scopa-most-diamonds-tie = Số lượng Rô bằng nhau - không ai có điểm.
scopa-seven-diamonds = { $player } được 1 điểm vì có lá 7 Rô.
scopa-seven-diamonds-multi = { $player } được 1 điểm vì có nhiều 7 Rô nhất ({ $count } × 7 Rô).
scopa-seven-diamonds-tie = Số lượng 7 Rô bằng nhau - không ai có điểm.
scopa-most-sevens = { $player } được 1 điểm vì nhiều quân 7 nhất ({ $count } quân).
scopa-most-sevens-tie = Số lượng quân 7 bằng nhau - không ai có điểm.
scopa-round-scores = Điểm vòng này:
scopa-round-score-line = { $player }: +{ $round_score } (tổng: { $total_score })
scopa-table-empty = Không có lá bài nào trên bàn.
scopa-no-such-card = Không có lá bài nào ở vị trí đó.
scopa-captured-count = Bạn đã ăn được { $count } lá

# Hành động xem
scopa-view-table = Xem bàn
scopa-view-captured = Xem bài đã ăn

# Tùy chọn riêng cho Scopa
scopa-enter-target-score = Nhập điểm mục tiêu (1-121)
scopa-set-cards-per-deal = Số lá mỗi lần chia: { $cards }
scopa-enter-cards-per-deal = Nhập số lá mỗi lần chia (1-10)
scopa-set-decks = Số lượng bộ bài: { $decks }
scopa-enter-decks = Nhập số lượng bộ bài (1-6)
scopa-toggle-escoba = Chế độ Escoba (tổng bằng 15): { $enabled }
scopa-toggle-hints = Gợi ý nước ăn bài: { $enabled }
scopa-set-mechanic = Cơ chế Scopa: { $mechanic }
scopa-select-mechanic = Chọn cơ chế Scopa
scopa-toggle-instant-win = Thắng ngay khi được Scopa: { $enabled }
scopa-toggle-team-scoring = Gộp bài cả đội để tính điểm: { $enabled }
scopa-toggle-inverse = Chế độ Đảo ngược (đạt điểm mục tiêu = bị loại): { $enabled }

# Thông báo thay đổi tùy chọn
scopa-option-changed-cards = Số lá mỗi lần chia đã đặt là { $cards }.
scopa-option-changed-decks = Số lượng bộ bài đã đặt là { $decks }.
scopa-option-changed-escoba = Chế độ Escoba { $enabled }.
scopa-option-changed-hints = Gợi ý nước ăn bài { $enabled }.
scopa-option-changed-mechanic = Cơ chế Scopa đã đặt là { $mechanic }.
scopa-option-changed-instant = Thắng ngay khi được Scopa { $enabled }.
scopa-option-changed-team-scoring = Gộp bài cả đội để tính điểm { $enabled }.
scopa-option-changed-inverse = Chế độ Đảo ngược { $enabled }.

# Các lựa chọn cơ chế Scopa
scopa-mechanic-normal = Bình thường
scopa-mechanic-no_scopas = Không tính điểm Scopa
scopa-mechanic-only_scopas = Chỉ tính điểm Scopa

# Lý do hành động bị vô hiệu hóa
scopa-timer-not-active = Đồng hồ vòng chơi không hoạt động.

# Lỗi xác thực
scopa-error-not-enough-cards = Không đủ bài trong { $decks } { $decks ->
    [one] bộ bài
   *[other] bộ bài
} cho { $players } { $players ->
    [one] người chơi
   *[other] người chơi
} với { $cards_per_deal } lá mỗi người. (Cần { $cards_per_deal } × { $players } = { $cards_needed } lá, nhưng chỉ có { $total_cards }.)
