from django.db import models
import datetime

# Create your models here.
from game.installed_games import InstalledGames,GameInterface

class Turn1(GameInterface):
    def pages(self):
        return ('index',)

    def template(self,page_id=None):
        game_context = {'sampledata':"hello", 'duedate':datetime.datetime.today()}
        return ('turn1/index.html',game_context)
    
    def variables(self,page_id=None):
        return []

InstalledGames.register_game('turn1',
                             'Turn 1',
                             Turn1() )
