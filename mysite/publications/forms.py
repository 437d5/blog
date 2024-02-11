from django import forms

class CreatePublicatonsForm(forms.Form):
    title = forms.CharField(label="Заголовок", max_length=100, required=True)
    text = forms.CharField(label="Текст поста", widget=forms.Textarea())

