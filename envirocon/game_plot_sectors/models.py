from django.db import models

# Create your models here.
from envirocon.game.installed_games import InstalledGames, GameInterface


class PlotSectorsGame(GameInterface):

    def pages(self):
        return ('index', 'page2',)

    def template(self, page_id=None, public_state=None):
        game_context = {'sampledata': "hello"}
        if page_id == "page2":
            return ('game_plot_sectors/index.html', game_context)
        return ('game_plot_sectors/intro.html', game_context)

    def variables(self, page_id=None):
        return ['game_plot_sectors']

InstalledGames.register_game('plot_sectors',
                             'Plot Sectors',
                             PlotSectorsGame())
