import re

class GameInterface:
    """This class is meant to be the parent for game application
    """
    def pages(self):
        return ('page_one',)

    def template(self,page_id=None):
        game_context = {'page_id':page_id}
        return ('game/game.html',game_context)

    def variables(self,page_id=None):
        """return a list of strings to declare the variables you will store/retrieve
        If your variable name conflicts with another game, you will share state
        """
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

    def template(self,game_code,page_id):
        return self.GAME_OBJECTS[game_code].template(page_id)
        
    def variables(self,game_code,page_id=None):
        return self.GAME_OBJECTS[game_code].variables(page_id)
        


InstalledGames = InstalledGamesLazySingleton()

