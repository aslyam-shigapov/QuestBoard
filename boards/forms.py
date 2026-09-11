from django import forms
from .models import Board


class BoardForm(forms.ModelForm):
    """
    Форма создания/редактирования доски.
    Поля owner и created_at заполняются автоматически во view.
    """
    class Meta:
        model = Board
        fields = ['title', 'description', 'cover', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название доски'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'О чём эта доска?'}),
        }