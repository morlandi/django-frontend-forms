import sys
import inspect
from django.apps import apps
from django import forms
from frontend_forms.app_settings import MODEL_FORMS_MODULES


def _collect_model_forms():
    model_forms = []
    for pattern in MODEL_FORMS_MODULES:
        model_forms += [
            klass
            for name, klass in inspect.getmembers(sys.modules[pattern])
            if inspect.isclass(klass) and issubclass(klass, forms.ModelForm)
        ]
    return model_forms


def get_model_form_class(app_label, model_name):

    # List all ModelForms in this module
    # model_forms = [
    #     klass
    #     for name, klass in inspect.getmembers(sys.modules[__name__])
    #     if inspect.isclass(klass) and issubclass(klass, forms.ModelForm)
    # ]

    model_forms = _collect_model_forms()

    # Scan ModelForms until we find the right one
    for model_form in model_forms:
        model = model_form._meta.model
        if (model._meta.app_label, model._meta.model_name) == (app_label, model_name):
            return model_form

    # Failing that, build a suitable ModelForm on the fly
    model_class = apps.get_model(app_label, model_name)
    class _ObjectForm(forms.ModelForm):
        class Meta:
            model = model_class
            exclude = []
    return _ObjectForm
