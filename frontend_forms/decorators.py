from functools import wraps
from django.shortcuts import render


def check_logged_in():
    """
    Decorator for views that checks that the user is logged in,
    showing an error message if necessary.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            template_name = 'frontend_forms/check_logged_in_failed.html'
            if request.is_ajax():
                template_name = 'frontend_forms/check_logged_in_failed_inner.html'
            return render(request, template_name, {})
        return _wrapped_view
    return decorator
