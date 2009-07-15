from django.db import models
from game.installed_games import InstalledGames

class Activity(models.Model):
    """Something which has a game
    """
    game = models.CharField(max_length=64, choices=InstalledGames, blank=True,null=True)

    page_id = None #blessed by view with name of the page
    
    #GAME code, we LOVE delegation!
    def gamepages(self):
        if self.game:
            return InstalledGames.pages(self.game)
        else:
            return tuple()

    def gamevariables(self,page_id=None):
        if self.game:
            return InstalledGames.variables(self.game,page_id) or []
        return []

    def gametemplate(self, page_id=None):
        return InstalledGames.template(self.game,page_id)
