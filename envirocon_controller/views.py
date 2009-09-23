from django.template import RequestContext, loader
from django.http import HttpResponse,Http404
from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response
from django.db import models

Survey = models.get_model('survey','survey')
from game.installed_games import InstalledGames
from statefulgame.views import team_view_data


def home(request):
    todo = filled_out_a_profile(request)
    state = {'todo':todo,
             'games':InstalledGames,
             }

    if hasattr(request,'course'):
        if request.user in request.course.faculty:
            state['is_faculty'] = True
            
        for k,v in team_view_data(request).items():
            state[k] = v


    return render_to_response('envirocon_controller/home.html',
                              state,
                              context_instance=RequestContext(request))


#NOT A VIEW
def filled_out_a_profile(request):
    c = getattr(request,'course',None)
    if Survey and c:
        surveys = Survey.objects.surveys_for(c)
        return [sy for sy in surveys
                if not sy.has_answers_from(request.session.session_key)]
    else:
        return tuple()
        
        
