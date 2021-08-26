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