"""
Тесты моделей QuestBoard.
"""

import pytest
from decimal import Decimal
from django.contrib.auth.models import User

from boards.models import Board
from quests.models import Quest, QuestCompletion
from achievements.models import Achievement, UserAchievement
from users.models import Profile


# ============================================
# ФИКСТУРЫ (создают объекты для тестов)
# ============================================

@pytest.fixture
def user(db):
    """Тестовый пользователь."""
    return User.objects.create_user(username='tester', password='TestPass2026!')


@pytest.fixture
def board(db, user):
    """Тестовая доска."""
    return Board.objects.create(
        owner=user,
        title='Спортивный челлендж',
        description='Каждый день — 30 минут спорта',
        is_public=True,
    )


@pytest.fixture
def quest(db, board):
    """Тестовый квест."""
    return Quest.objects.create(
        board=board,
        title='Пробежка 3 км',
        description='Бегать 3 км каждый день',
        difficulty='medium',
        xp_reward=20,
    )


@pytest.fixture
def achievement(db):
    """Тестовая ачивка."""
    return Achievement.objects.create(
        code='first-steps',
        title='Первые шаги',
        description='Выполнил первый квест',
        xp_bonus=5,
    )


# ============================================
# ТЕСТЫ МОДЕЛЕЙ
# ============================================

@pytest.mark.django_db
class TestBoardModel:
    """Тесты модели Board."""

    def test_str(self, board):
        """__str__ должен возвращать название доски."""
        assert str(board) == 'Спортивный челлендж'

    def test_default_is_public(self, user):
        """По умолчанию доска публичная."""
        new_board = Board.objects.create(owner=user, title='Test')
        assert new_board.is_public is True

    def test_quests_relation(self, board, quest):
        """Обратная связь от доски к квестам работает."""
        assert board.quests.count() == 1
        assert board.quests.first() == quest


@pytest.mark.django_db
class TestQuestModel:
    """Тесты модели Quest."""

    def test_str(self, quest):
        """__str__ должен возвращать название + сложность."""
        assert 'Пробежка 3 км' in str(quest)
        assert 'Средний' in str(quest)

    def test_default_xp_reward(self, board):
        """По умолчанию XP = 10."""
        new_quest = Quest.objects.create(board=board, title='Test')
        assert new_quest.xp_reward == 10

    def test_default_difficulty(self, board):
        """По умолчанию сложность — easy."""
        new_quest = Quest.objects.create(board=board, title='Test')
        assert new_quest.difficulty == 'easy'

    def test_is_active_default(self, board):
        """По умолчанию квест активен."""
        new_quest = Quest.objects.create(board=board, title='Test')
        assert new_quest.is_active is True


@pytest.mark.django_db
class TestProfileSignals:
    """Тесты сигнала post_save для Profile."""

    def test_auto_created_on_user_create(self):
        """При создании User автоматически создаётся Profile."""
        new_user = User.objects.create_user(username='bob', password='Pass2026!')
        assert Profile.objects.filter(user=new_user).exists()

    def test_profile_defaults(self):
        """У нового профиля XP = 0 и level = 1."""
        new_user = User.objects.create_user(username='alice', password='Pass2026!')
        profile = new_user.profile
        assert profile.xp == 0
        assert profile.level == 1


@pytest.mark.django_db
class TestAchievementModel:
    """Тесты модели Achievement."""

    def test_str(self, achievement):
        """__str__ должен возвращать название."""
        assert str(achievement) == 'Первые шаги'

    def test_unique_code(self, db, achievement):
        """Код ачивки должен быть уникальным."""
        import django.db
        with pytest.raises(Exception):
            Achievement.objects.create(code='first-steps', title='Дубликат')


@pytest.mark.django_db
class TestUserAchievement:
    """Тесты связи User-Achievement."""

    def test_user_earns_achievement(self, user, achievement):
        """Пользователь может получить ачивку."""
        ua = UserAchievement.objects.create(user=user, achievement=achievement)
        assert ua.user == user
        assert ua.achievement == achievement

    def test_unique_together(self, user, achievement):
        """Один и тот же пользователь не может получить одну ачивку дважды."""
        UserAchievement.objects.create(user=user, achievement=achievement)
        with pytest.raises(Exception):
            UserAchievement.objects.create(user=user, achievement=achievement)