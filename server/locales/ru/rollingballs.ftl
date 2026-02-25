# Rolling Balls game messages
# Note: Common messages like round-start, turn-start are in games.ftl

# Game info
game-name-rollingballs = Катящиеся шары

# Turn actions
rb-take = Взять { $count } { $count ->
    [one] шар
    [few] шара
   *[other] шаров
}
rb-reshuffle-action = Перемешать шары в трубе (осталось: { $remaining })
rb-view-pipe-action = Заглянуть в трубу (осталось: { $remaining })

# Take ball events
rb-you-take = Вы берёте { $count } { $count ->
    [one] шар
    [few] шара
   *[other] шаров
}!
rb-player-takes = { $player } берёт { $count } { $count ->
    [one] шар
    [few] шара
   *[other] шаров
}!
rb-ball-plus = Шар №{ $num }: { $description }! Плюс { $value } { $value ->
    [one] очко
    [few] очка
   *[other] очков
}!
rb-ball-minus = Шар №{ $num }: { $description }! Минус { $value } { $value ->
    [one] очко
    [few] очка
   *[other] очков
}!
rb-ball-zero = Шар №{ $num }: { $description }! Без изменений!
rb-new-score = Счёт игрока { $player }: { $score } { $score ->
    [one] очко
    [few] очка
   *[other] очков
}.

# Reshuffle events
rb-you-reshuffle = Вы встряхиваете трубу!
rb-player-reshuffles = { $player } встряхивает трубу!
rb-reshuffled = Шары в трубе перемешаны!
rb-reshuffle-penalty = { $player } теряет { $points } { $points ->
    [one] очко
    [few] очка
   *[other] очков
} за перемешивание.

# View pipe
rb-view-pipe-header = В трубе { $count } { $count ->
    [one] шар
    [few] шара
   *[other] шаров
}:
rb-view-pipe-ball = { $num }: { $description }. Ценность: { $value } { $value ->
    [one] очко
    [few] очка
   *[other] очков
}.

# Game start
rb-pipe-filled = В трубу засыпали { $count } { $count ->
    [one] шар
    [few] шара
   *[other] шаров
}!
rb-balls-remaining = В трубе осталось { $count } { $count ->
    [one] шар
    [few] шара
   *[other] шаров
}.

# Game end
rb-pipe-empty = Труба пуста!
rb-score-line = { $player }: { $score } { $score ->
    [one] очко
    [few] очка
   *[other] очков
}.
rb-winner = Победитель — { $player } с результатом { $score }!
rb-you-win = Вы победили, набрав { $score }!
rb-tie = Ничья между игроками { $players }! У обоих по { $score }!

# Options
rb-set-min-take = Минимум шаров за ход: { $count }
rb-enter-min-take = Введите минимальное количество шаров (1–5):
rb-option-changed-min-take = Минимальное количество шаров за ход установлено на { $count }.

rb-set-max-take = Максимум шаров за ход: { $count }
rb-enter-max-take = Введите максимальное количество шаров (1–5):
rb-option-changed-max-take = Максимальное количество шаров за ход установлено на { $count }.

rb-set-view-pipe-limit = Лимит просмотров трубы: { $count }
rb-enter-view-pipe-limit = Введите лимит просмотров (0 — отключить, макс. 100):
rb-option-changed-view-pipe-limit = Лимит просмотров трубы установлен на { $count }.

rb-set-reshuffle-limit = Лимит перемешиваний: { $count }
rb-enter-reshuffle-limit = Введите лимит перемешиваний (0 — отключить, макс. 100):
rb-option-changed-reshuffle-limit = Лимит перемешиваний установлен на { $count }.

rb-set-reshuffle-penalty = Штраф за перемешивание: { $points }
rb-enter-reshuffle-penalty = Введите штраф за перемешивание (0–5):
rb-option-changed-reshuffle-penalty = Штраф за перемешивание установлен на { $points }.

rb-set-ball-packs = Наборы шаров (выбрано { $count } из { $total })
rb-option-changed-ball-packs = Наборы шаров обновлены (выбрано { $count } из { $total }).

# Disabled reasons
rb-not-enough-balls = В трубе недостаточно шаров.
rb-no-reshuffles-left = Попытки перемешивания закончились.
rb-already-reshuffled = Вы уже перемешивали шары в этом ходу.
rb-no-views-left = Попытки просмотра закончились.