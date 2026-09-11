from django.contrib import admin
from .models import Board
from quests.models import Quest


class QuestInline(admin.TabularInline):
    """
    Квесты показываются прямо внутри доски (компактная таблица).
    """
    model = Quest
    extra = 1  # одна пустая строка для нового квеста


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """
    Настройка отображения досок в админке.
    """
    list_display = ('title', 'owner', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('title', 'description', 'owner__username')
    list_editable = ('is_public',)
    inlines = [QuestInline]