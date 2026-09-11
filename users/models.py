from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Расширенный профиль пользователя: XP, уровень, аватар, био.
    Связан с User один-к-одному.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь',
    )
    xp = models.PositiveIntegerField('Опыт (XP)', default=0)
    level = models.PositiveIntegerField('Уровень', default=1)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True, null=True)
    bio = models.TextField('О себе', blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль {self.user.username} (ур. {self.level})'