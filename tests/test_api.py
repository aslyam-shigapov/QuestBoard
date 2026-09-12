"""
Тесты API QuestBoard (DRF).
"""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from boards.models import Board
from quests.models import Quest


# ============================================
# ФИКСТУРЫ
# ============================================

@pytest.fixture
def api_client():
    """DRF-клиент для тестов."""
    return APIClient()


@pytest.fixture
def user(db):
    """Тестовый пользователь."""
    return User.objects.create_user(username='apitester', password='TestPass2026!')


@pytest.fixture
def board(db, user):
    """Публичная тестовая доска."""
    return Board.objects.create(
        owner=user,
        title='API-доска',
        description='Для тестов',
        is_public=True,
    )


@pytest.fixture
def quest(db, board):
    """Квест в тестовой доске."""
    return Quest.objects.create(
        board=board,
        title='API-квест',
        difficulty='easy',
        xp_reward=10,
    )


# ============================================
# ТЕСТЫ API
# ============================================

@pytest.mark.django_db
class TestBoardsAPI:
    """Тесты /api/boards/."""

    def test_list_returns_200(self, api_client):
        """GET /api/boards/ должен вернуть 200."""
        response = api_client.get('/api/boards/')
        assert response.status_code == 200

    def test_list_contains_board(self, api_client, board):
        """В списке должна быть созданная доска."""
        response = api_client.get('/api/boards/')
        data = response.json()
        assert data['count'] == 1
        assert data['results'][0]['title'] == 'API-доска'

    def test_detail_returns_200(self, api_client, board):
        """GET /api/boards/<id>/ возвращает 200."""
        response = api_client.get(f'/api/boards/{board.id}/')
        assert response.status_code == 200

    def test_detail_has_correct_structure(self, api_client, board):
        """В JSON должны быть нужные поля."""
        response = api_client.get(f'/api/boards/{board.id}/')
        data = response.json()
        assert 'id' in data
        assert 'title' in data
        assert 'owner_username' in data
        assert data['title'] == 'API-доска'


@pytest.mark.django_db
class TestQuestsAPI:
    """Тесты /api/quests/."""

    def test_list_returns_200(self, api_client):
        """GET /api/quests/ должен вернуть 200."""
        response = api_client.get('/api/quests/')
        assert response.status_code == 200

    def test_list_contains_quest(self, api_client, quest):
        """В списке должен быть созданный квест."""
        response = api_client.get('/api/quests/')
        data = response.json()
        assert data['count'] == 1
        assert data['results'][0]['title'] == 'API-квест'

    def test_filter_by_board(self, api_client, board, quest):
        """Фильтр ?board=<id> работает."""
        response = api_client.get(f'/api/quests/?board={board.id}')
        data = response.json()
        assert data['count'] == 1


@pytest.mark.django_db
class TestProfileAPI:
    """Тесты /api/profile/me/."""

    def test_unauthorized_returns_403(self, api_client):
        """Аноним не должен получать профиль."""
        response = api_client.get('/api/profile/me/')
        assert response.status_code in [401, 403]

    def test_authorized_returns_profile(self, api_client, user):
        """Авторизованный получает свой профиль."""
        api_client.force_authenticate(user=user)
        response = api_client.get('/api/profile/me/')
        assert response.status_code == 200
        data = response.json()
        assert data['username'] == 'apitester'
        assert 'xp' in data
        assert 'level' in data