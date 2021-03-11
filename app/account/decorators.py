from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You\'re already logged in.')
            return redirect('account:sample')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwrgs):
            if request.user.is_authenticated:
                if 'judge' in allowed_roles and request.user.is_judge:
                    return view_func(request, *args, **kwrgs)
                elif 'tl' in allowed_roles and request.user.is_tl:
                    return view_func(request, *args, **kwrgs)
                elif 'admin' in allowed_roles and request.user.is_admin:
                    return view_func(request, *args, **kwrgs)
                else:
                    messages.error(
                        request, 'You are not authorized to view the page. Please login with a permitted account.')
                    return redirect('account:sample')
            else:
                messages.error(request, 'Login first to view the page.')
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return wrapper_func
    return decorator
