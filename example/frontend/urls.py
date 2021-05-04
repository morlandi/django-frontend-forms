from django.urls import path
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', lambda x: redirect('/page/1/')),
    path('page/<int:page>/', views.page, name="page"),
    path('page/<int:page>/view-code/', views.code, name="code"),
]
