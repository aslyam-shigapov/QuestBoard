from django.shortcuts import render


# Пока нет БД — тестовые доски
MOCK_BOARDS = [
    {
        'title': 'Спортивный челлендж 30 дней',
        'description': 'Каждый день — 30 минут спорта. Пробежки, отжимания, йога.',
        'author': 'Aslyam',
        'quests_count': 30,
        'difficulty': 'hard',
    },
    {
        'title': 'Путь программиста',
        'description': 'Ежедневно изучаю Django, решаю задачи, пишу код.',
        'author': 'Aslyam',
        'quests_count': 21,
        'difficulty': 'medium',
    },
    {
        'title': 'Книжный марафон',
        'description': 'Читаю минимум 20 страниц в день. Художка и нон-фикшн.',
        'author': 'Aslyam',
        'quests_count': 15,
        'difficulty': 'easy',
    },
    {
        'title': 'Ранний подъём',
        'description': 'Встаю в 6 утра каждый день. Без кнопки «ещё 5 минут».',
        'author': 'Aslyam',
        'quests_count': 14,
        'difficulty': 'hard',
    },
]


def home_page(request):
    """
    Главная страница QuestBoard — приветствие и краткое описание.
    """
    return render(request, 'boards/home.html')


def board_list(request):
    """
    Список публичных досок. Пока с фейковыми данными (без БД).
    """
    context = {'boards': MOCK_BOARDS}
    return render(request, 'boards/board_list.html', context)