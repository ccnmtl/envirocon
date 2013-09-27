from django.db import models

# Create your models here.
from envirocon.game.installed_games import InstalledGames, GameInterface


class Week1(GameInterface):

    def pages(self):
        return ('index',)

    def template(self, page_id=None, public_state=None):
        game_context = {'sampledata': "hello"}
        return ('week1/index.html', game_context)

    def variables(self, page_id=None):
        return []

InstalledGames.register_game('week1',
                             'Week 1',
                             Week1())
