# Create your views here.
from django.template import RequestContext, loader
from django.http import HttpResponse,Http404,HttpResponseRedirect,HttpResponseForbidden
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
            course_id = request.course.id
        count = int(request.POST.get('count',1))
        tms = [Team.objects.create(course_id=course_id)
               for i in range(count)]
        
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def addmember(request, user_id, course_id=None, team_id=None):
    #TODO: test for addteam permission or faculty
    done = 'no'
    if request.method == "POST":
        course = (course_id is None) and request.course \
                 or Course.objects.get(pk=course_id)
        if not course.is_faculty(request.user):
            return HttpResponseForbidden()
        user = User.objects.get(pk=user_id)
        current_team = Team.objects.by_user(user, course)
        if current_team and current_team.id != team_id:
            current_team.group.user_set.remove(user)
        if team_id:
            new_team = Team.objects.get(pk=team_id)
            new_team.group.user_set.add(user)
        done = 'yes'
    return HttpResponse(done)

def deleteteam(request, team_id, remove_group=True):
    if request.method in ("POST","DELETE"):
        team = get_object_or_404(Team, pk=team_id)
        if not team.course.is_faculty(request.user):
            return HttpResponseForbidden()

        if remove_group:
            team.group.delete()
        team.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def team_admin(request):
    c = request.course
    teams = request.course.team_set.all()
    if not request.course.is_faculty(request.user):
        return HttpResponseForbidden()
    
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
