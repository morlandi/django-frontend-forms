import sys
import inspect
from django.template.loader import render_to_string
from django import forms
from django.apps import apps
from backend.models import Artist
from backend.models import Album
from backend.models import Track
from .widgets import AlbumWidget, AlbumWidgetWithAddPopup


# def get_model_form_class(app_label, model_name):

#     model_form_class = None

#     # List all ModelForms in this module
#     model_forms = [
#         klass
#         for name, klass in inspect.getmembers(sys.modules[__name__])
#         if inspect.isclass(klass) and issubclass(klass, forms.ModelForm)
#     ]

#     # Scan ModelForms until we find the right one
#     for model_form in model_forms:
#         model = model_form._meta.model
#         if (model._meta.app_label, model._meta.model_name) == (app_label, model_name):
#             return model_form

#     # Failing that, build a suitable ModelForm on the fly
#     model_class = apps.get_model(app_label, model_name)
#     class _ObjectForm(forms.ModelForm):
#         class Meta:
#             model = model_class
#             exclude = []
#     return _ObjectForm


class SimpleForm(forms.Form):

    value = forms.IntegerField(required=True, label='value', help_text='Enter a value between 1 and 10')

    def save(self):
        return True

    def clean_value(self):
        value = self.cleaned_data['value']
        if value is not None:
            if value < 1 or value > 10:
                raise forms.ValidationError('This value is not accepteble')
        return value


class AdvancedForm(forms.Form):

    value = forms.IntegerField(required=True, label='value', help_text='Enter a value between 1 and 10')
    date = forms.DateField(widget=forms.DateInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = forms.DateInput(attrs={'class': 'datepicker'})

    def save(self):
        return True

    def clean_value(self):
        value = self.cleaned_data['value']
        if value is not None:
            if value < 1 or value > 10:
                raise forms.ValidationError('This value is not accepteble')
        return value


class ArtistCreateForm(forms.ModelForm):

    class Meta:
        model = Artist
        fields = [
            'name',
            'notes',
        ]


class ArtistUpdateForm(forms.ModelForm):

    class Meta:
        model = Artist
        fields = [
            'name',
            'notes',
        ]


class ArtistEditForm(forms.ModelForm):
    """
    To be used for both creation and update
    """

    class Meta:
        model = Artist
        fields = [
            'name',
            'notes',
        ]


class AlbumEditForm(forms.ModelForm):
    """
    To be used for both creation and update
    """

    class Meta:
        model = Album
        fields = [
            'name',
            'artist',
            'year',
        ]


class TrackForm(forms.ModelForm):

    name = forms.CharField(label='Track name')

    class Meta:
        model = Track
        fields = [
            'name',
            'album',
        ]
        widgets = {
            # "data-minimum-input-length":
            # - either set as attr here,
            # - or override build_attrs() in the widget class
            #'album': AlbumWidget(attrs={'data-minimum-input-length': 0,}),
            'album': AlbumWidget(),
        }



class SelectWithAddPopup(forms.Select):
    def render(self, name, *args, **kwargs):
        html = super().render(name, *args, **kwargs)
        popupplus = render_to_string("form/popupplus.html", {'field': name})
        return html + popupplus

class MultipleSelectWithAddPopup(forms.SelectMultiple):
    def render(self, name, *args, **kwargs):
        html = super().render(name, *args, **kwargs)
        popupplus = render_to_string("form/popupplus.html", {'field': name})
        return html + popupplus


class TrackFormEx(forms.ModelForm):

    name = forms.CharField(label='Track name')

    class Meta:
        model = Track
        fields = [
            'name',
            'album',
        ]
        widgets = {
            # "data-minimum-input-length":
            # - either set as attr here,
            # - or override build_attrs() in the widget class
            #'album': AlbumWidget(attrs={'data-minimum-input-length': 0,}),
            'album': AlbumWidgetWithAddPopup(),
        }
