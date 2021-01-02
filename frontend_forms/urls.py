from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog
from . import views

app_name = 'frontend_forms'

urlpatterns = [

    # check at "http://127.0.0.1:8000/frontend_forms/jsi18n/"
    path('jsi18n/', JavaScriptCatalog.as_view(packages=['frontend_forms']), name='javascript-catalog'),

    path('login/', views.login, {'template_name': 'frontend_forms/login.html', }, name="login"),
    path('logout/', views.logout, {'next_page': '/'}, name="logout"),

    path('<str:app_label>/<str:model_name>/add/', views.edit_object, name="object-add"),

    path('<str:app_label>/<str:model_name>/<int:pk>/change/', views.edit_object, name="object-change"),
    path('<str:app_label>/<str:model_name>/<int:pk>/delete/', views.delete_object, name="object-delete"),
    path('<str:app_label>/<str:model_name>/<int:pk>/clone/', views.clone_object, name="object-clone"),

    path('<str:app_label>/<str:model_name>/<uuid:pk>/change/', views.edit_object, name="object-change"),
    path('<str:app_label>/<str:model_name>/<uuid:pk>/delete/', views.delete_object, name="object-delete"),
    path('<str:app_label>/<str:model_name>/<uuid:pk>/clone/', views.clone_object, name="object-clone"),
]
