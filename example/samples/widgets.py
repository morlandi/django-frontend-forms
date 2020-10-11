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
