import time
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.conf import settings
from frontend_forms.decorators import check_logged_in
from frontend_forms.utils import get_object_by_uuid_or_404
from backend.models import Artist
from .forms import SimpleForm
from .forms import AdvancedForm
from .forms import ArtistCreateForm
from .forms import ArtistUpdateForm
from .forms import ArtistEditForm
from .forms import TrackForm
from .forms import TrackFormEx


def is_ajax(request):
    try:
        is_ajax_request = request.accepts("application/json")
    except AttributeError as e:
        # Django < 4.0
        is_ajax_request = is_ajax(request)
    return is_ajax_request


def simulate_network_latency():
    if settings.DEBUG:
        time.sleep(1.0)


def simple_content(request):
    return HttpResponse('<b>Lorem ipsum dolor sit amet</b>, consectetur adipiscing elit. Proin dignissim dapibus ipsum id elementum. Morbi in justo purus. Duis ornare lobortis nisl eget condimentum. Donec quis lorem nec sapien vehicula eleifend vel sit amet nunc.')


def simple_content_forbidden(request):
    raise PermissionDenied


def simple_content2(request):
    # Either render only the modal content, or a full standalone page
    if is_ajax(request):
        template_name = 'dialogs/simple_content2_inner.html'
    else:
        template_name = 'dialogs/simple_content2.html'
    return render(request, template_name, {
    })


def simple_form_validation(request):

    simulate_network_latency()

    if is_ajax(request):
        template_name = 'dialogs/simple_form_inner.html'
    else:
        template_name = 'dialogs/simple_form.html'

    if request.method == 'POST':
        form = SimpleForm(data=request.POST)
        if form.is_valid():
            form.save()
            if not is_ajax(request):
                messages.info(request, "Form has been validated" )
    else:
        form = SimpleForm()

    return render(request, template_name, {
        'action': reverse('samples:simple-form-validation'),
        'form': form,
    })


def advanced_form_validation(request):

    simulate_network_latency()

    if is_ajax(request):
        template_name = 'dialogs/advanced_form_inner.html'
    else:
        template_name = 'dialogs/advanced_form.html'

    if request.method == 'POST':
        form = AdvancedForm(data=request.POST)
        if form.is_valid():
            form.save()
            if not is_ajax(request):
                messages.info(request, "Form has been validated" )
    else:
        form = AdvancedForm()

    return render(request, template_name, {
        'form': form,
    })


def form_validation_with_feedback(request):

    simulate_network_latency()

    if is_ajax(request):
        template_name = 'dialogs/simple_form_inner.html'
    else:
        template_name = 'dialogs/simple_form.html'

    if request.method == 'POST':
        form = SimpleForm(data=request.POST)
        if form.is_valid():
            form.save()
            if not is_ajax(request):
                messages.info(request, "Form has been validated")
            else:
                return HttpResponse("<h1>Great !</h1> Your form has been validated")
    else:
        form = SimpleForm()

    return render(request, template_name, {
        'action': reverse('samples:form-validation-with-feedback'),
        'form': form,
    })


def simple_form_validation_with_addon(request):

    simulate_network_latency()

    if is_ajax(request):
        template_name = 'dialogs/simple_form_with_addon_inner.html'
    else:
        template_name = 'dialogs/simple_form_with_addon.html'

    if request.method == 'POST':
        form = SimpleForm(data=request.POST)
        if form.is_valid():
            form.save()
            if not is_ajax(request):
                messages.info(request, "Form has been validated" )
    else:
        form = SimpleForm()

    return render(request, template_name, {
        'action': reverse('samples:simple-form-validation-with-addon'),
        'form': form,
    })


@check_logged_in()
def add_artist(request):

    if not request.user.has_perm('backend.add_artist'):
        raise PermissionDenied

    # Either render only the modal content, or a full standalone page
    if is_ajax(request):
        template_name = 'frontend_forms/generic_form_inner.html'
    else:
        template_name = 'dialogs/generic_form.html'

    object = None
    if request.method == 'POST':

        simulate_network_latency()

        form = ArtistCreateForm(data=request.POST)
        if form.is_valid():
            object = form.save()
            if not is_ajax(request):
                # reload the page
                message = 'The object "%s" was added successfully.' % object
                messages.success(request, message)
                next = request.META['PATH_INFO']
                return HttpResponseRedirect(next)
            # if is_ajax(), we just return the validated form, so the modal will close
    else:
        form = ArtistCreateForm()

    return render(request, template_name, {
        'form': form,
        'object': object,
    })


@check_logged_in()
def update_artist(request, pk):

    if not request.user.has_perm('backend.change_artist'):
        raise PermissionDenied

    # Either render only the modal content, or a full standalone page
    if is_ajax(request):
        template_name = 'frontend_forms/generic_form_inner.html'
    else:
        template_name = 'dialogs/generic_form.html'

    object = get_object_by_uuid_or_404(Artist, pk)
    if request.method == 'POST':

        simulate_network_latency()

        form = ArtistUpdateForm(instance=object, data=request.POST)
        if form.is_valid():
            object = form.save()
            if not is_ajax(request):
                # reload the page
                message = 'The object "%s" was changed successfully.' % object
                messages.success(request, message)
                next = request.META['PATH_INFO']
                return HttpResponseRedirect(next)
            # if is_ajax(), we just return the validated form, so the modal will close
    else:
        form = ArtistUpdateForm(instance=object)

    return render(request, template_name, {
        'form': form,
        'object': object,
    })


@check_logged_in()
def edit_artist(request, pk=None):
    """
    Either add a new Artist,
    or change an existing one
    """

    # Retrieve object
    if pk is None:
        # "Add" mode
        object = None
        required_permission = 'backend.add_artist'
    else:
        # "Change" mode
        object = get_object_by_uuid_or_404(Artist, pk)
        required_permission = 'backend.change_artist'

    # Check user permissions
    if not request.user.is_authenticated or not request.user.has_perm(required_permission):
        raise PermissionDenied


    # Either render only the modal content, or a full standalone page
    if is_ajax(request):
        template_name = 'frontend_forms/generic_form_inner.html'
    else:
        template_name = 'dialogs/generic_form.html'

    if request.method == 'POST':

        simulate_network_latency()

        form = ArtistEditForm(instance=object, data=request.POST)
        if form.is_valid():
            object = form.save()
            if not is_ajax(request):
                # reload the page
                if pk is None:
                    message = 'The object "%s" was added successfully.' % object
                else:
                    message = 'The object "%s" was changed successfully.' % object
                messages.success(request, message)
                next = request.META['PATH_INFO']
                return HttpResponseRedirect(next)
            # if is_ajax(), we just return the validated form, so the modal will close
    else:
        form = ArtistEditForm(instance=object)

    return render(request, template_name, {
        'form': form,
        'object': object,
    })


def delete_artist(request, pk):

    required_permission = 'backend.delete_artist'
    if not request.user.is_authenticated or not request.user.has_perm(required_permission):
        raise PermissionDenied

    object = get_object_by_uuid_or_404(Artist, pk)
    object_id = object.id
    object.delete()

    return JsonResponse({'object_id': object_id})


def new_track(request):

    simulate_network_latency()

    if is_ajax(request):
        template_name = 'dialogs/track_form_inner.html'
    else:
        template_name = 'dialogs/track_form.html'

    if request.method == 'POST':
        form = TrackForm(data=request.POST)
        if form.is_valid():
            #form.save()
            if not is_ajax(request):
                messages.info(request, "Form has been validated")
            else:
                return HttpResponse(
                    '<h1>Great !</h1> Your form has been validated<br /><br />You entered <b>"%s"</b>' % form.cleaned_data['name']
                )
    else:
        form = TrackForm()

    #action = request.get_full_path()

    return render(request, template_name, {
        #'action': action,
        'form': form,
    })


def new_track_ex(request):

    simulate_network_latency()

    if is_ajax(request):
        template_name = 'dialogs/track_form_ex_inner.html'
    else:
        template_name = 'dialogs/track_form_ex.html'

    if request.method == 'POST':
        form = TrackFormEx(data=request.POST)
        if form.is_valid():
            #form.save()
            if not is_ajax(request):
                messages.info(request, "Form has been validated")
            else:
                return HttpResponse(
                    '<h1>Great !</h1> Your form has been validated<br /><br />You entered <b>"%s"</b>' % form.cleaned_data['name']
                )
    else:
        form = TrackFormEx()

    #action = request.get_full_path()

    return render(request, template_name, {
        #'action': action,
        'form': form,
    })

