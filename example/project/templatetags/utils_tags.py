import datetime
import imghdr
from PIL import Image
from django import template
from django.utils import timezone
from django.utils import formats

register = template.Library()


@register.filter
def pdb(element):
    """ Usage: {{ template_var|pdb }}
        then inspect 'element' from pdb
    """
    import pdb
    pdb.set_trace()
    return element


@register.filter
def ipdb(element):
    """ Usage: {{ template_var|pdb }}
        then inspect 'element' from pdb
    """
    import ipdb
    ipdb.set_trace()
    return element


@register.filter
def format_datetime(dt, include_time=True, include_seconds=False, exclude_date=False):
    """
    Apply datetime format suggested for all admin views.

    Here we adopt the following rule:
    1) format date according to active localization
    2) append time in military format
    """

    if dt is None:
        return ''

    if not isinstance(dt, datetime.datetime):
        include_time = False

    if include_time:
        dt = timezone.localtime(dt)

    if exclude_date:
        text = ''
    else:
        text = formats.date_format(dt, use_l10n=True, format='SHORT_DATE_FORMAT')
    if include_time:
        if len(text):
            text += ' '
        text += dt.strftime('%H:%M')
        if include_seconds:
            text += dt.strftime(':%S')
    return text


@register.filter
def imagesize(obj):
    image_type = imghdr.what(obj.file)
    if image_type is None:
        return ''

    image = Image.open(obj.file)
    w, h = image.size
    text = '%s (%dx%d)' % (image_type, w, h)
    return text
