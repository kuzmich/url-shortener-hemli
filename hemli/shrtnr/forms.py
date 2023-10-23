from django import forms


class ShortenerForm(forms.Form):
    long_url = forms.URLField(label="Длинный URL")
    custom_path = forms.CharField(label='Желаемый URL', required=False)
