# Create your views here.
from django.template import RequestContext, loader
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response
from django.db import models

User = models.get_model('auth','user')
Team = models.get_model('teams','team')

Survey = models.get_model('survey','survey')
Question = models.get_model('survey','question')
Answer = models.get_model('survey','answer')


def addteam(request,course_id=None):
    #TODO: test for addteam permission or faculty
    tms = tuple()
    if request.method == "POST":    
        if course_id is None:
            course_id = request.actual_course_object.id
        count = int(request.POST.get('count',1))
        tms = [Team.objects.create(course_id=course_id)
               for i in range(count)]
        
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def addmember(request, user_id, course_id=None, team_id=None):
    #TODO: test for addteam permission or faculty
    done = 'no'
    if request.method == "POST":
        course = (course_id is None) and request.actual_course_object \
                 or Course.objects.get(pk=course_id)
            
        user = User.objects.get(pk=user_id)
        current_team = Team.objects.by_user(user, course)
        if current_team and current_team.id != team_id:
            current_team.group.user_set.remove(user)
        if team_id:
            new_team = Team.objects.get(pk=team_id)
            new_team.group.user_set.add(user)
        done = 'yes'
    return HttpResponse(done)

def team_admin(request):
    c = request.actual_course_object
    teams = request.actual_course_object.team_set.all()
    
    return render_to_response('teams/teamassignment.html',
                              {'course':c,
                               'teams':teams,
                               'surveys':course_survey(c),
                               },
                              context_instance=RequestContext(request))

#not view
def course_survey(course):
    if Survey:
        studs = dict([(st.id,{'record':st,'surveys':[]}) for st in course.students])
        
        surveys = Survey.objects.surveys_for(course)
        for sy in surveys:
            questions = Question.objects.filter(survey=sy).order_by('order')
            for st in course.students:
                ans = []
                for q in questions:
                    a = Answer.objects.filter(user=st,question=q)
                    if len(a):
                        ans.append(a)
                    else:
                        ans.append(q)
                studs[st.id]['surveys'].append(ans)
        return studs
    else:
        return None
