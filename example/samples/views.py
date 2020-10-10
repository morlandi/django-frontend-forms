import time
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from .forms import SimpleForm
from .forms import AdvancedForm
from .forms import TrackForm


def simple_content(request):
    return HttpResponse('<b>Lorem ipsum dolor sit amet</b>, consectetur adipiscing elit. Proin dignissim dapibus ipsum id elementum. Morbi in justo purus. Duis ornare lobortis nisl eget condimentum. Donec quis lorem nec sapien vehicula eleifend vel sit amet nunc.')


def simple_content_forbidden(request):
    raise PermissionDenied


def simple_content2(request):
    # Either render only the modal content, or a full standalone page
    if request.is_ajax():
        template_name = 'dialogs/simple_content2_inner.html'
    else:
        template_name = 'dialogs/simple_content2.html'
    return render(request, template_name, {
    })


def simple_form_validation(request):

    # Simulate network latency
    time.sleep(1.0)

    if request.is_ajax():
        template_name = 'dialogs/simple_form_inner.html'
    else:
        template_name = 'dialogs/simple_form.html'

    if request.method == 'POST':
        form = SimpleForm(data=request.POST)
        if form.is_valid():
            form.save()
            if not request.is_ajax():
                messages.info(request, "Form has been validated" )
    else:
        form = SimpleForm()

    return render(request, template_name, {
        'action': reverse('samples:simple-form-validation'),
        'form': form,
    })


def advanced_form_validation(request):

    # Simulate network latency
    time.sleep(1.0)

    if request.is_ajax():
        template_name = 'dialogs/advanced_form_inner.html'
    else:
        template_name = 'dialogs/advanced_form.html'

    if request.method == 'POST':
        form = AdvancedForm(data=request.POST)
        if form.is_valid():
            form.save()
            if not request.is_ajax():
                messages.info(request, "Form has been validated" )
    else:
        form = AdvancedForm()

    return render(request, template_name, {
        'form': form,
    })


def form_validation_with_feedback(request):

    # Simulate network latency
    time.sleep(1.0)

    if request.is_ajax():
        template_name = 'dialogs/simple_form_inner.html'
    else:
        template_name = 'dialogs/simple_form.html'

    if request.method == 'POST':
        form = SimpleForm(data=request.POST)
        if form.is_valid():
            form.save()
            if not request.is_ajax():
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

    # Simulate network latency
    time.sleep(1.0)

    if request.is_ajax():
        template_name = 'dialogs/simple_form_with_addon_inner.html'
    else:
        template_name = 'dialogs/simple_form_with_addon.html'

    if request.method == 'POST':
        form = SimpleForm(data=request.POST)
        if form.is_valid():
            form.save()
            if not request.is_ajax():
                messages.info(request, "Form has been validated" )
    else:
        form = SimpleForm()

    return render(request, template_name, {
        'action': reverse('samples:simple-form-validation-with-addon'),
        'form': form,
    })


def new_track(request):

    # Simulate network latency
    time.sleep(1.0)

    if request.is_ajax():
        template_name = 'dialogs/track_form_inner.html'
    else:
        template_name = 'dialogs/track_form.html'

    if request.method == 'POST':
        form = TrackForm(data=request.POST)
        if form.is_valid():
            #form.save()
            if not request.is_ajax():
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

