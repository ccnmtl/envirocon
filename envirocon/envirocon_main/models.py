import datetime
from django.db import models
# not sure why get_model doesn't work--the bowels of django app loading?
from envirocon.statefulgame.models import Game, Assignment

Course = models.get_model('courseaffils', 'course')
Group = models.get_model('auth', 'group')
Team = models.get_model('teams', 'team')


Survey = models.get_model('survey', 'survey')
Question = models.get_model('survey', 'question')
QuestionChoices = models.get_model('survey', 'choices')


class GroundWorkClass:

    def __init__(self, title='Another Test Class',
                 creator=None, copy_survey=False):

        self.faculty_group = Group.objects.create(name=title + ' Faculty')
        self.course_group = Group.objects.create(name=title + ' Students')

        self.course = Course.objects.create(group=self.course_group,
                                            faculty_group=self.faculty_group,
                                            title=title
                                            )

        if creator:
            self.creator = creator
            self.faculty_group.user_set.add(creator)
            self.course_group.user_set.add(creator)

        # NO SURVEY FOR NOW
        #self.survey = 'x'
        #import fixture
        # remove pks of leaves
        # create objects in order of inheritance and
        # replace pks

        self.game = Game.objects.create(course=self.course)
        # activity1,2,3,4,5,6...
        self.faculty_team = Team(
            course=self.course,
            group=self.faculty_group,
            name='Team 1: Faculty of %s' % self.course.title)
        self.faculty_team.save()

        for a in activities:
            Assignment.objects.create(app=a['app'],
                                      name=a['name'],
                                      game=self.game,
                                      individual=a['individual'],
                                      open=False,
                                      close_date=self.next_month())

    def next_month(self):
        d = datetime.datetime.today()
        # month value is 1..12
        return datetime.datetime(d.year + (d.month + 1) / 12,
                                 ((d.month + 1) % 12) + 1, d.day)

    def copy_survey(self, orig=None):
        if orig is None:
            orig = Survey.objects.all()[0]
        if orig:
            self.survey = Survey(
                title=orig.title,
                slug='survey' + str(self.course.pk),
                description=orig.description,
                opens=datetime.datetime.today(),
                closes=self.next_month(),
                visible=True,
                public=False,
                restricted=True,
                allows_multiple_interviews=orig.allows_multiple_interviews,
                created_by=self.creator,
                editable_by=self.creator,
                recipient_type=orig.recipient_type,
                recipient_id=self.course.id)
            self.survey.save()
            for q in orig.questions.all():
                choices = q.choices.all()
                q.survey = self.survey
                q.id = None
                q.save(force_insert=True)
                for c in choices:
                    c.question = q
                    c.id = None
                    c.save(force_insert=True)

activities = [
    {'app': 'conflict_assessment',
     'name': 'Conflict Assessment',
     'individual': True,
     },
    {'app': 'obtain_additional_information',
     'name': 'Obtain Additional Information',
     'individual': False,
     },
    {'app': 'explain_your_report_selection',
     'name': 'Explain Your Report Selection',
     'individual': False,
     },
    {'app': 'plot_sectors',
     'name': 'Viewing and Plotting Environmental and Peacebuilding Sectors',
     'individual': False,
     },
    {'app': 'recommending_interventions',
     'name': 'Recommending Interventions',
     'individual': False,
     },
    {'app': 'funding_interventions',
     'name': 'Funding Interventions',
     'individual': False,
     },
    {'app': 'tracking_your_projects',
     'name': 'Tracking Your Projects',
     'individual': False,
     },
    {'app': 'results_framework',
     'name': 'The Results Framework',
     'individual': False,
     },
    {'app': 'donors_conference',
     'name': 'Donors Conference & More Interventions',
     'individual': False,
     },
    {'app': 'final_paper',
     'name': 'Final Paper',
     'individual': True,
     },
]
