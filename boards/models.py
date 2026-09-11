from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    """
    Доска — тематический набор квестов.
    Может быть публичной или приватной.
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='boards',
        verbose_name='Владелец',
    )
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    cover = models.ImageField('Обложка', upload_to='boards/', blank=True, null=True)
    is_public = models.BooleanField('Публичная', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'
        ordering = ['-created_at']

    def __str__(self):
        return self.title