from django.db import models

# Create your models here.
from game.installed_games import InstalledGames,GameInterface

class ConflictAssessment(GameInterface):
    def pages(self):
        return ('index',)

    def template(self,page_id=None):
        game_context = {'sampledata':"hello"}
        if page_id == "country_narrative":
          return ('conflict_assessment/narrative.html',game_context)
        return ('conflict_assessment/index.html',game_context)
    
    def variables(self,page_id=None):
        return ['conflict_assessment']

InstalledGames.register_game('conflict_assessment',
                             'Conflict Assessment',
                             ConflictAssessment() )
