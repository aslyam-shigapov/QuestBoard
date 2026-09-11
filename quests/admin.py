from django.contrib import admin
from .models import Quest, QuestCompletion


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    """
    Настройка отображения квестов в админке.
    """
    list_display = ('title', 'board', 'difficulty', 'xp_reward', 'is_active')
    list_filter = ('difficulty', 'is_active', 'board')
    search_fields = ('title', 'description')
    list_editable = ('xp_reward', 'is_active')


@admin.register(QuestCompletion)
class QuestCompletionAdmin(admin.ModelAdmin):
    """
    Настройка отображения выполнений квестов.
    """
    list_display = ('user', 'quest', 'completed_at')
    list_filter = ('completed_at', 'quest')
    search_fields = ('user__username', 'quest__title')
    readonly_fields = ('completed_at',)