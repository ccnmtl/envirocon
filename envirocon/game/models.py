from django.db import models
from envirocon.game.installed_games import InstalledGames


class Activity(models.Model):

    """Something which has a game
    """
    app = models.CharField(
        max_length=64, choices=InstalledGames, blank=True, null=True)

    page_id = None  # blessed by view with name of the page

    # GAME code, we LOVE delegation!
    @classmethod
    def gamechoices(c):
        return InstalledGames.GAME_NAMES

    def gamename(self):
        return InstalledGames.viewname(self.app)

    def gamepages(self):
        if self.app:
            return InstalledGames.pages(self.app)
        else:
            return tuple()

    def gamevariables(self, page_id=None):
        if self.app:
            return InstalledGames.variables(self.app, page_id) or []
        return []

    def gamepublic_variables(self):
        if self.app:
            return InstalledGames.public_variables(self.app) or []
        return []

    def gametemplate(self, page_id=None, public_state=None):
        return InstalledGames.template(self.app, page_id, public_state)

    def gameresources(self, game_state, onopen=False, onclosed=False):
        return InstalledGames.resources(self.app, game_state, onopen=onopen, onclosed=onclosed)

    def gamevideo(self):
        try:
            return ActivityVideo.objects.get(app=self.app)
        except:
            # Not all activities have videos
            return None

    def gameconsequences(self, game_state):
        return InstalledGames.consequences(self.app, game_state)

    def game_autoshock(self, game_state):
        return InstalledGames.autoshock(self.app, game_state)


class ActivityVideo(models.Model):

    def __unicode__(self):
        return unicode(self.app)

    app = models.CharField(max_length=64, choices=InstalledGames)
    title = models.CharField(max_length=512)
    description = models.TextField()
    video_embed_code = models.TextField()
