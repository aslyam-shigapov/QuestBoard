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