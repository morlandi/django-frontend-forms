from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)
from backend.models import Album

class MySelect2Widget():

    def _get_media(self):
        return None

    media = property(_get_media)


#class AlbumWidget(ModelSelect2Widget):
class AlbumWidget(MySelect2Widget, ModelSelect2Widget):
    model = Album
    search_fields = [
        'name__istartswith',
    ]
