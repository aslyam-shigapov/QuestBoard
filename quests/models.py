from django.db import models
from django.contrib.auth.models import User
from boards.models import Board


class Quest(models.Model):
    """
    Квест — конкретное задание внутри доски.
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Лёгкий'),
        ('medium', 'Средний'),
        ('hard', 'Хардкор'),
    ]

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='quests',
        verbose_name='Доска',
    )
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    xp_reward = models.PositiveIntegerField('Награда (XP)', default=10)
    difficulty = models.CharField(
        'Сложность',
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy',
    )
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Квест'
        verbose_name_plural = 'Квесты'
        ordering = ['id']

    def __str__(self):
        return f'{self.title} ({self.get_difficulty_display()})'


class QuestCompletion(models.Model):
    """
    Факт выполнения квеста пользователем.
    """
    quest = models.ForeignKey(
        Quest,
        on_delete=models.CASCADE,
        related_name='completions',
        verbose_name='Квест',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='completions',
        verbose_name='Пользователь',
    )
    completed_at = models.DateTimeField('Выполнено', auto_now_add=True)

    class Meta:
        verbose_name = 'Выполнение квеста'
        verbose_name_plural = 'Выполнения квестов'
        ordering = ['-completed_at']

    def __str__(self):
        return f'{self.user.username} ✓ {self.quest.title}'