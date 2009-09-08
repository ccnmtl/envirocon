from statefulgame.models import Submission, Turn, Assignment
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db import models
import simplejson as json

from game.views import game
Team = models.get_model('teams','team')

def assignment_page(request,assignment_id):
  assignment = get_object_or_404(Assignment,pk=assignment_id,game__course=getattr(request,"course",None))
  #team = Team.objects.by_user(request.user, getattr(request,"course",None))
  return game(request,assignment)

# saves an assignment blob to the database
def save_assignment(request):
  data = request.POST.get('data',None)
  turn_id = request.POST['turn_id']
  turn = Turn.objects.get(id=turn_id)
  created = True
  if turn.assignment.individual:
    submission,created = Submission.objects.get_or_create(author=request.user,turn=turn)
  else:
    try:
      submission = Submission.objects.get(turn=turn)
      created=False
    except Submission.DoesNotExist:
      submission = Submission(turn=turn,author=request.user)
  submission.data = data
  submission.published = ( request.POST.get('published','Draft').find('Draft') < 0 )
  submission.save()
  return HttpResponse(created)

def get_assignment_data(request,turn_id):
  user = request.user
  team = Team.objects.by_user(user, getattr(request,"course",None))
  turn = Turn.objects.get(pk=turn_id,team=team)
  if turn.assignment.individual:
    submission = get_object_or_404(Submission, author=user,turn=turn)
  else:
    submission = get_object_or_404(Submission, turn=turn)
  if request.GET.has_key("jsonp"):
    return HttpResponse("%s(%s)" % (request.GET["jsonp"], submission.data))
  return HttpResponse(submission.data)
  
def current_turn(request):
  user = request.user
  team = Team.objects.by_user(user, getattr(request,"course",None))
  turn = team.state.turn
  
  # TODO: "wait" page if current turn pending
  
  # TODO: url lookup
  return HttpResponseRedirect("/assignment/%s" % turn.assignment.id)
