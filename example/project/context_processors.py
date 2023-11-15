from django.conf import settings


def main_settings(request):
    return {
        'USE_VANILLA_JS': settings.USE_VANILLA_JS,
    }
