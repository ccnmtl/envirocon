from statefulgame.models import *
from statefulgame.forms import BasicAssignmentForm

from django.http import HttpResponse,Http404,HttpResponseRedirect,HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.db import models
from django.core.urlresolvers import reverse

from django.forms.models import inlineformset_factory

import simplejson as json

from game.views import game
Team = models.get_model('teams','team')

def assignment_page(request,assignment_id,faculty_view=None,user_id=None,page_id=None):
  assignment = get_object_or_404(Assignment,pk=assignment_id,game__course=getattr(request,"course",None))
  #we can assume request.course from now on
  user = request.user
  faculty_info = None
  if faculty_view and request.course.is_faculty(request.user):
    user = User.objects.get(pk=user_id)
    faculty_info={'teams':[{'r':team,}
                           for team in request.course.team_set.all()],
                  'shocks':Shock.objects.all(),
                  #'next_assignment':assignment.get_next_in_order(),
                  }
    if not page_id and 'page2' in assignment.gamepages():
      page_id = 'page2'
    
  team = Team.objects.by_user(user, getattr(request,"course",None))
  if team is None:
    raise Http404

  if not team.state.resource_access(assignment,page_id,user):
    return HttpResponseForbidden('You do not have access to this activity resource at this time.')
  turn = assignment.turn(team)
  if turn:
    world = team.state.world_slice(assignment.gamepublic_variables())
    resources = team.state.resources(user)
    resources_by_app = {}
    for act_meta in resources:
      app_dict = resources_by_app.setdefault(act_meta['a'].app,OrderedDict())
      for r in act_meta['res']:
        app_dict[ r['page_id'] ] =  r
  editable = turn.open and not faculty_info
  world_state = { 'duedate':turn.assignment.close_date,
                  'individual':turn.assignment.individual,
                  'turn_id':turn.id,
                  'published':turn.published(user),
                  'editable':editable,
                  'faculty_info':faculty_info,
                  'resources':resources,
                  'resources_by_app':resources_by_app,
                  'team':team,
                  'assignment':assignment,
                  'turn':turn,
                  'user_id':user.id,
                  'submission':assignment.submission(team,user)
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
  data = request.REQUEST.get('data',None)
  turn_id = request.REQUEST['turn_id']
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
  submission.published = (request.REQUEST.get('published','Draft').find('Draft') < 0 )
  submission.save()

  

  return HttpResponse(created)

def get_assignment_data(request,turn_id,user_id):
  user = request.user
  if user_id and request.course.is_faculty(request.user):
    user = User.objects.get(pk=user_id)

  team = Team.objects.by_user(user, getattr(request,"course",None))

  turn = get_object_or_404(Turn,pk=turn_id,team=team)
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
  


def team_view_data(request,teams=None,game=None):
  """
  past assignments (with title,status,shock)
  
  """
  is_faculty = (request.user in request.course.faculty)
  assignment_forms = None
  team = None
  AssignmentFormSet = inlineformset_factory(Game, Assignment,
                                            can_delete=False,
                                            form=BasicAssignmentForm,
                                            extra=0,
                                            )

  if game is None:
    game = request.course.game_set.all()[0]
    
  team = Team.objects.by_user(request.user, getattr(request,'course',None))
  if is_faculty:
    teams =Team.objects.filter(course=getattr(request,'course',None))
    if request.method == 'POST':
      post_forms = AssignmentFormSet(request.POST, request.FILES, instance=game)
      if post_forms.is_valid():
        post_forms.save()
  else:
    teams = [team]


  assignment_forms = AssignmentFormSet(instance=game)

  assignments = [{'data':f.instance,'form':f,
                  'teams':[],'hidden':False,'current':False,}
                 for f in assignment_forms.forms]
  for t in teams:
    for d in assignments:
      turn = d['data'].turn(t)
      if not (turn.open or turn.complete):
        d['hidden'] = True
      elif t==team and turn == t.state.turn:
        d['current'] = True
      d['teams'].append({'turn':turn,
                         'data':t,
                         'sub':d['data'].submission(t, request.user, is_faculty)
                         })
  return {'teams':teams,
          'assignments':assignments,
          'is_faculty':is_faculty,
          'formset':assignment_forms,
          'team':team,#user's team (implies a student)
          }
  
def set_shock(request):
  """team_id,assignment_id,shock_id
  OR team_id,assignment_id,shock_name,shock_outcome
  """
  if request.method=='POST' and request.course.is_faculty(request.user):
    team = get_object_or_404(Team,pk=request.POST['team_id'],course=request.course)
    assignment = get_object_or_404(Assignment,pk=request.POST['assignment_id'],
                                   game__course=request.course)
    turn = assignment.turn(team)
    if request.POST.get('shock_id',False):
      if request.POST['shock_id']=='none':
        shock = None
      else:
        shock = get_object_or_404(Shock,pk=request.POST['shock_id'])
    else:
      shock = Shock.objects.create(name=request.POST['shock_name'],outcome=request.POST['shock_outcome'])
    turn.shock = shock
    turn.save()
    return HttpResponse(shock)
    


class OrderedDict:
  #mostly
  dic = {}
  array = []
  def __get__(self,key):
    return self.dic[key]

  def __setitem__(self,key,val):
    if key in self.dic:
      self.dic[key] = val
    else:
      self.array.append(key)
      self.dic[key] = val

  def values(self):
    return [self.dic[k] for k in self.array]

  def items(self):
    return [(k,self.dic[k]) for k in self.array]
    
