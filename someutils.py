#!ve/bin/python


from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponseNotAllowed

from django.http import HttpResponse


from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.http import urlquote
from django.http import HttpResponseRedirect
class AuthRequirementMiddleware(object):
    def process_request(self, request):
        path = urlquote(request.get_full_path())
        try:
            for exempt_path in settings.ANONYMOUS_PATHS:
                try:
                    if path.startswith(exempt_path):
                        return None
                except TypeError: # it wasn't a string object .. must be a regex
                    if exempt_path.match(path):
                        return None
        except AttributeError:
            pass


        if request.user.is_authenticated():
            return None

        #from django.shortcuts import get_object_or_404
        #request.coursename = "A&HW 5050 - Special Topics: Vietnam Now!"
        # CUcourse_A&HWY5050_001_2009_2
        #request.course = Group.objects.get_or_create(name='summer09')[0]

        return HttpResponseRedirect('%s?%s=%s' % (
            settings.LOGIN_URL,
            REDIRECT_FIELD_NAME,
            path))
