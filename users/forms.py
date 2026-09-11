from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class CustomRegisterForm(UserCreationForm):
    """
    Форма регистрации: стандартные поля Django + обязательный email.
    """
    email = forms.EmailField(required=True, label='Email')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class ProfileForm(forms.ModelForm):
    """
    Форма редактирования профиля: био и аватар.
    """
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']

    def clean_bio(self):
        """Валидация: био не должно быть слишком длинным и без мата."""
        bio = self.cleaned_data.get('bio', '')
        if len(bio) > 500:
            raise forms.ValidationError('Био не должно превышать 500 символов')
        forbidden = ['мат', 'дурак', 'бред']
        for word in forbidden:
            if word in bio.lower():
                raise forms.ValidationError(f'Слово «{word}» использовать нельзя')
        return bio