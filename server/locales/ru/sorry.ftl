# Sorry localization

game-name-sorry = Sorry!
category-board-games = Настольные игры

# Turn actions
sorry-draw-card = Взять карту
sorry-move-slot = Вариант хода { $slot }
sorry-move-slot-fallback = Выберите ход

# Move labels (for dynamic move menu entries)
sorry-move-start = Вывести фишку { $pawn } со старта
sorry-move-forward = Продвинуть фишку { $pawn } вперёд на { $steps } { $steps ->
    [one] клетку
    [few] клетки
   *[other] клеток
}
sorry-move-backward = Подвинуть фишку { $pawn } назад на { $steps } { $steps ->
    [one] клетку
    [few] клетки
   *[other] клеток
}
sorry-move-swap = Поменять фишку { $pawn } местами с фишкой { $target_pawn } игрока { $target_player }
sorry-move-sorry = Заменить фишку { $target_pawn } игрока { $target_player } своей фишкой { $pawn }
sorry-move-split7 = Разделить 7: фишка { $pawn_a } на { $steps_a }, фишка { $pawn_b } на { $steps_b }

# Gameplay announcements
sorry-card-sorry = Sorry!
sorry-draw-announcement = { $player } берёт карту: { $card }.
sorry-no-legal-moves = У игрока { $player } нет доступных ходов для карты { $card }.
sorry-play-start = { $player } выводит фишку { $pawn } со старта.
sorry-play-forward = { $player } передвигает фишку { $pawn } вперёд на { $steps } { $steps ->
    [one] клетку
    [few] клетки
   *[other] клеток
}.
sorry-play-backward = { $player } передвигает фишку { $pawn } назад на { $steps } { $steps ->
    [one] клетку
    [few] клетки
   *[other] клеток
}.
sorry-play-swap = { $player } меняет свою фишку { $pawn } местами с фишкой { $target_pawn } игрока { $target_player }.
sorry-play-sorry = Sorry! { $player } заменяет фишку { $target_pawn } игрока { $target_player } своей фишкой { $pawn }.
sorry-play-split7 = { $player } разделяет 7: фишка { $pawn_a } на { $steps_a }, фишка { $pawn_b } на { $steps_b }.

# Options
sorry-option-rules-profile = Профиль правил: { $rules_profile }
sorry-option-select-rules-profile = Выберите профиль правил
sorry-option-changed-rules-profile = Профиль правил изменён на { $rules_profile }.
sorry-rules-profile-classic-00390 = Классика 00390
sorry-rules-profile-a5065-core = A5065 (базовый)
sorry-option-auto-apply-single-move = Автоход при единственном варианте: { $auto_apply_single_move }
sorry-option-faster-setup-one-pawn-out = Быстрый старт (одна фишка сразу на поле): { $faster_setup_one_pawn_out }
sorry-option-changed-auto-apply-single-move = Автоход при единственном варианте: { $auto_apply_single_move }.
sorry-option-changed-faster-setup-one-pawn-out = Быстрый старт: { $faster_setup_one_pawn_out }.