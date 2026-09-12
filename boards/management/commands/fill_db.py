"""
Management-команда для автозаполнения БД тестовыми данными.

Запуск:
    python manage.py fill_db

Что создаёт:
    - 5 пользователей (с профилями)
    - 10 досок (по 2 доски на каждого юзера)
    - 50 квестов (по 5 квестов на доску)
    - 10 ачивок

Идемпотентна: использует get_or_create, можно запускать много раз.
"""

import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from users.models import Profile
from boards.models import Board
from quests.models import Quest
from achievements.models import Achievement


# ============================================
# Справочные данные
# ============================================

USERS_DATA = [
    ('quest_master', 'quest_master@questboard.local'),
    ('dragon_slayer', 'dragon@questboard.local'),
    ('pixel_wizard', 'pixel@questboard.local'),
    ('night_runner', 'night@questboard.local'),
    ('code_ninja', 'ninja@questboard.local'),
]

BOARDS_DATA = [
    ('Спортивный челлендж 30 дней', 'Каждый день — 30 минут спорта. Пробежки, отжимания, йога.', True),
    ('Путь программиста', 'Ежедневно изучаю Django, решаю задачи, пишу код.', True),
    ('Книжный марафон', 'Читаю минимум 20 страниц в день. Художка и нон-фикшн.', True),
    ('Ранний подъём', 'Встаю в 6 утра каждый день. Без кнопки «ещё 5 минут».', True),
    ('Медитация и осознанность', '10 минут медитации каждое утро.', True),
    ('Английский каждый день', '15 минут практики английского. Duolingo, сериалы, чтение.', True),
    ('Вода — наше всё', 'Пью 2 литра воды каждый день.', True),
    ('Шаги в день', 'Прохожу минимум 10 000 шагов.', True),
    ('Изучаю новое', '30 минут на новую тему каждый день.', True),
    ('Цифровой детокс', 'Никаких соцсетей после 21:00.', True),
]

QUEST_TEMPLATES = [
    ('Основной квест', 'Выполнить основное задание дня', 'easy', 10),
    ('Продвинутый квест', 'Сделать больше обычного', 'medium', 20),
    ('Бонусный квест', 'Дополнительное задание для упорных', 'easy', 5),
    ('Хардкорный квест', 'Испытание для настоящих героев', 'hard', 50),
    ('Ежедневный челлендж', 'Каждый день — новый вызов', 'medium', 15),
]

ACHIEVEMENTS_DATA = [
    ('first_steps', 'Первые шаги', 'Выполнил первый квест', 5),
    ('marathoner', 'Марафонец', 'Выполнил 30 квестов подряд', 50),
    ('legend', 'Легенда', 'Достиг 10 уровня', 100),
    ('night_hunter', 'Ночной охотник', 'Выполнил квест после 22:00', 15),
    ('early_bird', 'Ранняя пташка', 'Выполнил квест до 7 утра', 15),
    ('perfectionist', 'Перфекционист', 'Выполнил все квесты на доске', 30),
    ('collector', 'Коллекционер', 'Создал 10 досок', 25),
    ('social_butterfly', 'Душа компании', 'Поделился доской с друзьями', 10),
    ('hardcore', 'Хардкорщик', 'Выполнил 10 хардкорных квестов', 40),
    ('unstoppable', 'Неудержимый', '30 дней подряд заходил на сайт', 60),
]


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными (юзеры, доски, квесты, ачивки)'

    def handle(self, *args, **options):
        """Главный метод команды."""
        self.stdout.write(self.style.WARNING('🚀 Начинаю заполнение БД...'))

        with transaction.atomic():
            users = self._create_users()
            self._create_boards_and_quests(users)
            self._create_achievements()

        self.stdout.write(self.style.SUCCESS('✅ Готово! База заполнена.'))
        self._print_stats()

    # ============================================
    # Создание пользователей
    # ============================================

    def _create_users(self):
        """Создаёт 5 тестовых юзеров с профилями. Возвращает список User."""
        self.stdout.write('\n👤 Создаю пользователей...')
        users = []
        for username, email in USERS_DATA:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email},
            )
            if created:
                user.set_password('Quest2026!')
                user.save()
                self.stdout.write(f'   ✅ {username} (пароль: Quest2026!)')
            else:
                self.stdout.write(f'   ⏭️  {username} уже существует')

            # Профиль создаётся автоматически через сигнал, но на всякий случай
            profile, _ = Profile.objects.get_or_create(user=user)
            # Задаём случайный XP
            profile.xp = random.randint(0, 500)
            profile.level = 1 + profile.xp // 100
            profile.save()

            users.append(user)

        return users

    # ============================================
    # Создание досок и квестов
    # ============================================

    def _create_boards_and_quests(self, users):
        """Создаёт 10 досок (по 2 на юзера) и 50 квестов (по 5 на доску)."""
        self.stdout.write('\n🗂️  Создаю доски и квесты...')
        boards_created = 0
        quests_created = 0

        for i, (title, description, is_public) in enumerate(BOARDS_DATA):
            owner = users[i % len(users)]

            board, created = Board.objects.get_or_create(
                title=title,
                owner=owner,
                defaults={
                    'description': description,
                    'is_public': is_public,
                },
            )
            if created:
                boards_created += 1

            # Создаём 5 квестов на доску
            for quest_title, quest_desc, difficulty, xp in QUEST_TEMPLATES:
                unique_title = f'{quest_title} — {board.title[:20]}'
                _, quest_created = Quest.objects.get_or_create(
                    board=board,
                    title=unique_title,
                    defaults={
                        'description': quest_desc,
                        'difficulty': difficulty,
                        'xp_reward': xp,
                        'is_active': True,
                    },
                )
                if quest_created:
                    quests_created += 1

        self.stdout.write(f'   ✅ Досок создано: {boards_created}')
        self.stdout.write(f'   ✅ Квестов создано: {quests_created}')

    # ============================================
    # Создание ачивок
    # ============================================

    def _create_achievements(self):
        """Создаёт 10 ачивок."""
        self.stdout.write('\n🏆 Создаю ачивки...')
        created_count = 0

        for code, title, description, xp_bonus in ACHIEVEMENTS_DATA:
            _, created = Achievement.objects.get_or_create(
                code=code,
                defaults={
                    'title': title,
                    'description': description,
                    'xp_bonus': xp_bonus,
                },
            )
            if created:
                created_count += 1

        self.stdout.write(f'   ✅ Ачивок создано: {created_count}')

    # ============================================
    # Статистика
    # ============================================

    def _print_stats(self):
        """Печатает итоговую статистику БД."""
        self.stdout.write('\n📊 Итоговая статистика:')
        self.stdout.write(f'   👤 Пользователей: {User.objects.count()}')
        self.stdout.write(f'   🗂️  Досок: {Board.objects.count()}')
        self.stdout.write(f'   ⚔️  Квестов: {Quest.objects.count()}')
        self.stdout.write(f'   🏆 Ачивок: {Achievement.objects.count()}')
        self.stdout.write('\n🎉 Все тестовые юзеры имеют пароль: Quest2026!')