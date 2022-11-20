from django.http import HttpResponse
from django.shortcuts import redirect

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('Вы не имеете прав доступа к этому ресурсу')

    return wrapper_function()