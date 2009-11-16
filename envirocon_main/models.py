from django.db import models
from statefulgame.models import *
from courseaffils.models import *
from teams.models import *

class GroundWorkClass:
    def __init__(self,**kargs):
        self.faculty_group = 'x' #(submitter = faculty member
        self.course = Course(group=self.faculty_group)
        self.survey = 'x'
        #import fixture
        # remove pks of leaves
        # create objects in order of inheritance and
        # replace pks
        self.game = Game(course=self.course)
        #activity1,2,3,4,5,6...
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
        self.faculty_team = 'x'

        for a in activities:
            ass = Assignment(app=a['app'],
                             name=a['name'],
                             game=self.game,
                             individual=a['individual'],
                             open=False,
                             close_date='x',#next month
                             )
