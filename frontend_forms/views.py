import os
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.apps import apps

from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.shortcuts import get_current_site

from .decorators import check_logged_in
from .utils import get_object_by_uuid_or_404
from .forms import get_model_form_class

################################################################################
# Login support
# Borrowed and adapted from Django v1.9.13 (contrib.auth.views)

@csrf_protect
@never_cache
def login(request, template_name='frontend_forms/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(
        redirect_field_name,
        request.GET.get(redirect_field_name, '')
    )

    if request.is_ajax():
        template_name = 'frontend_forms/login_inner.html'

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, allowed_hosts=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            if request.is_ajax():
                return render(request, "frontend_forms/login_successful_message.html", {})
                #return HttpResponse("<h1>Great !</h1> You're logged in")
            else:
                return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    return render(request, template_name, context)


def logout(request, next_page=None,
           template_name='registration/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           extra_context=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    auth_logout(request)

    if next_page is not None:
        next_page = resolve_url(next_page)

    if (redirect_field_name in request.POST or
            redirect_field_name in request.GET):
        next_page = request.POST.get(redirect_field_name,
                                     request.GET.get(redirect_field_name))
        # Security check -- don't allow redirection to a different host.
        if not is_safe_url(url=next_page, host=request.get_host()):
            next_page = request.path

    if next_page:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page)

    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': _('Logged out')
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


################################################################################
# Edit any object

def edit_object(request, app_label, model_name, pk=None):
    """
    Choose a suitable ModelForm class, than invoke generic_edit_view()
    """

    model_form_class = get_model_form_class(app_label, model_name)
    template_name = 'frontend_forms/generic_form.html'

    # TODO: fix in gaia
    # if (app_label, model_name) == ('cbrdb', 'rapportoimpianto'):
    #     template_name = 'modal_helpers/rapportoimpianto_form.html'
    # elif (app_label, model_name) == ('cbrdb', 'rapportomacchina'):
    #     template_name = 'modal_helpers/rapportomacchina_form.html'

    return generic_edit_view(request, model_form_class, pk, template_name)


################################################################################
# A fully generic "edit" view to either create a new object or update an existing one;
# works with any Django model

@check_logged_in()
def generic_edit_view(request, model_form_class, pk=None, template_name='frontend_forms/generic_form.html'):

    model_class = model_form_class._meta.model
    app_label = model_class._meta.app_label
    model_name = model_class._meta.model_name
    model_verbose_name = model_class._meta.verbose_name.capitalize()

    # Retrieve object
    if pk is None:
        # "Add" mode
        object = None
        required_permission = '%s.add_%s' % (app_label, model_name)
    else:
        # Change mode
        object = get_object_by_uuid_or_404(model_class, pk)
        required_permission = '%s.change_%s' % (app_label, model_name)

    # Check user permissions
    if not request.user.is_authenticated or not request.user.has_perm(required_permission):
        raise PermissionDenied

    # Either render only the modal content, or a full standalone page
    # if request.is_ajax():
    #     template_name = 'modal_helpers/generic_form_inner.html'
    # else:
    #     template_name = 'modal_helpers/generic_form.html'
    if request.is_ajax():
        filename, extension = os.path.splitext(template_name)
        template_name = filename + '_inner' + extension

    # Since so many Forms will require the `request` for proper initialization,
    # we wish to pass it to the Form's constructor;
    # however, this raises an exception in the general case, so let's do it only
    # when specifically required with `Form.Meta.want_request = True`
    try:
        forms_wants_request = model_form_class.Meta.wants_request
    except:
        forms_wants_request = False

    if request.method == 'POST':

        #form = model_form_class(instance=object, data=request.POST)
        kwargs = {'instance': object, 'data': request.POST }
        if forms_wants_request:
            kwargs.update({'request': request, })
        form = model_form_class(**kwargs)

        if form.is_valid():
            object = form.save()
            if not request.is_ajax():
                # reload the page
                if pk is None:
                    message = 'The %s "%s" was added successfully.' % (model_verbose_name, object)
                else:
                    message = 'The %s "%s" was changed successfully.' % (model_verbose_name, object)
                messages.success(request, message)
                next = request.META['PATH_INFO']
                return HttpResponseRedirect(next)
            # if is_ajax(), we just return the validated form, so the modal will close
        else:
            print('INVALID FORM:')
            print('non_field_errors: ' + str(form.non_field_errors()))
            print('errors: ' + str(form.errors))

    else:

        # Provide initial values fro specific model
        initial = {}
        #form = model_form_class(instance=object, initial=initial, request=request)
        kwargs = {'instance': object, 'initial': initial, }
        if forms_wants_request:
            kwargs.update({'request': request, })
        form = model_form_class(**kwargs)

    # Add a specific form class attribute so we can characterize the form in the template;
    # i.e.:   <form class="form {{form.form_class}}" ...
    if hasattr(form, 'form_class'):
        form.form_class += ' '
    else:
        form.form_class = ''
    form.form_class += 'form-%s-%s' % (app_label, model_name)

    return render(request, template_name, {
        'object': object,
        'form': form,
    })


################################################################################
# Deleting an object

def delete_object(request, app_label, model_name, pk):

    required_permission = '%s.delete_%s' % (app_label, model_name)
    if not request.user.is_authenticated or not request.user.has_perm(required_permission):
        raise PermissionDenied

    model = apps.get_model(app_label, model_name)
    object = get_object_by_uuid_or_404(model, pk)
    object_id = object.id
    object.delete()

    return HttpResponse(object_id)


################################################################################
# Cloning an object

def clone_object(request, app_label, model_name, pk):

    required_permission = '%s.add_%s' % (app_label, model_name)
    if not request.user.is_authenticated or not request.user.has_perm(required_permission):
        raise PermissionDenied

    model = apps.get_model(app_label, model_name)
    object = get_object_by_uuid_or_404(model, pk)
    new_object = object.clone(request)
    return HttpResponse(new_object.id)
