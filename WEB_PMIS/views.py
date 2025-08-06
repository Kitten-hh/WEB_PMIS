from django.http import HttpResponseRedirect

def csrf_failure(request, reason=""):
    return HttpResponseRedirect("/looper");