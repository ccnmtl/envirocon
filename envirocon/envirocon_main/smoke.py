from courseaffils.models import Course
from smoketest import SmokeTest


class DBConnectivity(SmokeTest):
    def test_retrieve(self):
        cnt = Course.objects.all().count()
        self.assertTrue(cnt > 0)
