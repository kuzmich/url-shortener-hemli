from django import forms

from .models import ShortLink


class ShortenerForm(forms.ModelForm):
    class Meta:
        model = ShortLink
        fields = ['url', 'path']
        error_messages = {
            'url': {
                'required': 'Обязательное поле.',
                'invalid': 'Введите корректный URL.'
            },
            'path': {
                'unique': 'Такое сокращение уже занято.',
                'max_length': 'Сокращение должно быть не длиннее 10 символов.'
            },
        }
