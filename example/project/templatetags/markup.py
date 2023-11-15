"""
Adapted from:
https://github.com/Alir3z4/django-markwhat

See also:
- http://www.codekoala.com/posts/syntax-highlighting-rest-pygments-and-django/
- http://stefan.sofa-rockers.org/2010/01/13/django-highlighting-rest-using-pygments/


Set of "markup" template filters for Django.
These filters transform plain text
markup syntaxes to HTML; currently there is support for:

    * Textile, which requires the PyTextile library available at
      http://loopcore.com/python-textile/

    * Markdown, which requires the Python-markdown library from
      http://www.freewisdom.org/projects/python-markdown

    * reStructuredText, which requires docutils from http://docutils.sf.net/
"""

from django import template
from django.conf import settings
#from django.utils.encoding import smart_str, force_text
try:
    from django.utils.encoding import force_text
except:
    from django.utils.encoding import force_str as force_text
from django.utils.encoding import smart_str

from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
def textile(value):
    """
    :type value: str

    :rtype: str
    """
    import textile

    return mark_safe(force_text(
        textile.textile(smart_str(value), encoding='utf-8', output='utf-8'))
    )


@register.filter(is_safe=True)
def markdown(value, args=''):
    """
    Runs Markdown over a given value, optionally using various
    extensions python-markdown supports.

    Syntax::

        {{ value|markdown:"extension1_name,extension2_name..." }}

    To enable safe mode, which strips raw HTML and only returns HTML
    generated by actual Markdown syntax, pass "safe" as the first
    extension in the list.

    If the version of Markdown in use does not support extensions,
    they will be silently ignored.

    :type value: str
    :type args: str

    :rtype: str
    """
    import markdown

    extensions = [e for e in args.split(',') if e]
    if len(extensions) > 0 and extensions[0] == "safe":
        extensions = extensions[1:]
        safe_mode = True
    else:
        safe_mode = False

    return mark_safe(markdown.markdown(
        force_text(value),
        extensions,
        safe_mode=safe_mode,
        enable_attributes=(not safe_mode)
    ))


@register.filter(is_safe=True)
def restructuredtext(value):
    """
    :type value: str
    :rtype: str
    """
    from docutils.core import publish_parts

    docutils_settings = getattr(
        settings,
        "RESTRUCTUREDTEXT_FILTER_SETTINGS", {
            'syntax_highlight': 'short',
        }
    )
    parts = publish_parts(
        source=smart_str(value),
        writer_name="html4css1",
        settings_overrides=docutils_settings,
    )
    return mark_safe(force_text(parts["fragment"]))
