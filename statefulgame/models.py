from django.db import models
from game.models import Activity
#from teams.models import Team
Course = models.get_model('courseaffils','course')
User = models.get_model('auth','user')

from game import signals as game_signals
import datetime


class Game(models.Model):
  def __unicode__(self):
    return self.course.title
  course = models.ForeignKey(Course)

# instance of an Activity for a specific class (has due date, etc.)
class Assignment(Activity):
  game = models.ForeignKey(Game)
  close_date = models.DateTimeField()
  open = models.BooleanField()
  name = models.CharField(max_length=100)
  individual = models.BooleanField()  # True = individual assignment; False = group assignment
  # app (inherited from Activity)

  def __unicode__(self):
    return self.name


# abstract
class Shock(models.Model):
  name = models.CharField(max_length=100)
  outcome = models.TextField()
  
  def __unicode__(self):
    return self.name

# breadcrumb - formerly ActivityTeamNode
class Turn(models.Model):
  #team = models.ForeignKey(Team)
  assignment = models.ForeignKey(Assignment)
  shock = models.ForeignKey(Shock, null=True)
  
# singleton per team
class State(models.Model):
  #team = models.ForeignKey(Team)
  assignment = models.ForeignKey(Assignment)
  turn = models.ForeignKey(Turn)
  data = models.TextField()  # state data

# breadcrumb
class Submission(models.Model):
  author = models.ForeignKey(User)
  turn = models.ForeignKey(Turn)
  published = models.BooleanField()
  data = models.TextField()  # submitted data



#SIGNAL SUPPORT
def include_world_state(sender, context,request, **kwargs):
    return { 'duedate':datetime.datetime.today(), # assignment.close_date
             'individual':1,  # assignment.individual
             'turn_id':1}  # TODO real turn ID
game_signals.world_state.connect(include_world_state)

