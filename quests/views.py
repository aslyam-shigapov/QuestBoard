from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Quest, QuestCompletion
from .forms import QuestForm
from boards.models import Board


@login_required
def quest_create(request, board_id):
    """Создание квеста внутри доски. Только владелец доски."""
    board = get_object_or_404(Board, id=board_id)
    if board.owner != request.user:
        return HttpResponseForbidden('Это не ваша доска')
    if request.method == 'POST':
        form = QuestForm(request.POST)
        if form.is_valid():
            quest = form.save(commit=False)
            quest.board = board
            quest.save()
            return redirect('boards:board_detail', board_id=board.id)
    else:
        form = QuestForm()
    return render(request, 'quests/quest_form.html', {'form': form, 'board': board})


@login_required
def quest_delete(request, quest_id):
    """Удаление квеста. Только владелец доски."""
    quest = get_object_or_404(Quest, id=quest_id)
    if quest.board.owner != request.user:
        return HttpResponseForbidden('Это не ваш квест')
    board_id = quest.board.id
    quest.delete()
    return redirect('boards:board_detail', board_id=board_id)


@login_required
def quest_complete(request, quest_id):
    """Отметка квеста как выполненного. Только авторизованные."""
    quest = get_object_or_404(Quest, id=quest_id)
    QuestCompletion.objects.create(quest=quest, user=request.user)
    # Начисляем XP
    profile = request.user.profile
    profile.xp += quest.xp_reward
    profile.level = 1 + profile.xp // 100
    profile.save()
    return redirect('boards:board_detail', board_id=quest.board.id)