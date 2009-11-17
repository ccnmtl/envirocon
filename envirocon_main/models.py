from django.db import models
import datetime
#not sure why get_model doesn't work--the bowels of django app loading?
from statefulgame.models import Game,Assignment

Course = models.get_model('courseaffils','course')
Group = models.get_model('auth','group')
Team = models.get_model('teams','team')

class GroundWorkClass:
    def __init__(self,title='Another Test Class',creator=None):
        
        self.faculty_group = Group.objects.create(name=title+' Faculty')
        self.course_group = Group.objects.create(name=title+' Students')

        self.course = Course.objects.create(group=self.course_group,
                                            faculty_group=self.faculty_group,
                                            title = title
                                            )

        if creator:
            self.faculty_group.user_set.add(creator)
            self.course_group.user_set.add(creator)

        #NO SURVEY FOR NOW
        #self.survey = 'x'
        #import fixture
        # remove pks of leaves
        # create objects in order of inheritance and
        # replace pks

        self.game = Game.objects.create(course=self.course)
        #activity1,2,3,4,5,6...
        self.faculty_team = Team(course=self.course,
                                 group=self.faculty_group
                                 )
        self.faculty_team.save()

        d = datetime.datetime.today()
        next_month = datetime.datetime(d.year + (d.month+2)/12,(d.month+2) %12,d.day)

        for a in activities:
            ass = Assignment.objects.create(app=a['app'],
                                            name=a['name'],
                                            game=self.game,
                                            individual=a['individual'],
                                            open=False,
                                            close_date=next_month,
                                            )


activities = [
    {'app':'conflict_assessment',
     'name':'Conflict Assessment',
     'individual':True,
     },
    {'app':'obtain_additional_information',
     'name':'Obtain Additional Information',
     'individual':False,
     },
    {'app':'explain_your_report_selection',
     'name':'Explain Your Report Selection',
     'individual':False,
     },
    {'app':'plot_sectors',
     'name':'Viewing and Plotting Environmental and Peacebuilding Sectors',
     'individual':False,
     },
    {'app':'recommending_interventions',
     'name':'Recommending Interventions',
     'individual':False,
     },
    {'app':'funding_interventions',
     'name':'Funding Interventions',
     'individual':False,
     },
    {'app':'tracking_your_projects',
     'name':'Tracking Your Projects',
     'individual':False,
     },
    {'app':'results_framework',
     'name':'The Results Framework',
     'individual':False,
     },
    {'app':'donors_conference',
     'name':'Donors Conference & More Interventions',
     'individual':False,
     },
    {'app':'final_paper',
     'name':'Final Paper',
     'individual':True,
     },
    ]
