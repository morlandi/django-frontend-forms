from django.template.loader import render_to_string
from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)
from backend.models import Album


class MySelect2Widget():
    """
    Avoid inclusion of select2 by django-select2 as a result of {{form.media}},
    since we're already including everything in base.html
    """
    def _get_media(self):
        return None
    media = property(_get_media)


class AlbumWidget(MySelect2Widget, ModelSelect2Widget):
    model = Album
    search_fields = [
        'name__istartswith',
    ]

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs=base_attrs, extra_attrs=extra_attrs)
        # "data-minimum-input-length";
        # - either override build_attrs() here,
        # - or provide as attr in the instance; for example:
        #   'album': AlbumWidget(attrs={'data-minimum-input-length': 0,}),
        attrs['data-minimum-input-length'] = 0
        return attrs


class AlbumWidgetWithAddPopup(AlbumWidget):

    def render(self, name, *args, **kwargs):
        html = super().render(name, *args, **kwargs)
        popupplus = render_to_string("dialogs/form/popupplus.html", {'field': name})
        return popupplus + html

