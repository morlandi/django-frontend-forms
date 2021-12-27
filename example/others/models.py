import uuid
import os
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from project.templatetags.utils_tags import format_datetime
from .utils import auto_delete_filefields_on_delete


################################################################################
# BaseModel

class BaseModel(models.Model):
    """
    Base class for all models;
    defines common metadata
    """
    class Meta:
        abstract = True
        ordering = ('-created', )  # better choice for UI
        get_latest_by = "-created"

    # Primary key
    id = models.UUIDField('id', default=uuid.uuid4, primary_key=True, unique=True,
        null=False, blank=False, editable=False)

    # metadata
    created = models.DateTimeField(_('created'), null=True, blank=True, )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'), null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
    updated = models.DateTimeField(_('updated'), null=True, blank=True, )
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('updated by'), null=True, blank=True, related_name='+', on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.id)

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" %
            (self._meta.app_label, self._meta.model_name), args=(self.id,))

    def get_absolute_url(self):
        return self.get_admin_url()

    def created_display(self):
        return format_datetime(self.created)
    created_display.short_description = _('Created')
    created_display.admin_order_field = 'created'

    def updated_display(self):
        return format_datetime(self.updated)
    updated_display.short_description = _('Updated')
    updated_display.admin_order_field = 'updated'

    def save(self, *args, **kwargs):
        today = timezone.now()
        if self.created is None:
            self.created = today
        self.updated = today
        return super(BaseModel, self).save(*args, **kwargs)


class File(BaseModel):

    class Meta(BaseModel.Meta):
        abstract = False
        verbose_name = _("File")
        verbose_name_plural = _("Files")

    description = models.CharField(_('Description'), max_length=256, null=False, blank=True)
    file = models.FileField(_('File'), null=True, blank=True, upload_to='uploads/')

    def __str__(self):
        text = self.description
        if len(text) <= 0:
            text = str(self.id)
        return text

models.signals.post_delete.connect(auto_delete_filefields_on_delete, sender=File)


class Picture(BaseModel):

    class Meta(BaseModel.Meta):
        abstract = False
        verbose_name = _("Picture")
        verbose_name_plural = _("Pictures")

    description = models.CharField(_('Description'), max_length=256, null=False, blank=True)
    image = models.ImageField(_('Image'), null=True, blank=True, upload_to='uploads/')

    def __str__(self):
        text = self.description
        if len(text) <= 0:
            text = str(self.id)
        return text

models.signals.post_delete.connect(auto_delete_filefields_on_delete, sender=File)

