from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CreatePublicatonsForm(forms.Form):
    title = forms.CharField(label="Заголовок", max_length=100, required=True)
    text = forms.CharField(label="Текст поста", widget=forms.Textarea())

class CreateCommentsForm(forms.Form):
    text = forms.CharField(label="Текст комментария", max_length=100, required=True, widget=forms.Textarea())

    def clean_text(self):
        text = self.cleaned_data['text']
        censor_list = ["хуй", "пизда", "пидор", "блять"]

        for i in censor_list:
            if i in text:
                raise ValidationError("Invalid comment text - obscene language")

        return text