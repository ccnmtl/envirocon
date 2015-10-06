from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from envirocon.envirocon_main.models import GroundWorkClass


class TestGroundWorkClassModels(TestCase):

    def setUp(self):
        self.gwc = GroundWorkClass()

    def test_gwc_init(self):
        self.assertIsNotNone(self.gwc)
        self.assertEquals(unicode(self.gwc.faculty_group.name),
                          'Another Test Class Faculty')
        self.assertEquals(unicode(self.gwc.course_group.name),
                          'Another Test Class Students')
        self.assertIsNotNone(self.gwc.course)
        self.assertIsNotNone(self.gwc.game)
        self.assertIsNotNone(self.gwc.faculty_team)

    def test_gwc_init_creator(self):
        cr = User.objects.create()
        ngwc = GroundWorkClass(creator=cr, title='New Name')
        self.assertIsNotNone(ngwc.creator)

    def test_next_month(self):
        nm = self.gwc.next_month()
        d = datetime.today()
        nxtmn = datetime(d.year + (d.month + 1) / 12,
                         ((d.month + 1) % 12) + 1, d.day)
        self.assertEquals(nm, nxtmn)

    def test_copy_survey_srvy_none(self):
        pass
