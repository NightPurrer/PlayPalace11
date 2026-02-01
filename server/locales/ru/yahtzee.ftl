# Yahtzee game messages

# Game info
game-name-yahtzee = Ятзи

# Actions - Rolling
yahtzee-roll = Перебросить (осталось { $count })
yahtzee-roll-all = Бросить кубики

# Upper section scoring categories
yahtzee-score-ones = Единицы за { $points } { $points ->
    [one] очко
    [few] очка
   *[other] очков
}
yahtzee-score-twos = Двойки за { $points } { $points ->
    [one] очко
    [few] очка
   *[other] очков
}
yahtzee-score-threes = Тройки за { $points } { $points ->
    [one] очко
    [few] очка
   *[other] очков
}
yahtzee-score-fours = Четвёрки за { $points } { $points ->
    [one] очко
    [few] очка
   *[other] очков
}
yahtzee-score-fives = Пятёрки за { $points } { $points ->
    [one] очко
    [few] очка
   *[other] очков
}
yahtzee-score-sixes = Шестёрки за { $points } { $points ->
    [one] очко
    [few] очка
   *[other] очков
}

# Lower section scoring categories
yahtzee-score-three-kind = Триплет за { $points } { $points ->
    [one] очко
    [few] очка
   *[other] очков
}
yahtzee-score-four-kind = Каре за { $points } { $points ->
    [one] очко
    [few] очка
   *[other] очков
}
yahtzee-score-full-house = Фулл-хаус за { $points } { $points ->
    [one] очко
    [few] очка
   *[other] очков
}
yahtzee-score-small-straight = Малый стрит за { $points } { $points ->
    [one] очко
    [few] очка
   *[other] очков
}
yahtzee-score-large-straight = Большой стрит за { $points } { $points ->
    [one] очко
    [few] очка
   *[other] очков
}
yahtzee-score-yahtzee = Ятзи за { $points } { $points ->
    [one] очко
    [few] очка
   *[other] очков
}
yahtzee-score-chance = Шанс за { $points } { $points ->
    [one] очко
    [few] очка
   *[other] очков
}

# Game events
yahtzee-you-rolled = Вы выбросили: { $dice }. Осталось бросков: { $remaining }
yahtzee-player-rolled = { $player } выбрасывает: { $dice }. Осталось бросков: { $remaining }

# Scoring announcements
yahtzee-you-scored = Вы набрали { $points } { $points ->
    [one] очко
    [few] очка
   *[other] очков
} в категории «{ $category }».
yahtzee-player-scored = { $player } набирает { $points } в категории «{ $category }».

# Yahtzee bonus
yahtzee-you-bonus = Бонус Ятзи! +100 очков
yahtzee-player-bonus = { $player } получает бонус Ятзи! +100 очков

# Upper section bonus
yahtzee-you-upper-bonus = Бонус верхней секции! +35 очков ({ $total } в верхней секции)
yahtzee-player-upper-bonus = { $player } получает бонус верхней секции! +35 очков
yahtzee-you-upper-bonus-missed = Вы не получили бонус верхней секции (у вас { $total } очков, а нужно 63).
yahtzee-player-upper-bonus-missed = { $player } не получает бонус верхней секции.

# Scoring mode
yahtzee-choose-category = Выберите категорию для записи очков.
yahtzee-continuing = Продолжение хода.

# Status checks
yahtzee-check-scoresheet = Посмотреть таблицу очков
yahtzee-view-dice = Посмотреть кубики
yahtzee-your-dice = Ваши кубики: { $dice }.
yahtzee-your-dice-kept = Ваши кубики: { $dice }. Оставлено: { $kept }
yahtzee-not-rolled = Вы ещё не бросали кубики.

# Scoresheet display
yahtzee-scoresheet-header = Таблица очков: { $player }
yahtzee-scoresheet-upper = Верхняя секция:
yahtzee-scoresheet-lower = Нижняя секция:
yahtzee-scoresheet-category-filled = { $category }: { $points }
yahtzee-scoresheet-category-open = { $category }: -
yahtzee-scoresheet-upper-total-bonus = Итого в верхней: { $total } (БОНУС: +35)
yahtzee-scoresheet-upper-total-needed = Итого в верхней: { $total } (нужно ещё { $needed } для бонуса)
yahtzee-scoresheet-yahtzee-bonus = Бонусы Ятзи: { $count } x 100 = { $total }
yahtzee-scoresheet-grand-total = ОБЩИЙ СЧЁТ: { $total }

# Category names (for announcements)
yahtzee-category-ones = Единицы
yahtzee-category-twos = Двойки
yahtzee-category-threes = Тройки
yahtzee-category-fours = Четвёрки
yahtzee-category-fives = Пятёрки
yahtzee-category-sixes = Шестёрки
yahtzee-category-three-kind = Триплет
yahtzee-category-four-kind = Каре
yahtzee-category-full-house = Фулл-хаус
yahtzee-category-small-straight = Малый стрит
yahtzee-category-large-straight = Большой стрит
yahtzee-category-yahtzee = Ятзи
yahtzee-category-chance = Шанс

# Game end
yahtzee-winner = { $player } побеждает с результатом { $score } { $score ->
    [one] очко
    [few] очка
   *[other] очков
}!
yahtzee-winners-tie = Ничья! { $players } набрали по { $score } { $score ->
    [one] очку
    [few] очка
   *[other] очков
}!

# Options
yahtzee-set-rounds = Количество партий: { $rounds }
yahtzee-enter-rounds = Введите количество партий (1–10):
yahtzee-option-changed-rounds = Количество партий установлено на { $rounds }.

# Disabled action reasons
yahtzee-no-rolls-left = У вас не осталось бросков.
yahtzee-roll-first = Сначала нужно бросить кубики.
yahtzee-category-filled = Эта категория уже заполнена.
