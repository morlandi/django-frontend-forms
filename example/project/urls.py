"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    #path('', lambda x: redirect('/files_upload/'), name='index'),
    path('', include('frontend.urls', namespace='frontend')),
    path('home/', TemplateView.as_view(template_name="pages/index.html"), name="home"),
    path('admin/', admin.site.urls),
    path('frontend_forms/', include('frontend_forms.urls', namespace='frontend_forms')),
    path('samples/', include('samples.urls', namespace='samples')),
    path('select2/', include('django_select2.urls')),
    path('others/', include('others.urls', namespace='others')),
] \
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
