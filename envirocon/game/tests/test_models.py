from django.test import TestCase
from envirocon.game.installed_games import GameInterface
from envirocon.game.models import Activity, ActivityVideo


class TestGameInterfaceMethods(TestCase):

    def setUp(self):
        self.gi = GameInterface()

    def test_gi_pages(self):
        self.assertEquals(self.gi.pages(),
                          ('page_one',))

    def test_gi_template(self):
        self.assertEquals(self.gi.template(page_id=1),
                          ('game/game.html', {'page_id': 1}))

    def test_gi_variables(self):
        self.assertEquals(self.gi.variables(),
                          [])

    def test_gi_public_variables(self):
        self.assertEquals(self.gi.public_variables(),
                          [])

    def test_gi_resources(self):
        self.assertEquals(self.gi.resources(game_state="game_state"),
                          [])

    def test_gi_consequences(self):
        self.assertEquals(self.gi.consequences(game_state="game_state"),
                          False)


class TestActivityMethods(TestCase):

    def setUp(self):
        self.act = Activity(app='conflict_assessment')

    def test_activity_gamechoices(self):
        self.assertIn('conflict_assessment',
                      Activity.gamechoices())

    def test_activity_gamename(self):
        self.assertEquals('Conflict Assessment',
                          self.act.gamename())

    def test_activity_gamepages(self):
        self.assertEquals(('index', 'page2'),
                          self.act.gamepages())

    def test_activity_else_of_gamepages(self):
        self.act2 = Activity()
        self.assertEquals(tuple(),
                          self.act2.gamepages())

    def test_activity_gamevariables(self):
        self.assertEquals(['conflict_assessment'],
                          self.act.gamevariables())

    def test_activity_gamepublic_variables(self):
        self.assertEquals([],
                          self.act.gamepublic_variables())

    def test_activity_gametemplate(self):
        self.assertEquals(
            ('game_many/conflict_assessment_intro.html',
             {'sampledata': "hello"}),
            self.act.gametemplate())

    def test_activity_gameresources(self):
        self.assertEquals([],
                          self.act.gameresources('game_state'))

    def test_activity_onopen_gameresources(self):
        self.assertEquals([{"page_id": 'country_narrative',
                            "type": 'file',
                            "title": 'Country Narrative.pdf',
                            }],
                          self.act.gameresources('game_state', onopen=True))

    def test_activity_gamevideo(self):
        self.assertEquals(None,
                          self.act.gamevideo())


class TestActivityVideoMethod(TestCase):

    def setUp(self):
        self.actvid = ActivityVideo(app='conflict_assessment')

    def test_activity_gamechoices(self):
        self.assertEquals(unicode(self.actvid),
                          'conflict_assessment')
