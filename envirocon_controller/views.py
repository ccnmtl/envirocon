from django.template import RequestContext, loader
from django.http import HttpResponse,Http404
from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response


from survey.models import Survey
# Create your views here.

def home(request):
    todo = filled_out_a_profile(request)
    return render_to_response('envirocon_controller/home.html',
                              {'todo':todo},
                              context_instance=RequestContext(request))


#NOT A VIEW
def filled_out_a_profile(request):
    c = getattr(request,'actual_course_object',None)
    if c:
        surveys = Survey.objects.surveys_for(c)
        return [s for s in surveys
                if not s.has_answers_from(request.session.session_key)]
    else:
        return tuple()
        
        