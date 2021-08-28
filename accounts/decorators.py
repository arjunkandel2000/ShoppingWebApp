from django.http import HttpResponse
from django.shortcuts import redirect

#a decorator is function that takes another function as parameter

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated: #if user is logged in he cannot goto login page withouth logging out
            return redirect('home')

        else:
            return view_func(request,*args, **kwargs) #this view function is argument function loginPage. this function will be excuted at last after logics of upper function are executed
    
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func): # view func is home function
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name # it means the name of first user will be set as group name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page.')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')  #customers will redirected to user page when they want to goto the home page
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper_func
    