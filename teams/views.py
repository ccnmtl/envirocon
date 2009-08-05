# Create your views here.
from django.template import RequestContext, loader
from django.http import HttpResponse,Http404
from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response

from teams.models import *


def team_admin(request):
    c = request.actual_course_object
    teams = request.actual_course_object.team_set.all()
    
    return render_to_response('teams/teamassignment.html',
                              {'course':c, 'teams':teams},
                              context_instance=RequestContext(request))
