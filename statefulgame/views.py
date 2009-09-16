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

# return list of files team has seen
def get_files(request):
  team = Team.objects.by_user(request.user, getattr(request,"course",None))

  world_state = team.state.world_ro
  if world_state.has_key('documents'):
    if request.GET.has_key("jsonp"):
      return HttpResponse("%s(%s)" % (request.GET["jsonp"], json.dumps(world_state['documents'])))
    return HttpResponse(json.dumps(world_state['documents']), mimetype="application/javascript")
  return HttpResponse("")
  

def assignment_page(request,assignment_id,page_id=None):
  assignment = get_object_or_404(Assignment,pk=assignment_id,game__course=getattr(request,"course",None))
  #team = Team.objects.by_user(request.user, getattr(request,"course",None))
  return game(request,assignment,page_id=page_id,first_time=False)

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

def get_assignment_data(request,turn_id):
  user = request.user
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
  
  # TODO: "wait" page if current turn pending
  if turn is None:
    pass

  return HttpResponseRedirect(reverse("assignment-page", args=[turn.assignment.id]))


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
  if not teams:
    teams = [Team.objects.by_user(request.user, getattr(request,'course',None))]
  assignments = [{'data':a,'teams':[]} for a in Assignment.objects.filter(game__course=request.course)]
  for t in teams:
    for d in assignments:
      turn = None      
      try:
        turn = Turn.objects.get(assignment=d['data'],team=t)
      except:
        pass
      d['teams'].append(turn)
  return {'teams':teams,
          'assignments':assignments,
          }
  
