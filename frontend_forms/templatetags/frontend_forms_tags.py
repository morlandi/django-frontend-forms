import math
import json
import re
from django.urls.exceptions import NoReverseMatch
from django import template
from django.urls import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils import timezone
from frontend_forms.app_settings import FORM_LAYOUT_FLAVOR
from frontend_forms.app_settings import FORM_LAYOUT_DEFAULT

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

################################################################################
# Support for generic editing in the front-end

@register.filter
def model_verbose_name(model):
    """
    Sample usage:
        {{model|model_name}}
    """
    return model._meta.verbose_name


@register.filter
def model_verbose_name_plural(model):
    """
    Sample usage:
        {{model|model_name}}
    """
    return model._meta.verbose_name_plural


@register.filter
def model_name(model):
    """
    Sample usage:
        {{model|model_name}}
    """
    return model._meta.model_name


@register.filter
def app_label(model):
    """
    Sample usage:
        {{model|app_label}}
    """
    return model._meta.app_label


@register.filter
def change_object_url(object):
    """
    Given an object, returns the "canonical" url for object editing:

        <a href="{{object|change_object_url}}">change this object</a>
    """
    model = object.__class__
    return reverse('frontend_forms:object-change', args=(model._meta.app_label, model._meta.model_name, object.id))


@register.filter
def change_model_url(model, object_id):
    """
    Given a model and an object id, returns the "canonical" url for object editing:

        <a href="{{model|change_model_url:object.id}}">change this object</a>
    """
    return reverse('frontend_forms:object-change', args=(model._meta.app_label, model._meta.model_name, object_id))


@register.filter
def add_model_url(model):
    """
    Given a model, return the "canonical" url for adding a new object:

        <a href="{{model|add_model_url}}">add a new object</a>
    """
    return reverse('frontend_forms:object-add', args=(model._meta.app_label, model._meta.model_name))


@register.filter
def delete_object_url(object):
    """
    Given an object, returns the "canonical" url for object deletion:

        <a href="{{object|delete_object_url}}">delete this object</a>
    """
    model = object.__class__
    return reverse('frontend_forms:object-delete', args=(model._meta.app_label, model._meta.model_name, object.id))


@register.filter
def delete_model_url(model, object_id):
    """
    Given a model and an object id, returns the "canonical" url for object deletion:

        <a href="{{model|delete_model_url:object.id}}">delete this object</a>
    """
    return reverse('frontend_forms:object-delete', args=(model._meta.app_label, model._meta.model_name, object_id))


@register.filter
def clone_object_url(object):
    """
    Given an object, returns the "canonical" url for object cloning:

        <a href="{{object|clone_object_url}}">clone this object</a>
    """
    model = object.__class__
    return reverse('frontend_forms:object-clone', args=(model._meta.app_label, model._meta.model_name, object.id))


@register.filter
def clone_model_url(model, object_id):
    """
    Given a model and an object id, returns the "canonical" url for object cloning:

        <a href="{{model|clone_model_url:object.id}}">clone this object</a>
    """
    return reverse('frontend_forms:object-clone', args=(model._meta.app_label, model._meta.model_name, object_id))


@register.simple_tag(takes_context=True)
def testhasperm(context, model, action):
    """
    Returns True iif the user have the specified permission over the model.
    For 'model', we accept either a Model class, or a string formatted as "app_label.model_name".

    Sample usage:

        {% testhasperm model 'view' as can_view_objects %}
        {% if not can_view_objects %}
            <h2>Sorry, you have no permission to view these objects</h2>
        {% endif %}
    """
    user = context['request'].user
    if isinstance(model, str):
        app_label, model_name = model.split('.')
    else:
        app_label = model._meta.app_label
        model_name = model._meta.model_name
    required_permission = '%s.%s_%s' % (app_label, action, model_name)
    return user.is_authenticated and user.has_perm(required_permission)


@register.tag
def ifhasperm(parser, token):
    """
    Check user permission over specified model.
    (You can specify either a model or an object).

    Sample usage:

        {% ifhasperm model 'add' %}
            <div style="color: #090">User can add objects</div>
        {% else %}
            <div style="color: #900">User cannot add objects</div>
        {% endifhasperm %}
    """

    # Separating the tag name from the parameters
    try:
        tag, model, action = token.contents.split()
    except (ValueError, TypeError):
        raise template.TemplateSyntaxError(
            "'%s' tag takes three parameters" % tag)

    default_states = ['ifhasperm', 'else']
    end_tag = 'endifhasperm'

    # Place to store the states and their values
    states = {}

    # Let's iterate over our context and find our tokens
    while token.contents != end_tag:
        current = token.contents
        states[current.split()[0]] = parser.parse(default_states + [end_tag])
        token = parser.next_token()

    model_var = parser.compile_filter(model)
    action_var = parser.compile_filter(action)
    return CheckPermNode(states, model_var, action_var)


class CheckPermNode(template.Node):
    def __init__(self, states, model_var, action_var):
        self.states = states
        self.model_var = model_var
        self.action_var = action_var

    def render(self, context):

        # Resolving variables passed by the user
        model = self.model_var.resolve(context)
        action = self.action_var.resolve(context)

        # Check user permission
        if testhasperm(context, model, action):
            html = self.states['ifhasperm'].render(context)
        else:
            html = self.states['else'].render(context) if 'else' in self.states else ''

        return html

################################################################################
# Form rendering helpers

@register.filter()
def boostrap_field_class(field):
    text = "class=form-control"
    if field.errors:
        text += " is-invalid"
    elif field.form.is_bound:
        text += " is-valid"
    return text

# Adapted from:
# https://blog.joeymasip.com/how-to-add-attributes-to-form-widgets-in-django-templates/
@register.filter(name='add_field_attrs')
def add_field_attrs(field, css):
    """
    Sample usage:

        {{ field|add_field_attrs:"class=form-control,style=border: 1px solid red;" }}

    Prepending a value with "^" means: replace (instead of append); example:

        {% render_form_field form.username extra_attrs="autocomplete=^off,autocorrect=off,autocapitalize=none" %}
    """

    # attrs = {}
    # definition = css.split(',')
    # for d in definition:
    #     # if ':' not in d:
    #     #     attrs['class'] = d
    #     # else:
    #     #     key, val = d.split('=')
    #     #     attrs[key] = val
    #     if '=' not in d:
    #         key = 'class'
    #         val = d
    #     else:
    #         key, val = d.split('=')
    #     if key in attrs:
    #         attrs[key] += ' ' + val
    #     else:
    #         attrs[key] = val

    # Pars tokens and collect result as {key: [value1, value2, ...]
    attrs_lists = {}
    tokens = css.split(',')
    for token in tokens:
        # assume key='class' when key not specified
        if '=' not in token:
            key = 'class'
            val = token
        else:
            key, val = token.split('=')
        # Make suer we have and entry for this key
        if not key in attrs_lists:
            attrs_lists[key] = []
        # '^' means "replace"
        if val.startswith('^'):
            attrs_lists[key] = [val[1:], ]
        else:
            # append to existing values, but avoid duplicates
            if not val in attrs_lists[key]:
                attrs_lists[key].append(val)

    # Convert from:
    #     {key: [value1, value2, ...], }
    # to:
    #     {key: "value1 value2 ...", }
    attrs = {k: ' '.join(v) for k, v in attrs_lists.items()}

    return field.as_widget(attrs=attrs)

@register.inclusion_tag('frontend_forms/render_form_field.html')
def render_form_field(field, flavor=None, extra_attrs='', layout=FORM_LAYOUT_DEFAULT, index=0, addon=''):

    # Example:
    #   {'class': 'user-position', 'style': 'border: 1px solid red;'} --> 'class=user-position,style=border: 1px solid red;'

    assert bool(field), "render_form_field(): no field specified"

    attrs = field.field.widget.attrs
    field_attrs = ','.join(['='.join([key,str(value)]) for key,value in attrs.items()])

    if extra_attrs:
        field_attrs = ','.join([field_attrs, extra_attrs])

    return {
        'field': field,
        'field_attrs': field_attrs,
        'FORM_LAYOUT_FLAVOR': flavor if flavor is not None else FORM_LAYOUT_FLAVOR,
        'layout': layout,
        'index': index,
        'addon': addon,
    }

@register.inclusion_tag('frontend_forms/render_form.html')
def render_form(form, flavor=None, layout=FORM_LAYOUT_DEFAULT):
    return {
        'form': form,
        'FORM_LAYOUT_FLAVOR': flavor if flavor is not None else FORM_LAYOUT_FLAVOR,
        'layout': layout,
    }
