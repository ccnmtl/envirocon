from statefulgame.models import *
from django.http import HttpResponse,Http404,HttpResponseRedirect,HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.db import models
from django.core.urlresolvers import reverse

from django.forms.models import modelformset_factory,inlineformset_factory

import simplejson as json

from game.views import game
Team = models.get_model('teams','team')

def assignment_page(request,assignment_id,faculty_view=None,user_id=None,page_id=None):
  assignment = get_object_or_404(Assignment,pk=assignment_id,game__course=getattr(request,"course",None))
  #we can assume request.course from now on
  user = request.user
  is_faculty = False
  if faculty_view and request.course.is_faculty(request.user):
    user = User.objects.get(pk=user_id)
    is_faculty=True
  team = Team.objects.by_user(user, getattr(request,"course",None))

  if not team.state.resource_access(assignment,page_id,user):
    return HttpResponseForbidden('You do not have access to this activity resource at this time.')

  turn = assignment.turn(team)
  if turn:
    world = team.state.world_slice(assignment.gamepublic_variables())
    resources = team.state.resources(user)
    resources_by_type = {}
    for act_meta in resources:
      for r in act_meta['res']:
        t_bin = resources_by_type.setdefault(r.get('type','None'),[])
        t_bin.append({'a':act_meta['a'],'res':r})
  editable = turn.open and not is_faculty
  world_state = { 'duedate':turn.assignment.close_date,
                  'individual':turn.assignment.individual,
                  'turn_id':turn.id,
                  'published':turn.published(user),
                  'editable':editable,
                  'is_faculty':is_faculty,
                  'resources':resources,
                  'res_by_type':resources_by_type,
                  'team':team,
                  'user_id':user.id,
                  }
  # TODO: if you go to the activity page directly but it is
  # also your current assignment, it should pull that assign. data
  # TODO: if assignment exists, old assignment so use that
  # (not editable)
  #assignment = Assignment.objects.get(app=activity)
  #turn = Turn.objects.get(team=team, assignment=assignment)
  # if assignment does not exist, just show the activity
  # for now (though actually we should disallow)
  #elif team.state.assignment.app == activity.app:
  #else: turn = team.state.turn
  
  return game(request,assignment,page_id=page_id,
              extra_world_state=world_state)

# saves an assignment blob to the database
def save_assignment(request):
  data = getattr(request,request.method).get('data',None)
  turn_id = getattr(request,request.method)['turn_id']
  turn = Turn.objects.get(id=turn_id)
  if not turn.open:
    return HttpResponseForbidden()
  if turn.assignment.individual:
    submission,created = Submission.objects.get_or_create(author=request.user,turn=turn)
  else:
    try:
      submission = Submission.objects.get(turn=turn)
      created=False
    except Submission.DoesNotExist:
      submission = Submission(turn=turn,author=request.user)
      created = True
    #save global state if we have public vars
    state = turn.team.state
    pubs = turn.assignment.gamepublic_variables()
    world = state.world_ro
    dirty = False
    for k,v in json.loads(data).items():
      if k in pubs:
        world.setdefault('app_vars',{})
        world['app_vars'][k] = v
        dirty = True
    if dirty:
      state.save_world(world)
  submission.data = data
  submission.published = (getattr(request,request.method).get('published','Draft').find('Draft') < 0 )
  submission.save()

  

  return HttpResponse(created)

def get_assignment_data(request,turn_id,user_id):
  user = request.user
  if user_id and request.course.is_faculty(request.user):
    user = User.objects.get(pk=user_id)

  team = Team.objects.by_user(user, getattr(request,"course",None))
  turn = Turn.objects.get(pk=turn_id,team=team)
  data = team.state.world_slice(turn.assignment.gamepublic_variables())
  try:
    if turn.assignment.individual:
      submission = Submission.objects.get(author=user,turn=turn)
    else:
      submission = Submission.objects.get(turn=turn)
    data.update(json.loads(submission.data))
  except Submission.DoesNotExist:
    pass
  serialized_data = json.dumps(data)
  if request.GET.has_key("jsonp"):
    return HttpResponse("%s(%s)" % (request.GET["jsonp"], serialized_data))
  return HttpResponse(serialized_data)
  
def current_turn(request):
  user = request.user
  team = Team.objects.by_user(user, getattr(request,"course",None))
  turn = team.state.current_turn()
  
  if turn:
    return HttpResponseRedirect(reverse("assignment-page", args=[turn.assignment.id]))
  else:
    return HttpResponseRedirect('/?message=no+activity+ready')


def faculty_view(request, game_id=None):
  """
  list assignments (change due dates/ open|close)
  see teams:
    set turn (manually) per-team
       AND globally (through assignments list above)
        
  """
  if request.user not in request.course.faculty \
         and not request.user.is_staff:
    return HttpResponseForbidden()

  game = None
  if game_id:
    game = get_object_or_404(Game, pk=game_id, course=request.course)
  else:
    game = Game.objects.filter(course=request.course)[0]

  if request.method == 'POST':
    pass

  return render_to_response('statefulgame/faculty_view.html',
                            {'course':request.course,
                             'game':game,
                             },
                            context_instance=RequestContext(request))


def faculty_assignment_review(request):
  """
  view assignments
  
  """
  data = {}
  if request.user.is_staff or request.user in request.course.faculty:
    data['assignments'] = Assignment.objects.filter(game__course=request.course)
  return render_to_response('statefulgame/faculty_view.html',
                            {'course':request.course,
                             'game':game,
                             },
                            context_instance=RequestContext(request))
  


def team_view_data(request,teams=None):
  """
  past assignments (with title,status,shock)
  
  """
  is_faculty = (request.user in request.course.faculty)
  if is_faculty:
    teams =Team.objects.filter(course=getattr(request,'course',None))
  else:
    teams = [Team.objects.by_user(request.user, getattr(request,'course',None))]

  assignments = [{'data':a,'teams':[],'hidden':False,'current':False}
                 for a in Assignment.objects.filter(game__course=request.course)]
  for t in teams:
    for d in assignments:
      turn = None      
      try:
        turn = Turn.objects.get(assignment=d['data'],team=t)
        if not (turn.open or turn.complete):
          d['hidden'] = True
        elif turn == t.state.turn:
          d['current'] = True
      except:
        pass
      d['teams'].append(turn)
  return {'teams':teams,
          'assignments':assignments,
          'is_faculty':is_faculty,
          }
  
