from django.contrib import admin
from .models import Achievement, UserAchievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """
    Настройка ачивок в админке.
    """
    list_display = ('title', 'code', 'xp_bonus')
    search_fields = ('title', 'code', 'description')
    prepopulated_fields = {'code': ('title',)}  # код автоматически из названия


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    """
    Настройка полученных ачивок.
    """
    list_display = ('user', 'achievement', 'unlocked_at')
    list_filter = ('achievement', 'unlocked_at')
    search_fields = ('user__username', 'achievement__title')
    readonly_fields = ('unlocked_at',)