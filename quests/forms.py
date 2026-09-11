from django import forms
from .models import Quest


class QuestForm(forms.ModelForm):
    """
    Форма создания/редактирования квеста.
    Поля board заполняется автоматически во view.
    """
    class Meta:
        model = Quest
        fields = ['title', 'description', 'difficulty', 'xp_reward', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название квеста'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Что нужно сделать?'}),
        }