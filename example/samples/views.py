import time
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .forms import SimpleForm
from .forms import AdvancedForm


def simple_content(request):
    return HttpResponse('<b>Lorem ipsum dolor sit amet</b>, consectetur adipiscing elit. Proin dignissim dapibus ipsum id elementum. Morbi in justo purus. Duis ornare lobortis nisl eget condimentum. Donec quis lorem nec sapien vehicula eleifend vel sit amet nunc.')


def simple_content_forbidden(request):
    raise PermissionDenied


def simple_content2(request):
    # Either render only the modal content, or a full standalone page
    if request.is_ajax():
        template_name = 'samples/simple_content2_inner.html'
    else:
        template_name = 'samples/simple_content2.html'
    return render(request, template_name, {
    })


def simple_form_validation(request):

    # Simulate network latency
    time.sleep(1.0)

    if request.is_ajax():
        template_name = 'samples/simple_form_inner.html'
    else:
        template_name = 'samples/simple_form.html'

    if request.method == 'POST':
        form = SimpleForm(data=request.POST)
        if form.is_valid():
            form.save()
            if not request.is_ajax():
                messages.info(request, "Form has been validated" )
    else:
        form = SimpleForm()

    return render(request, template_name, {
        'form': form,
    })

def advanced_form_validation(request):

    # Simulate network latency
    time.sleep(1.0)

    if request.is_ajax():
        template_name = 'samples/advanced_form_inner.html'
    else:
        template_name = 'samples/advanced_form.html'

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
