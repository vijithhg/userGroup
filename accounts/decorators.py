from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request):
        if request.user.is_authenticated:
            return redirect('home')
        else :
            return view_func(request)
    
        return view_func(request)
    return wrapper_func


def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request):
            group = None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:                
                return view_func(request)
            else:
                return HttpResponse('You are not authorized')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_function(request):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        
        if group=='student':
            return redirect('student')

        if group=='teacher':
            return redirect('teacher')
        if group=='admin':
            return view_func(request)
                
    return wrapper_function