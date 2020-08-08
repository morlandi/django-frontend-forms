from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.views.generic.edit import FormView
from .forms import FileForm
try:
    from django.urls import reverse
except ModuleNotFoundError as e:
    # for Django < v1.10
    from django.core.urlresolvers import reverse
from .models import File


def clear_all_files(request):
    File.objects.all().delete()
    return HttpResponseRedirect(reverse('index'))


class FileFormView(FormView):
    template_name = 'pages/files_upload.html'
    form_class = FileForm
    success_url = '/'
    use_dropzonejs = True

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['use_dropzonejs'] = bool(int(self.request.GET.get('use_dropzonejs', self.use_dropzonejs)))
        return kwargs

    # def get_success_url(self):
    #     """Return the URL to redirect to after processing a valid form."""
    #     if not self.success_url:
    #         raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
    #     return str(self.success_url)  # success_url may be lazy

    # def form_valid(self, form):
    #     """If the form is valid, redirect to the supplied URL."""
    #     return HttpResponseRedirect(self.get_success_url())

    # def form_invalid(self, form):
    #     """If the form is invalid, render the invalid form."""
    #     return self.render_to_response(self.get_context_data(form=form))

    # def get(self, request, *args, **kwargs):
    #     """Handle GET requests: instantiate a blank version of the form."""
    #     return self.render_to_response(self.get_context_data())

    # def post(self, request, *args, **kwargs):
    #     """
    #     Handle POST requests: instantiate a form instance with the passed
    #     POST variables and then check if it's valid.
    #     """
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        files = request.FILES.getlist('file')

        is_ajax = request.is_ajax()
        print('is_ajax: ' + str(is_ajax))
        print(request.POST)

        if form.is_valid():
            for f in files:
                messages.info(request, f)
                print(f)
                # with open(Path(settings.MEDIA_ROOT + "/" + f.name).resolve(), 'wb+') as destination:
                #     for chunk in f.chunks():
                #         destination.write(chunk)
            if not is_ajax:
                return HttpResponseRedirect(self.get_success_url())
            else:
                return JsonResponse({'form': True})
        else:
            if not is_ajax:
                return self.render_to_response(self.get_context_data(form=form))
            else:
                return JsonResponse({'form': False})
