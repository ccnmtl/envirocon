from django.db import models

# Create your models here.
from game.installed_games import InstalledGames,GameInterface

class ExplainYourReportSelection(GameInterface):
    def pages(self):
        return ('index',)

    def template(self,page_id=None):
        game_context = {'sampledata':"hello"}
        return ('explain_your_report_selection/index.html',game_context)
    
    def variables(self,page_id=None):
        return []

InstalledGames.register_game('explain_your_report_selection',
                             'Explain Your Report Selection',
                             ExplainYourReportSelection() )
