from django.conf import settings

def set_global_parameters(request):
    return {
        'salc_server': settings.SALC_SERVER,
        #'csrf_cookie_name':settings.CSRF_COOKIE_NAME
    }