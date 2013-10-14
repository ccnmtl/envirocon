from django.test import TestCase
from courseaffils.models import Course
from django.contrib.auth.models import Group, User
from envirocon.statefulgame.models import Game


class TestGame(TestCase):
    def setUp(self):
        self.student_group = Group.objects.create(name="studentgroup")
        self.faculty_group = Group.objects.create(name="facultygroup")
        self.student = User.objects.create(username="student")
        self.faculty = User.objects.create(username="faculty")
        self.student.groups.add(self.student_group)
        self.faculty.groups.add(self.faculty_group)
        self.c = Course.objects.create(
            group=self.student_group,
            title="test course",
            faculty_group=self.faculty_group)

    def test_unicode(self):
        g = Game.objects.create(course=self.c)
        self.assertEqual(str(g), "test course")
