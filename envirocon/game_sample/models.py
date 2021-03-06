from envirocon.game.installed_games import InstalledGames, GameInterface


class SampleGame(GameInterface):

    def pages(self):
        return ('index',)

    def template(self, page_id=None, public_state=None):
        game_context = {'sampledata': "hello"}
        return ('game_sample/index.html', game_context)

    def variables(self, page_id=None):
        return []

InstalledGames.register_game('sample',
                             'Sample Game',
                             SampleGame())
