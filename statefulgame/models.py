from django.db import models
from django.db.models.signals import post_save
from game.models import Activity
from game import signals as game_signals
import datetime
import simplejson as json

Team = models.get_model('teams','team')
Course = models.get_model('courseaffils','course')
User = models.get_model('auth','user')



class Game(models.Model):
  def __unicode__(self):
    return self.course.title
  course = models.ForeignKey(Course)

# instance of an Activity for a specific class (has due date, etc.)
class Assignment(Activity):
  game = models.ForeignKey(Game)
  close_date = models.DateTimeField()
  open = models.BooleanField(default=False)
  name = models.CharField(max_length=100)
  individual = models.BooleanField()  # True = individual assignment; False = group assignment
  # app (inherited from Activity)

  def __unicode__(self):
    return "%s (due %s)" % (self.name, self.close_date)
    
  class Meta:
    order_with_respect_to = 'game'

  def save(self,*args,**kwargs):
    super(Assignment,self).save(*args,**kwargs)
    for team in self.game.course.team_set.all():
      Turn.objects.get_or_create(team=team,assignment=self)

  def submission(self,team,user=None):
    if not self.individual:
      return Submission.objects.filter(turn__team=team)
    elif user:
      return Submission.objects.filter(turn__team=team,author=user)
    else:
      return None
    
  def turn(self,team):
    turn,created = Turn.objects.get_or_create(team=team,assignment=self)
    return turn

# abstract
class Shock(models.Model):
  name = models.CharField(max_length=100)
  outcome = models.TextField()
  
  def __unicode__(self):
    return self.name

# breadcrumb - formerly ActivityTeamNode
class Turn(models.Model):
  team = models.ForeignKey(Team)
  assignment = models.ForeignKey(Assignment)
  shock = models.ForeignKey(Shock, null=True, blank=True)
  
  def __unicode__(self):
    return "Turn ID %s for Team %s (%s)" % (self.id, self.team, self.assignment)

  def published(self,user=None):
    sub = self.assignment.submission(self.team,user)
    if sub:
      return sub[0].published
    else:
      return False

  @property
  def open(self):
    "When a turn is open, the team can edit their submission"
    #TODO: if self.team.state.turn is earlier than self
    #      are we open, or do they have to finish the first part?
    return (self==self.team.state.turn or self.assignment.open)
  
class State(models.Model):
  #game = models.ForeignKey(Game)
  team = models.OneToOneField(Team)  # singleton per team
  turn = models.ForeignKey(Turn, null=True, blank=True)
  world_state = models.TextField(blank=True)  # state data
  
  @property
  def assignment(self):
    return self.turn.assignment
  
  @property
  def world_ro(self):
    try:
      return json.loads(team.state.world_state)
    except:
      return {}

  def world_slice(self,vars):
    try:
      world = json.loads(team.state.world_state)
      return dict([(k,v) for k,v in world.setdefault('app_vars',{}).items() if k in vars])
    except:
      return {}

  def save_world(self,world):
    """OK, saving is a bit dump here, but--I really wanted this method name :-)"""
    self.world_state = json.dumps(world)
    self.save()

  def save(self,*args,**kwargs):
    if self.turn:
      assert(self.turn.team == self.team)
    return super(State,self).save(*args,**kwargs)

  def current_turn(self,assignment=None):
    if assignment:
      if assignment.open:
        return Turn.objects.get_or_create(team=self.team,assignment=assignment)[0]
      else:
        return None
    elif self.turn:
      return self.turn
    else:
      turn = None
      for assn in Assignment.objects.filter(game__course=self.team.course,
                                            open=True):
        turn,created = Turn.objects.get_or_create(team=self.team,assignment=assn)
        if created:
          return turn
      #last open turn: since any could do
      return turn

  def resources(self,user=None):
    "The resources from each game that the team has access to"
    res = []
    if self.turn:
      game = self.turn.assignment.game
      for a in game.assignment_set.all():
        turn = a.turn(self.team)
        sub = a.submission(self.team, user)
        data = (sub and sub[0].data or None)
        res.extend(a.gameresources(data,#not de-jsoned
                                   onopen=(turn.open or data),
                                   onclosed=(not turn.open and data)
                                   ))
    return res
      
# breadcrumb
class Submission(models.Model):
  author = models.ForeignKey(User)
  turn = models.ForeignKey(Turn) #not 1-1 when individual assignments
  published = models.BooleanField()
  data = models.TextField()  # submitted data



#SIGNAL SUPPORT
def create_state_for_team(sender, instance, created, **kwargs):
  if isinstance(instance,Team) and created:
    State.objects.create(team=instance) # turn=null to begin with

post_save.connect(create_state_for_team, sender=Team)

def include_world_state(sender,request, **kwargs):
  activity = sender
  user = request.user
  team = Team.objects.by_user(user, getattr(request,"course",None))
  if isinstance(activity, Assignment):
    turn = team.state.current_turn(assignment=activity)
    if turn:
      world = team.state.world_slice(activity.gamepublic_variables())
      world.update({ 'duedate':turn.assignment.close_date,
                     'individual':turn.assignment.individual,
                     'turn_id':turn.id,
                     'published':turn.published(user)
                     })
      return world
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
  #return { 'turn_id':None }
  raise Exception("Activity does not match assignment for this turn.")
  
game_signals.world_state.connect(include_world_state)

