from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.shortcuts import redirect
from . import views
from backend.models import Artist

app_name = 'others'

urlpatterns = [
    path('files_upload/', views.FileFormView.as_view(), name="files_upload"),
    path('chained_selection/', views.chained_selection, name="chained_selection"),
]
