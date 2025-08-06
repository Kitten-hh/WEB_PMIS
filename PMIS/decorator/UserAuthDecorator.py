from django.http import HttpResponseRedirect
from django.conf import settings
def login_required(f):
    def wrap(request, *args, **kwargs):
            #this check the session if userid key exist, if not it will redirect to login page
            if settings.SESSION_USERNAME not in request.session.keys():   ## 'admin_username'對應用戶登錄成功後，保存用戶名的Session key
                    return HttpResponseRedirect("/looper/login")   ## /admin/login_page為用戶登錄頁面，如果用戶沒有登錄將跳轉到該頁面
            return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap