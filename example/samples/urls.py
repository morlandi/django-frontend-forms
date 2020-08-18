from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.shortcuts import redirect
from . import views

app_name = 'samples'

urlpatterns = [
    path('basic-modal/',
        TemplateView.as_view(template_name="samples/basic_modal.html"),
        name="basic-modal"),
    path('basic-modal-which-returns-a-value/',
        TemplateView.as_view(template_name="samples/basic_modal_which_returns_a_value.html"),
        name="basic-modal-which-returns-a-value"),
    path('basic-modal-with-bootstrap/',
        TemplateView.as_view(template_name="samples/basic_modal_with_bootstrap.html"),
        name="basic-modal-with-bootstrap"),

    path('simple-dialogs/',
        TemplateView.as_view(template_name="samples/simple_dialogs.html"),
        name="simple-dialogs"),
    path('simple-content', views.simple_content, name="simple-content"),
    path('simple-content-forbidden', views.simple_content_forbidden, name="simple-content-forbidden"),
    path('simple-content2', views.simple_content2, name="simple-content2"),

    path('form-submission/',
        TemplateView.as_view(template_name="samples/form_submission.html"),
        name="form-sumbission"),

    path('simple-form-validation', views.simple_form_validation, name="simple-form-validation"),
    path('advanced-form-validation', views.advanced_form_validation, name="advanced-form-validation"),
]
