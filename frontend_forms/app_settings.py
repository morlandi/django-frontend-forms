from django.conf import settings

FORM_LAYOUT_FLAVOR = getattr(settings, 'FRONTEND_FORMS_FORM_LAYOUT_FLAVOR', "generic")
MODEL_FORMS_MODULES = getattr(settings, 'FRONTEND_FORMS_MODEL_FORMS_MODULES', ['frontend.forms', ])
FORM_LAYOUT_DEFAULT = getattr(settings, 'FRONTEND_FORMS_FORM_LAYOUT_DEFAULT', 'vertical')

