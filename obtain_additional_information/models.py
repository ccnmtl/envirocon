from django.db import models

# Create your models here.
from game.installed_games import InstalledGames,GameInterface

class ObtainAdditionalInformation(GameInterface):
    def pages(self):
        return ('index',)

    def template(self,page_id=None,public_state=None):
        game_context = {'sampledata':"hello"}
        return ('obtain_additional_information/index.html',game_context)
    
    def variables(self,page_id=None):
        return ['additional_information']

    def public_variables(self):
        return ['additional_information']

InstalledGames.register_game('obtain_additional_information',
                             'Obtain Additional Information',
                             ObtainAdditionalInformation() )
