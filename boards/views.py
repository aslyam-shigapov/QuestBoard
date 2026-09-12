from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Board
from .forms import BoardForm


def home_page(request):
    """Главная страница QuestBoard."""
    return render(request, 'boards/home.html')


def board_list(request):
    """Список публичных досок (уже из БД)."""
    boards = Board.objects.filter(is_public=True)
    context = {'boards': boards}
    return render(request, 'boards/board_list.html', context)


def board_detail(request, board_id):
    """
    Детальная страница доски с квестами.
    Доступна всем, если доска публичная, или только владельцу.
    """
    board = get_object_or_404(Board, id=board_id)
    if not board.is_public and request.user != board.owner:
        return HttpResponseForbidden('Эта доска приватная')
    quests = board.quests.all()
    context = {'board': board, 'quests': quests}
    return render(request, 'boards/board_detail.html', context)


@login_required
def board_create(request):
    """Создание новой доски. Владелец подставляется автоматически."""
    if request.method == 'POST':
        form = BoardForm(request.POST, request.FILES)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            return redirect('boards:board_detail', board_id=board.id)
    else:
        form = BoardForm()
    return render(request, 'boards/board_form.html', {'form': form, 'action': 'Создать'})


@login_required
def board_edit(request, board_id):
    """Редактирование доски. Только владелец."""
    board = get_object_or_404(Board, id=board_id)
    if board.owner != request.user:
        return HttpResponseForbidden('Это не ваша доска')
    if request.method == 'POST':
        form = BoardForm(request.POST, request.FILES, instance=board)
        if form.is_valid():
            form.save()
            return redirect('boards:board_detail', board_id=board.id)
    else:
        form = BoardForm(instance=board)
    return render(request, 'boards/board_form.html', {'form': form, 'action': 'Редактировать'})


@login_required
def board_delete(request, board_id):
    """Удаление доски. Только владелец."""
    board = get_object_or_404(Board, id=board_id)
    if board.owner != request.user:
        return HttpResponseForbidden('Это не ваша доска')
    if request.method == 'POST':
        board.delete()
        return redirect('boards:board_list')
    return render(request, 'boards/board_confirm_delete.html', {'board': board})


def add_to_favorites(request, board_id):
    """
    Добавляет/убирает доску из избранного в сессии.
    Работает для анонимных и авторизованных пользователей.
    """
    board = get_object_or_404(Board, id=board_id)
    favorites = request.session.get('favorites', [])

    if board.id in favorites:
        favorites.remove(board.id)  # убираем
    else:
        favorites.append(board.id)  # добавляем

    request.session['favorites'] = favorites
    request.session.modified = True
    return redirect('boards:board_detail', board_id=board.id)


def favorites_list(request):
    """
    Показывает список избранных досок из сессии.
    """
    favorites_ids = request.session.get('favorites', [])
    boards = Board.objects.filter(id__in=favorites_ids)
    context = {'boards': boards}
    return render(request, 'boards/favorites.html', context)


def toggle_theme(request):
    """
    Переключает тему (light/dark) в куке. Живёт 30 дней.
    """
    current = request.COOKIES.get('theme', 'dark')
    new_theme = 'light' if current == 'dark' else 'dark'

    # Возвращаемся на ту же страницу
    referer = request.META.get('HTTP_REFERER', '/')
    response = redirect(referer)
    response.set_cookie('theme', new_theme, max_age=60 * 60 * 24 * 30)  # 30 дней
    return response


def board_chat(request, board_id):
    """
    Страница чата конкретной доски.
    """
    board = get_object_or_404(Board, id=board_id)
    context = {'board': board}
    return render(request, 'boards/chat.html', context)