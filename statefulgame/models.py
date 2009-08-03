from django.db import models
from game.models import Activity
from teams.models import Team

class Game(models.Model):
  #course = models.ForeignKey(Course)
  pass

# instance of an Activity for a specific class (has due date, etc.)
class Assignment(Activity):
  game = models.ForeignKey(Game)
  close_date = models.DateTimeField()
  open = models.BooleanField()
  name = models.CharField(max_length=100)
  # app (inherited from Activity)

# abstract
class Shock(models.Model):
  name = models.CharField(max_length=100)
  outcome = models.TextField()
  
  def __unicode__(self):
    return name

# breadcrumb - formerly ActivityTeamNode
class Turn(models.Model):
  team = models.ForeignKey(Team)
  assignment = models.ForeignKey(Assignment)
  shock = models.ForeignKey(Shock, null=True)
  
# singleton per team
class State(models.Model):
  team = models.ForeignKey(Team)
  assignment = models.ForeignKey(Assignment)
  turn = models.ForeignKey(Turn)
  data = models.TextField()  # state data

# breadcrumb
class Submission(models.Model):
  turn = models.ForeignKey(Turn)
  published = models.BooleanField()
  data = models.TextField()  # submitted data