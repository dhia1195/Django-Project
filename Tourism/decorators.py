from django.shortcuts import redirect
from functools import wraps

def login_required(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('auth')  # Replace 'login' with your actual login URL name
        return function(request, *args, **kwargs)
    return wrapper

def logout_required(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if  request.session.get('user_id'):
            return redirect('front')  # Replace 'login' with your actual login URL name
        return function(request, *args, **kwargs)
    return wrapper
