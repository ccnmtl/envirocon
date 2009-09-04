from django.template import RequestContext, loader
from django.http import HttpResponse,Http404
from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response
from django.db import models

Survey = models.get_model('survey','survey')
from game.installed_games import InstalledGames

def home(request):
    todo = filled_out_a_profile(request)
    return render_to_response('envirocon_controller/home.html',
                              {'todo':todo,
                               'games':InstalledGames,
                               },
                              context_instance=RequestContext(request))


#NOT A VIEW
def filled_out_a_profile(request):
    c = getattr(request,'actual_course_object',None)
    if Survey and c:
        surveys = Survey.objects.surveys_for(c)
        return [sy for sy in surveys
                if not sy.has_answers_from(request.session.session_key)]
    else:
        return tuple()
        
        
