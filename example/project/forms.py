from django import forms


class FileForm(forms.Form):
    title = forms.CharField(required=True)
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
