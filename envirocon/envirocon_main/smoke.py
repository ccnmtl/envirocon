from envirocon.envirocon_main.models import GroundWorkClass
from smoketest import SmokeTest


class DBConnectivity(SmokeTest):
    def test_retrieve(self):
        cnt = GroundWorkClass.objects.all().count()
        self.assertTrue(cnt > 0)
