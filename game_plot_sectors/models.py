from django.db import models

# Create your models here.
from game.installed_games import InstalledGames,GameInterface

class PlotSectorsGame(GameInterface):
    def pages(self):
        return ('index',)

    def template(self,page_id=None):
        game_context = {'sampledata':"hello"}
        return ('game_plot_sectors/index.html',game_context)
    
    def variables(self,page_id=None):
        return []

InstalledGames.register_game('plot_sectors',
                             'Plot Sectors',
                             PlotSectorsGame() )
