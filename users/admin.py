from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Настройка отображения профилей в админке.
    """
    list_display = ('user', 'level', 'xp')
    list_filter = ('level',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('xp', 'level')