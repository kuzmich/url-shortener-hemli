from django import forms

from .models import ShortLink


class ShortenerForm(forms.ModelForm):
    class Meta:
        model = ShortLink
        fields = ['url', 'path']
        error_messages = {
            'path': {
                'unique': 'Такое сокращение уже занято.'
            }
        }
