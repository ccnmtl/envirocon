from django.db import models

# Create your models here.
from game.installed_games import InstalledGames,GameInterface

class ObtainAdditionalInformation(GameInterface):
    def pages(self):
        return ('index',)

    def template(self,page_id=None):
        game_context = {'sampledata':"hello"}
        return ('obtain_additional_information/index.html',game_context)
    
    def variables(self,page_id=None):
        return []

InstalledGames.register_game('obtain_additional_information',
                             'Obtain Additional Information',
                             ObtainAdditionalInformation() )
