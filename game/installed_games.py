import re
import os.path
from django.conf import settings


class GameInterface:
    """This class is meant to be the parent for game application
    """
    def pages(self):
        return ('page_one',)

    def template(self,page_id=None,public_state=None):
        """return a tuple of template_name and game_context which will be
        available for the template.
        If you return "file" as the template then game_context
        should be a full http response which can be served directly to the client
        @param public_state is a dict with keys listed in public_variables
        if they have been set (by other apps)
        """
        game_context = {'page_id':page_id}
        return ('game/game.html',game_context)

    def variables(self,page_id=None):
        """return a list of strings to declare the variables you will store/retrieve
        If your variable name conflicts with another game, you will share state
        """
        return []

    def public_variables(self):
        """add these variables into the worldstate
        usable for other games
        don't include resource stuff here--only more interesting info
        """
        return []
        
    def resources(self,game_state,onopen=False,onclosed=False):
        """return a list of dicts may not be listed in pages()
        which are global resources for general availability at
        onset of starting the game or at the close of the game
        """
        #return [{"page_id":"foo","type":"map"},{"page_id":"foo","type":"file"}]
        return []



class InstalledGamesLazySingleton:
    #GAMES_INSTALLED = []
    GAME_OBJECTS = dict()
    GAME_NAMES = dict()    

    def register_game(self, game_code, view_name, game_obj):
        #self.GAMES_INSTALLED.append( (game_code,view_name,) )
        self.GAME_OBJECTS[game_code] = game_obj
        self.GAME_NAMES[game_code] = view_name
        
        for p in game_obj.pages():
            if re.findall('\W',p):
                raise "Game pages must have only word (web friendly) characters."

    def __iter__(self):
        return iter(self.GAME_NAMES.items())

    def viewname(self,game_code):
        return self.GAME_NAMES[game_code]

    #more delegation, 2nd round
    def pages(self,game_code):
        return self.GAME_OBJECTS[game_code].pages()

    def template(self,game_code,page_id,public_state=None):
        return self.GAME_OBJECTS[game_code].template(page_id,public_state=None)
        
    def variables(self,game_code,page_id=None):
        return self.GAME_OBJECTS[game_code].variables(page_id)
        
    def public_variables(self,game_code):
        return self.GAME_OBJECTS[game_code].public_variables()

    def resources(self,game_code,game_state,onopen=False,onclosed=False):
        return self.GAME_OBJECTS[game_code].resources(game_state,onopen,onclosed)


    #UTILS #HACK #HACK #HACK
    def absolute_path(self,app,path):
        path = os.path.abspath(".")
        template = '%s/envirocon/%s/%s'
        if settings.DEBUG:
            template = '%s/%s/%s'            
        return template % (path,app,path)
    



InstalledGames = InstalledGamesLazySingleton()

