from django.db import models

# Create your models here.
from game.installed_games import InstalledGames,GameInterface

class ExplainYourReportSelection(GameInterface):
    def pages(self):
        return ('index',)

    def template(self,page_id=None,public_state=None):
        game_context = {'sampledata':"hello"}
        return ('game_many/explain_your_report_selection.html',game_context)
    
    def variables(self,page_id=None):
        return ['explain_your_report_selection']

InstalledGames.register_game('explain_your_report_selection',
                             'Explain Your Report Selection',
                             ExplainYourReportSelection() )


class RecommendingInterventions(GameInterface):
    def pages(self):
        return ('index',)

    def template(self,page_id=None):
        game_context = {'sampledata':"hello"}
        return ('game_many/recommending_interventions.html',game_context)
    
    def variables(self,page_id=None):
        return ['recommending_interventions']

InstalledGames.register_game('recommending_interventions',
                             'Recommending Interventions',
                             RecommendingInterventions() )
