from django.template import RequestContext
from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response, redirect
from django.db import models


Survey = models.get_model('survey', 'survey')
Answer = models.get_model('survey', 'answer')
from envirocon.game.installed_games import InstalledGames
from envirocon.statefulgame.views import team_view_data
from envirocon.envirocon_main.models import GroundWorkClass


def home(request):
    print request.user
    print request.course
    print request.user.is_staff
    todo = filled_out_a_profile(request)
    state = {'todo': todo,
             'games': InstalledGames,
             }
    print todo
    for s in todo:
        print 's'
        print s
    if request.user.is_superuser:
        return render_to_response('envirocon_main/superuser_home.html',
                            state,
                            context_instance=RequestContext(request))
    if getattr(request, 'course', None) is not None:
        if request.user in request.course.faculty:
            state['is_faculty'] = True

        for k, v in team_view_data(request).items():
            state[k] = v

    if request.method == 'POST':
        # so reloads on posts aren't annoying
        return redirect('/')
    return render_to_response('envirocon_main/home.html',
                              state,
                              context_instance=RequestContext(request))


def about(request):
    return render_to_response('envirocon_main/about.html',
                              context_instance=RequestContext(request))


def help(request):
    return render_to_response('envirocon_main/help.html',
                              context_instance=RequestContext(request))


def contact(request):
    return render_to_response('envirocon_main/contact.html',
                              context_instance=RequestContext(request))


def filled_out_a_profile(request):
    print "filled_out_a_profile"
    c = getattr(request, 'course', None)
    if request.user.is_superuser:
        surveys = Survey.objects.all()
        print surveys
        return surveys
    if Survey and c:
        surveys = Survey.objects.surveys_for(c)
        return [sy for sy in surveys
                if not Answer.objects.filter(question__survey=sy,
                                             user=request.user)]
    else:
        return tuple()


def new_envirocon_class(request):
    if not request.user.is_staff:
        return HttpResponseForbidden(
            'Only accounts marked as staff have access to create classes.')
    message = ''
    if request.method == 'POST':
        if 'title' in request.POST:
            g = GroundWorkClass(title=request.POST['title'],
                                creator=request.user)

            message = ('Course Created. At the moment, the survey part is not '
                       'added by default. Also, remember that you need to '
                       'open the assignments to begin.')
            g.copy_survey()

    return render_to_response('envirocon_main/new_class.html',
                              {'message': message},
                              context_instance=RequestContext(request))
