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
  #so we auto-close only once
  auto_closed = models.BooleanField(default=False)

  #open means Teams are allowed to advance to this assignment
  #only one assignment is editable by a team at a particular moment (see turn.open)
  open = models.BooleanField(default=False)
  name = models.CharField(max_length=100)
  individual = models.BooleanField()  # True = individual assignment; False = group assignment
  # app (inherited from Activity)

  def __unicode__(self):
    return "%s (due %s)" % (self.name, self.close_date)
    
  class Meta:
    order_with_respect_to = 'game'

  def submission(self,team,user=None,allUsers=False):
    if not self.individual or allUsers:
      return Submission.objects.filter(turn__assignment=self,turn__team=team)
    elif user:
      return Submission.objects.filter(turn__assignment=self,turn__team=team,author=user)
    else:
      return None

  def any_submission(self):
    subs = Submission.objects.filter(turn__assignment=self)[:1]
    return (subs and subs[0] or None)
    
  def turn(self,team):
    turn = Turn.objects.get(team=team,assignment=self)
    return turn

  def auto_close(self):
    if self.open and not self.auto_closed and self.close_date < datetime.datetime.now():
      self.open = False
      self.auto_closed = True
      self.save()
      return True

# abstract
class Shock(models.Model):
  name = models.CharField(max_length=100)
  outcome = models.TextField()
  
  def __unicode__(self):
    return "%d: %s" %(self.id,self.name)

class TurnManager(models.Manager):
  #auto-create Turn on get() for access from ????
  def get(self,*args,**kwargs):
    try:
      return super(TurnManager, self).get(*args,**kwargs)
    except Turn.DoesNotExist:
      if kwargs.has_key('team') and kwargs.has_key('assignment'):
        return Turn.objects.create(team=kwargs['team'],
                                   assignment=kwargs['assignment'])
      else:
        raise #re-raise it

# breadcrumb - formerly ActivityTeamNode
class Turn(models.Model):
  objects = TurnManager() #manager
  
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
  def visible(self):
    return (self.assignment.id in self.team.state.visible_assignments())

  @property
  def open(self):
    """When a turn is open, the team can edit their submission
    only one (at most) turn can be open for a particular team, at once.
    """
    #TODO: if self.team.state.turn is earlier than self
    #      are we open, or do they have to finish the first part?
    return (self==self.team.state.turn and self.assignment.open)

  @property
  def complete(self):
    subs = [s.author.id for s in Submission.objects.filter(turn=self,published=True)]
    if not subs:
      return False
    if self.assignment.individual:
      for m in self.team.group.user_set.all():
        if m.id not in subs:
          return False
    return True

  def next(self):
    try:
      next_a = self.assignment.get_next_in_order()
      return next_a.turn(self.team)
    except Assignment.DoesNotExist:
      return None
      

class StateManager(models.Manager):
  #auto-create State on get() for access from team.state
  def get(self,*args,**kwargs):
    try:
      return super(StateManager, self).get(*args,**kwargs)
    except State.DoesNotExist:
      if kwargs.has_key('team__pk'):
        team = Team.objects.get(pk=kwargs['team__pk'])
        state = State(team=team,game=Game.objects.filter(course=team.course)[0])
        state.save()
        return state
      else:
        raise #re-raise it
  
class State(models.Model):
  objects = StateManager() #manager
  
  game = models.ForeignKey(Game)
  team = models.OneToOneField(Team)  # singleton per team
  turn = models.ForeignKey(Turn, null=True, blank=True)
  world_state = models.TextField(blank=True)  # state data

  def __unicode__(self):
    return u'State of '+unicode(self.team)

  @property
  def assignment(self):
    return self.turn.assignment
  
  @property
  def world_ro(self):
    try:
      return json.loads(self.world_state)
    except:
      return {}

  def world_slice(self,vars=None):
    try:
      world = json.loads(self.world_state)
      return dict([(k,v) for k,v in world.setdefault('app_vars',{}).items()
                   if vars is None or k in vars])
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

  def advance_turn(self):
    if self.turn is None:
      next_a = self.game.assignment_set.all()[0]
      if not getattr(next_a,'open',False):
        return False
    else:
      next_t = self.turn.next()
      if not next_t or not next_t.assignment.open or not self.turn.complete:
        return False
      next_a = next_t.assignment
    self.turn =  next_a.turn(self.team)
    self.save()
    return self.turn

  def current_turn(self):
    return self.advance_turn() or self.turn

  def visible_assignments(self):
    order = self.game.get_assignment_order()
    if self.turn:
      max_turn = order.index(self.turn.assignment.id)
      if self.turn.assignment.open:
        return order[0:max_turn+1] #include current
      else:
        return order[0:max_turn] #all previous

    return []
      

  def activity_resources(self,activity,turn,sub,world_state):
    onclosed = False
    if self.turn:
      order = self.game.get_assignment_order()
      turn_ind = order.index(turn.assignment.id)
      ahead_by = order.index(self.turn.assignment.id) - turn_ind
      if ahead_by > 1:
        onclosed = True
      elif ahead_by == 1:
        # note: last game can never have an
        # exposed onclosed resource.
        next_turn = self.turn.next()
        if next_turn:
          onclosed = next_turn.open
    return activity.gameresources(world_state,
                                  onopen=(turn.assignment.id in self.visible_assignments()),
                                  onclosed=onclosed
                                  ) or []

  def resource_access(self,activity,page_id,user=None):
    if not page_id or page_id in activity.gamepages():
      return True #public page
    turn = activity.turn(self.team)    
    sub = activity.submission(self.team, user)
    res = self.activity_resources(activity,turn,sub,self.world_slice())
    for d in res:
      if page_id==d.get('page_id',None):
        return True
    return False

  def resources(self,user=None):
    "The resources from each game that the team has access to"
    res = []
    if self.turn:
      game = self.turn.assignment.game
      world_state = self.world_slice()
      for a in game.assignment_set.all():
        turn = a.turn(self.team)
        sub = a.submission(self.team, user)
        res.append({'a':a,
                    'res':self.activity_resources(a,turn,sub,world_state),
                    })
    return res
      
# breadcrumb
class Submission(models.Model):
  author = models.ForeignKey(User)
  turn = models.ForeignKey(Turn) #not 1-1 when individual assignments
  published = models.BooleanField(default=False)
  data = models.TextField()  # submitted data
  modified = models.DateTimeField('date modified', auto_now=True,editable=False)

  archival = models.BooleanField(default=False)

#SIGNAL SUPPORT
def create_state_for_team(sender, instance, created, **kwargs):
  #possibly redundant to the StateManager auto-create workflow as well
  if isinstance(instance,Team) and created:
    State.objects.create(team=instance,game=Game.objects.filter(course=instance.course)[0]) # turn=null to begin with

post_save.connect(create_state_for_team, sender=Team)

def include_world_state(sender,request, **kwargs):
  #DEPRECATED: see statefulgame/views now
  if not isinstance(sender, Assignment):
    return { 'turn_id':1,
             'user_id':1,#hope there's a user.id==1!
             'editable':1,
             } #TEMPORARY
  else:
    return {} 
  raise Exception("Activity does not match assignment for this turn.")
  
game_signals.world_state.connect(include_world_state)

