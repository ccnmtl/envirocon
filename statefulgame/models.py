from django.db import models
from django.db.models.signals import post_save
from game.models import Activity
from game import signals as game_signals
import datetime

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

  @property
  def published(self):
    try:
      return self.submission.published
    except:
      return False

  @property
  def open(self):
    return (self==team.state.turn or self.assignment.open)
  
class State(models.Model):
  team = models.OneToOneField(Team)  # singleton per team
  #assignment = models.ForeignKey(Assignment)
  turn = models.ForeignKey(Turn, null=True, blank=True)
  world_state = models.TextField(blank=True)  # state data
  
  @property
  def assignment(self):
    return self.turn.assignment
   
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
      #any old turn can do
      return turn


# breadcrumb
class Submission(models.Model):
  author = models.ForeignKey(User)
  turn = models.OneToOneField(Turn)
  published = models.BooleanField()
  data = models.TextField()  # submitted data



#SIGNAL SUPPORT
def create_state_for_team(sender, instance, created, **kwargs):
  if isinstance(instance,Team) and created:
    State.objects.create(team=instance) # turn=null to begin with

post_save.connect(create_state_for_team, sender=Team)

def include_world_state(sender, context,request, **kwargs):
  activity = sender
  user = request.user
  team = Team.objects.by_user(user, getattr(request,"course",None))
  if isinstance(activity, Assignment):
    turn = team.state.current_turn(assignment=activity)
    return { 'duedate':turn.assignment.close_date,
             'individual':turn.assignment.individual,
             'turn_id':turn.id,
             'published':turn.published
           }
  else:
    # TODO: if you go to the activity page directly but it is
    # also your current assignment, it should pull that assign. data
    # TODO: if assignment exists, old assignment so use that
    # (not editable)
    #assignment = Assignment.objects.get(app=activity)
    #turn = Turn.objects.get(team=team, assignment=assignment)
    # if assignment does not exist, just show the activity
    # for now (though actually we should disallow)
    return { 'turn_id':None }
  #elif team.state.assignment.app == activity.app:
  #else: turn = team.state.turn
  #else:
  #  raise "Activity does not match assignment for this turn."
game_signals.world_state.connect(include_world_state)

