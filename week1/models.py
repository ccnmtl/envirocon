from django.db import models
import datetime

# Create your models here.
from game.installed_games import InstalledGames,GameInterface

class Week1(GameInterface):
    def pages(self):
        return ('index',)

    def template(self,page_id=None):
        game_context = {'sampledata':"hello", 'duedate':datetime.datetime.today(),
                        'turn_id':1}  # TODO real due date, real turn ID
        return ('week1/index.html',game_context)
    
    def variables(self,page_id=None):
        return []

InstalledGames.register_game('week1',
                             'Week 1',
                             Week1() )
