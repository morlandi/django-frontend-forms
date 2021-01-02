from django import forms
from django_select2.forms import ModelSelect2Widget

from backend.models import Artist
from backend.models import Album
from backend.models import Track


class FileForm(forms.Form):
    title = forms.CharField(required=True)
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class ChainedSelectionForm(forms.Form):

    artist = forms.ModelChoiceField(
        queryset=Artist.objects.all(),
        label="Artist",
        widget=ModelSelect2Widget(
            model=Artist,
            search_fields=['name__icontains'],
            attrs={'data-minimum-input-length': 0,},
        )
    )

    album = forms.ModelChoiceField(
        queryset=Album.objects.all(),
        label="Album",
        widget=ModelSelect2Widget(
            model=Album,
            search_fields=['name__icontains'],
            attrs={'data-minimum-input-length': 0,},
            dependent_fields={'artist': 'artist'},
        )
    )

    track = forms.ModelChoiceField(
        queryset=Track.objects.all(),
        label="Track",
        widget=ModelSelect2Widget(
            model=Track,
            search_fields=['name__icontains'],
            attrs={'data-minimum-input-length': 0,},
            dependent_fields={'album': 'album'},
        )
    )

