from django.db import models
from django.contrib.auth.models import User


class Achievement(models.Model):
    """
    Справочник ачивок — «Первые шаги», «Марафонец», «Легенда» и т.д.
    """
    code = models.SlugField('Код', max_length=50, unique=True)
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True)
    icon = models.ImageField('Иконка', upload_to='achievements/', blank=True, null=True)
    xp_bonus = models.PositiveIntegerField('Бонус XP', default=0)

    class Meta:
        verbose_name = 'Ачивка'
        verbose_name_plural = 'Ачивки'

    def __str__(self):
        return self.title


class UserAchievement(models.Model):
    """
    Связь пользователя и полученной ачивки.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='achievements',
        verbose_name='Пользователь',
    )
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.PROTECT,  # было CASCADE — теперь PROTECT
        related_name='owners',
        verbose_name='Ачивка',
    )
    unlocked_at = models.DateTimeField('Получена', auto_now_add=True)

    class Meta:
        verbose_name = 'Ачивка пользователя'
        verbose_name_plural = 'Ачивки пользователей'
        unique_together = ('user', 'achievement')
        ordering = ['-unlocked_at']

    def __str__(self):
        return f'{self.user.username} → {self.achievement.title}'