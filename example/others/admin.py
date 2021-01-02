from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from .models import File
from .models import Picture


################################################################################
# BaseModelAdmin

class BaseModelAdmin(admin.ModelAdmin):
    """
    Base class for 'shared' model admins;
    manages common metadata
    """
    date_hierarchy = 'created'
    search_fields = ['=id', ]
    list_display = [
        '__str__',
        'view_on_site_link',
        'created_display',
        'updated_display',
    ]
    list_filter = ['created', ]
    readonly_fields = ['id', 'created', 'created_by', 'updated', 'updated_by', ]

    save_on_top = False
    list_per_page = 100

    def view_on_site_link(self, obj):
        url = obj.get_absolute_url()
        html = '<a href="%s" class="link-with-icon link-view">view</a>' % url
        return mark_safe(html)
    view_on_site_link.short_description = 'View'

    def save_model(self, request, obj, form, change):
        today = timezone.now()
        if not change:
            obj.created_by = request.user
            obj.created = today
        obj.updated_by = request.user
        obj.updated = today
        # obj.save()
        super(BaseModelAdmin, self).save_model(request, obj, form, change)


@admin.register(File)
class FileAdmin(BaseModelAdmin):

    def get_list_display(self, request):
        list_display = BaseModelAdmin.list_display[:]
        list_display.insert(1, 'description')
        return list_display


@admin.register(Picture)
class PictureAdmin(BaseModelAdmin):

    def get_list_display(self, request):
        list_display = BaseModelAdmin.list_display[:]
        list_display.insert(1, 'description')
        return list_display
