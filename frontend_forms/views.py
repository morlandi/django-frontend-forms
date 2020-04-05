import os
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.apps import apps
from django.contrib.auth.decorators import login_required
from .utils import get_object_by_uuid_or_404
from .forms import get_model_form_class


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

@login_required
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

    if request.method == 'POST':
        form = model_form_class(instance=object, data=request.POST)
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

        # Provide initial values fro specific model
        initial = {}
        # TODO: fix in gaia
        # if (app_label, model_name) == ('cbrdb', 'rapportoimpianto') or \
        #    (app_label, model_name) == ('cbrdb', 'rapportomacchina'):
        #     initial = {'autore': request.user, }

        form = model_form_class(instance=object, initial=initial)

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

