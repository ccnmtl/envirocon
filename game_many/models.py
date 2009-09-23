from django.db import models
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, Http404
import os.path

# Create your models here.
from game.installed_games import InstalledGames,GameInterface

fileroot = os.path.abspath(".") + "/game_many/files/"

# point values for funding choices
def funding_points(week=4):
  value = {
             'water-supply-high':1,
             'water-supply-med' :2,
             'water-supply-low' :3,
             'sanitation-high'  :1,
             'sanitation-med'   :2,
             'sanitation-low'   :3,
             'waste-high'       :2,
             'waste-med'        :1,
             'waste-low'        :3,
             'timber-high'      :2,
             'timber-med'       :2,
             'timber-low'       :1,
             'deforestation-high':2,
             'deforestation-med':1,
             'deforestation-low':3,
             'tenure-high'      :3,
             'tenure-med'       :2,
             'tenure-low'       :1,
             'nomadic-high'     :3,
             'nomadic-med'      :2,
             'nomadic-low'      :1,
             'agriculture-high' :2,
             'agriculture-med'  :3,
             'agriculture-low'  :1,
             'desertification-high':3,
             'desertification-med':2,
             'desertification-low':1,
             'habitat-high'     :3,
             'habitat-med'      :2,
             'habitat-low'      :1,
             'water-high'       :2,
             'water-med'        :1,
             'water-low'        :3,
             'capacity-high'    :1,
             'capacity-med'     :2,
             'capacity-low'     :3,
            }
  if week == 6:
    value['timber-med'] = 1
    value['timber-low'] = 3
    value['tenure-med'] = 1
    value['tenure-low'] = 2
    value['nomadic-high'] = 1
    value['nomadic-low'] = 3
    value['agricultural-med'] = 1
    value['agricultural-low'] = 3
    value['desertification-high'] = 2
    value['desertification-med'] = 1
    value['desertification-low'] = 3

  return value

## week1 ##
class ConflictAssessment(GameInterface):
    def pages(self):
        return ('index','page2')

    def template(self,page_id=None,public_state=None):
        game_context = {'sampledata':"hello"}#, documents:documents}
        if page_id == "country_narrative":
          return('file',servefile("ConflictAssessment_CountryNarrative.pdf", "Country_Narrative.pdf"))

        if page_id == "page2":
          return ('game_many/conflict_assessment.html',game_context)

        return ('game_many/conflict_assessment_intro.html',game_context)
    
    def variables(self,page_id=None):
        return ['conflict_assessment']
        
    def resources(self,game_state,onopen=False,onclosed=False):
        if onopen:
            return [{"page_id":'country_narrative',
                     "type":'file',
                     "title":'Country Narrative.pdf',
                     }]
        else:
            return []

InstalledGames.register_game('conflict_assessment',
                             'Conflict Assessment',
                             ConflictAssessment() )
                             
                             
class ExplainYourReportSelection(GameInterface):
    """
    Week 1, Explain Your Report Selection
    """

    def pages(self):
        return ('index','page2')

    def template(self,page_id=None,public_state=None):
        game_context = {'sampledata':"hello"}
        if page_id == "page2":
          return ('game_many/explain_your_report_selection.html',game_context)
        return ('game_many/explain_your_report_selection_intro.html',game_context)
    
    def variables(self,page_id=None):
        return ['explain_your_report_selection','additional_information']

InstalledGames.register_game('explain_your_report_selection',
                             'Explain Your Report Selection',
                             ExplainYourReportSelection() )


class RecommendingInterventions(GameInterface):
    """
    Week 3, Recommending Interventions
    """
    def pages(self):
        return ('index','page2')

    def template(self,page_id=None,public_state=None):
        game_context = {'sampledata':"hello"}
        if page_id == "watching_brief":
          return('file', servefile("RecommendingInterventions_FirstWatchingBrief.pdf", "First_Watching_Brief.pdf"))

        if page_id == "page2":
          return ('game_many/recommending_interventions.html',game_context)
        return ('game_many/recommending_interventions_intro.html',game_context)
    
    def variables(self,page_id=None):
        return ['recommending_interventions']

    def resources(self,game_state,onopen=False,onclosed=False):
        if onopen:
            return [{"page_id":'watching_brief',
                     "type":'file',
                     "title":'First Watching Brief.pdf',
                     }]
        else:
            return []

InstalledGames.register_game('recommending_interventions',
                             'Recommending Interventions',
                             RecommendingInterventions() )

class FundingInterventions(GameInterface):
    """
    Week 4, Funding Interventions
    """
    def pages(self):
        return ('index','page2')

    def template(self,page_id=None,public_state=None):
        game_context = {'sampledata':"hello"}
        if page_id == "page2":
          return ('game_many/funding_interventions.html',game_context)
        return ('game_many/funding_interventions_intro.html',game_context)
    
    def variables(self,page_id=None):
        return ['funding_interventions']

    def public_variables(self):
        return ['funding_interventions']


InstalledGames.register_game('funding_interventions',
                             'Funding Interventions',
                             FundingInterventions() )

class TrackingYourProjects(GameInterface):
    """
    Week 4, Tracking Your Projects
    """
    def pages(self):
        return ('index','page2',)

    def template(self,page_id=None,public_state=None):
        game_context = {'sampledata':"hello"}
        if page_id == "page2":
          return ('game_many/tracking_your_projects.html',game_context)
        return ('game_many/tracking_your_projects_intro.html',game_context)
    
    def variables(self,page_id=None):
        return ['tracking_your_projects']

InstalledGames.register_game('tracking_your_projecst',
                             'Tracking Your Projects',
                             TrackingYourProjects() )

class ResultsFramework(GameInterface):
    """
    Week 5, Results Framework
    """
    def pages(self):
        return ('index','page2',)

    def template(self,page_id=None,public_state=None):
        game_context = {'sampledata':"hello"}
        if page_id == "overview":
          return('file', servefile("ResultsFramework_Overview.pdf", "Results_Framework_Overview.pdf"))
        if page_id == "matrices":
          return('file', servefile("ResultsFramework_ClusterMatrices.xls", "Results_Framework_Cluster_Matrices.xls", "excel/ms-excel"))
        if page_id == "page2":
          return ('game_many/results_framework.html',game_context)
        return ('game_many/results_framework_intro.html',game_context)
    
    def variables(self,page_id=None):
        return ['results_framework']

    def resources(self,game_state,onopen=False,onclosed=False):
        if onopen:
            return [{"page_id":'overview',
                     "type":'file',
                     "title":'Results Framework Overview.pdf',
                    },
                    {"page_id":'matrices',
                     "type":'file',
                     "title":'Cluster Matrices.xls'}
                   ]
        else:
            return []

InstalledGames.register_game('results_framework',
                             'Results Framework',
                             ResultsFramework() )

class DonorsConference(GameInterface):
    """
    Week 6, Donors Conference & More Interventions
    """
    
    def pages(self):
        return ('index','page2',)

    def template(self,page_id=None,public_state=None):
        game_context = {'sampledata':"hello"}
        if page_id == "summary":
          return('file', servefile("DonorsConference_DonorsConferenceSummary.pdf", "Donors_Conference_Summary.pdf"))
        if page_id == "watching_brief_1":
          return('file', servefile("DonorsConference_WatchingBrief1.pdf", "Second_Watching_Brief.pdf"))
        if page_id == "watching_brief_2":
          return('file', servefile("DonorsConference_WatchingBrief2.pdf", "Second_Watching_Brief.pdf"))
        if page_id == "watching_brief_3":
          return('file', servefile("DonorsConference_WatchingBrief3.pdf", "Second_Watching_Brief.pdf"))

        if page_id == "page2":
          return ('game_many/donors_conference.html',game_context)
        return ('game_many/donors_conference_intro.html',game_context)
    
    def variables(self,page_id=None):
        return ['donors_conference']

    def public_variables(self):
        return ['donors_conference']

    def resources(self,game_state,onopen=False,onclosed=False):
        if onopen and game_state.has_key('funding_interventions'):
          funded = game_state['funding_interventions']
          pts = funding_points()
          points = sum([pts[intervention] for intervention in funded])
          if points < 17:
            wb = {"page_id":'watching_brief_1', "type":'file', "title":'Second Watching Brief.pdf'}
          elif points < 30:
            wb = {"page_id":'watching_brief_2', "type":'file', "title":'Second Watching Brief.pdf'}
          else:
            wb = {"page_id":'watching_brief_3', "type":'file', "title":'Second Watching Brief.pdf'}
          return [{"page_id":'summary',
                   "type":'file',
                   "title":'Donors Conference Summary.pdf',
                  },
                  wb
                  ]
        else:
            return []

InstalledGames.register_game('donors_conference',
                             'Donors Conference',
                             DonorsConference() )

class FinalPaper(GameInterface):
    """
    Week 8, Final Paper
    """
    def pages(self):
        return ('index','page2',)

    def template(self,page_id=None,public_state=None):
        game_context = {'sampledata':"hello"}
        if page_id == "watching_brief_1":
          return('file', servefile("FinalPaper_WatchingBrief1.pdf", "Third_Watching_Brief.pdf"))
        if page_id == "watching_brief_2":
          return('file', servefile("FinalPaper_WatchingBrief2.pdf", "Third_Watching_Brief.pdf"))
        if page_id == "watching_brief_3":
          return('file', servefile("FinalPaper_WatchingBrief3.pdf", "Third_Watching_Brief.pdf"))

        if page_id == "page2":
          return ('game_many/final_paper.html',game_context)
        return ('game_many/final_paper_intro.html',game_context)
    
    def variables(self,page_id=None):
        return ['final_paper']

    def resources(self,game_state,onopen=False,onclosed=False):
        if onopen:
            return [
                    {"page_id":'watching_brief_1',
                     "type":'file',
                     "title":'Third Watching Brief.pdf',
                    },
                    {"page_id":'watching_brief_2',
                     "type":'file',
                     "title":'Third Watching Brief.pdf',
                    },
                    {"page_id":'watching_brief_3',
                     "type":'file',
                     "title":'Third Watching Brief.pdf',
                    },
                   ]

InstalledGames.register_game('final_paper',
                             'Final Paper',
                             FinalPaper() )

## helper function ##
def servefile(filename, name, mimetype="application/pdf"):
  # instead of serving the file directly, open it and pipe it over (for security)
  path = InstalledGames.absolute_path("game_many", "files/%s" % filename) 
  # return 404 if the file DNE
  try:
    file = open(path,"rb")
  except:
    raise Http404  #TODO this doesn't do what i expected
  response = HttpResponse(FileWrapper(file), mimetype=mimetype)
  response['Content-Disposition'] = 'attachment; filename=%s' % name
  response['Content-Length'] = os.path.getsize(path)
  return response
