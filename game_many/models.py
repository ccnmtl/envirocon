from django.db import models
from django.http import HttpResponse, Http404
import os.path

# Create your models here.
from game.installed_games import InstalledGames,GameInterface

fileroot = os.path.abspath(".") + "/game_many/files/"

## week1 ##
class ConflictAssessment(GameInterface):
    def pages(self):
        return ('index','page2')

    def template(self,page_id=None,public_state=None):
        game_context = {'sampledata':"hello"}#, documents:documents}
        if page_id == "country_narrative":
          return('file',servepdf("ConflictAssessment_CountryNarrative.pdf", "Country_Narrative.pdf"))

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
        return ['explain_your_report_selection']

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
          return('file', servepdf("RecommendingInterventions_FirstWatchingBrief.pdf", "First_Watching_Brief.pdf"))

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
        if page_id == "page2":
          return ('game_many/results_framework.html',game_context)
        return ('game_many/results_framework_intro.html',game_context)
    
    def variables(self,page_id=None):
        return ['results_framework']

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
          return('file', servepdf("DonorsConference_DonorsConferenceSummary.pdf", "Donors_Conference_Summary.pdf"))
        if page_id == "watching_brief_1":
          return('file', servepdf("DonorsConference_WatchingBrief1.pdf", "Second_Watching_Brief.pdf"))
        if page_id == "watching_brief_2":
          return('file', servepdf("DonorsConference_WatchingBrief2.pdf", "Second_Watching_Brief.pdf"))
        if page_id == "watching_brief_3":
          return('file', servepdf("DonorsConference_WatchingBrief3.pdf", "Second_Watching_Brief.pdf"))

        if page_id == "page2":
          return ('game_many/donors_conference.html',game_context)
        return ('game_many/donors_conference_intro.html',game_context)
    
    def variables(self,page_id=None):
        return ['donors_conference']

    def resources(self,game_state,onopen=False,onclosed=False):
        if onopen:
            return [{"page_id":'summary',
                     "type":'file',
                     "title":'Donors Conference Summary.pdf',
                    },
                    {"page_id":'watching_brief_1',
                     "type":'file',
                     "title":'Second Watching Brief.pdf',
                    },
                    {"page_id":'watching_brief_2',
                     "type":'file',
                     "title":'Second Watching Brief.pdf',
                    },
                    {"page_id":'watching_brief_3',
                     "type":'file',
                     "title":'Second Watching Brief.pdf',
                    },
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
        if page_id == "page2":
          return ('game_many/final_paper.html',game_context)
        return ('game_many/final_paper_intro.html',game_context)
    
    def variables(self,page_id=None):
        return ['final_paper']

InstalledGames.register_game('final_paper',
                             'Final Paper',
                             FinalPaper() )

## helper function ##
def servepdf(filename, name):
  # instead of serving the file directly, open it and pipe it over (for security)
  path = InstalledGames.absolute_path("game_many", "files/%s" % filename) 
  # return 404 if the file DNE
  try:
    file = open(path,"rb")
  except:
    raise Http404  #TODO this doesn't do what i expected
  response = HttpResponse(mimetype='application/pdf')
  response['Content-Disposition'] = 'attachment; filename=%s' % name
  response.write(file.read())
  return response