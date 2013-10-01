# flake8: noqa
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, Http404
import os.path

# Create your models here.
from envirocon.game.installed_games import InstalledGames, GameInterface
from funding_interventions import funding_points, funding_autoshocks

fileroot = os.path.abspath(".") + "/game_many/files/"

# week1 ##


class ConflictAssessment(GameInterface):

    def pages(self):
        return ('index', 'page2')

    def template(self, page_id=None, public_state=None):
        game_context = {'sampledata': "hello"}  # , documents:documents}
        if page_id == "country_narrative":
            return('file', servefile("ConflictAssessment_CountryNarrative.pdf",
                                     "Country_Narrative.pdf"))

        if page_id == "page2":
            return ('game_many/conflict_assessment.html', game_context)

        return ('game_many/conflict_assessment_intro.html', game_context)

    def variables(self, page_id=None):
        return ['conflict_assessment']

    def resources(self, game_state, onopen=False, onclosed=False):
        if onopen:
            return [{"page_id": 'country_narrative',
                     "type": 'file',
                     "title": 'Country Narrative.pdf',
                     }]
        else:
            return []

InstalledGames.register_game('conflict_assessment',
                             'Conflict Assessment',
                             ConflictAssessment())


class ExplainYourReportSelection(GameInterface):

    """
    Week 1, Explain Your Report Selection
    """

    def pages(self):
        return ('index', 'page2')

    def template(self, page_id=None, public_state=None):
        game_context = {'sampledata': "hello"}
        if page_id == "page2":
            return ('game_many/explain_your_report_selection.html',
                    game_context)
        return ('game_many/explain_your_report_selection_intro.html',
                game_context)

    def variables(self, page_id=None):
        return ['explain_your_report_selection']  # ,'additional_information']

InstalledGames.register_game('explain_your_report_selection',
                             'Explain Your Report Selection',
                             ExplainYourReportSelection())


class RecommendingInterventions(GameInterface):

    """
    Week 3, Recommending Interventions
    """

    def pages(self):
        return ('index', 'page2')

    def template(self, page_id=None, public_state=None):
        game_context = {'sampledata': "hello"}
        if page_id == "watching_brief":
            return(
                'file',
                servefile("RecommendingInterventions_FirstWatchingBrief.pdf",
                          "First_Watching_Brief.pdf"))

        if page_id == "page2":
            return ('game_many/recommending_interventions.html',
                    game_context)
        return ('game_many/recommending_interventions_intro.html',
                game_context)

    def variables(self, page_id=None):
        return ['recommending_interventions']

    def resources(self, game_state, onopen=False, onclosed=False):
        if onopen:
            return [{"page_id": 'watching_brief',
                     "type": 'file',
                     "title": 'First Watching Brief.pdf',
                     }]
        else:
            return []

InstalledGames.register_game('recommending_interventions',
                             'Recommending Interventions',
                             RecommendingInterventions())


class FundingInterventions(GameInterface):

    """
    Week 4, Funding Interventions
    """

    def pages(self):
        return ('index', 'page2')

    def template(self, page_id=None, public_state=None):
        game_context = {'sampledata': "hello"}
        if page_id == "page2":
            return ('game_many/funding_interventions.html', game_context)
        return ('game_many/funding_interventions_intro.html', game_context)

    def variables(self, page_id=None):
        return ['funding_interventions']

    def public_variables(self):
        return ['funding_interventions']

    def consequences(self, game_state):
        return DonorsConference().resources(game_state, onopen=True)


InstalledGames.register_game('funding_interventions',
                             'Funding Interventions',
                             FundingInterventions())


class TrackingYourProjects(GameInterface):

    """
    Week 4, Tracking Your Projects
    """

    def pages(self):
        return ('index', 'page2',)

    def template(self, page_id=None, public_state=None):
        funded = {}
        if 'tracking_your_projects' in public_state['resources_by_app']:
            if 'funded' in public_state[
                    'resources_by_app']['tracking_your_projects']:
                funded = public_state['resources_by_app'][
                    'tracking_your_projects']['funded']['value']
        game_context = {'funded': funded}
        if page_id == "page2":
            return ('game_many/tracking_your_projects.html', game_context)
        return ('game_many/tracking_your_projects_intro.html', game_context)

    def variables(self, page_id=None):
        return ['tracking_your_projects']

    def resources(self, game_state, onopen=False, onclosed=False):
        if onopen and 'funding_interventions' in game_state:
            funded = game_state['funding_interventions']
            return [{"page_id": 'funded',
                     "type": 'data',
                     'value': funded.keys()}]

    def autoshock(self, game_state):
        # to appear in Results Framework
        return funding_autoshocks('funding_interventions',
                                  game_state['funding_interventions'])


InstalledGames.register_game('tracking_your_projects',
                             'Tracking Your Projects',
                             TrackingYourProjects())


class ResultsFramework(GameInterface):

    """
    Week 5, Results Framework
    """

    def pages(self):
        return ('index', 'page2',)

    def template(self, page_id=None, public_state=None):
        game_context = {'sampledata': "hello"}
        if page_id == "overview":
            return('file', servefile("ResultsFramework_Overview.pdf",
                                     "Results_Framework_Overview.pdf"))
        if page_id == "matrices":
            return(
                'file',
                servefile("ResultsFramework_ClusterMatrices.xls",
                          "Results_Framework_Cluster_Matrices.xls",
                          "excel/ms-excel"))
        if page_id == "page2":
            return ('game_many/results_framework.html', game_context)
        return ('game_many/results_framework_intro.html', game_context)

    def variables(self, page_id=None):
        return ['results_framework']

    def resources(self, game_state, onopen=False, onclosed=False):
        if onopen:
            return [{"page_id": 'overview',
                     "type": 'file',
                     "title": 'Results Framework Overview.pdf',
                     },
                    {"page_id": 'matrices',
                     "type": 'file',
                     "title": 'Cluster Matrices.xls'}
                    ]
        else:
            return []

InstalledGames.register_game('results_framework',
                             'Results Framework',
                             ResultsFramework())


class DonorsConference(GameInterface):

    """
    Week 6, Donors Conference & More Interventions
    """

    def pages(self):
        return ('index', 'page2',)

    def template(self, page_id=None, public_state=None):
        points = 0
        ineligible = {}
        if 'donors_conference' in public_state['resources_by_app']:
            if 'week4points' in public_state[
                    'resources_by_app']['donors_conference']:
                points = public_state['resources_by_app'][
                    'donors_conference']['week4points']['value']
            if 'ineligible' in public_state[
                    'resources_by_app']['donors_conference']:
                ineligible = public_state['resources_by_app'][
                    'donors_conference']['ineligible']['value']

        #, 'wb2':wb2}
        game_context = {'week4points': points, 'ineligible': ineligible}

        if page_id == "summary":
            return('file',
                   servefile("DonorsConference_DonorsConferenceSummary.pdf",
                             "Donors_Conference_Summary.pdf"))
        if page_id == "watching_brief_1":
            return('file', servefile("DonorsConference_WatchingBrief1.pdf",
                                     "Second_Watching_Brief.pdf"))
        if page_id == "watching_brief_2":
            return('file', servefile("DonorsConference_WatchingBrief2.pdf",
                                     "Second_Watching_Brief.pdf"))
        if page_id == "watching_brief_3":
            return('file', servefile("DonorsConference_WatchingBrief3.pdf",
                                     "Second_Watching_Brief.pdf"))

        if page_id == "page2":
            return ('game_many/donors_conference.html', game_context)
        return ('game_many/donors_conference_intro.html', game_context)

    def variables(self, page_id=None):
        return ['donors_conference']

    def public_variables(self):
        return ['donors_conference']

    def resources(self, game_state, onopen=False, onclosed=False):
        if onopen and 'funding_interventions' in game_state:
            funded = game_state['funding_interventions']

            # certain interventions, if funded in week 4, are ineligible to be
            # funded in week 6
            ineligible = [intervention for intervention in funded
                          if intervention in ['timber-low',
                                              'nomadic-low',
                                              'agricultural-low',
                                              'desertification-low',
                                              'habitat-low',
                                              'water-low', ]]

            # teams who choose the 3-point option in any of the first 3
            # categories automatically get wb2
            wb2_choices = [intervention for intervention in funded
                           if intervention in ['water-supply-low',
                                               'sanitation-low',
                                               'waste-low']]
            autowb2 = False
            if wb2_choices != []:
                autowb2 = True

            unlock_wb2 = False
            points = funding_points(funded)
            if autowb2 or (points > 17 and points < 30):
                wb = {"page_id": 'watching_brief_2', "type":
                      'file', "title": 'Second Watching Brief.pdf'}
            elif points < 17:
                wb = {"page_id": 'watching_brief_1', "type":
                      'file', "title": 'Second Watching Brief.pdf'}
            else:  # 30 or more points
                wb = {"page_id": 'watching_brief_3', "type":
                      'file', "title": 'Second Watching Brief.pdf'}
                # yes, the third watching brief unlocks the WB2 map layers.
                # confusing but correct.
                unlock_wb2 = True
            return [{"page_id": 'summary',
                     "type": 'file',
                     "title": 'Donors Conference Summary.pdf',
                     },
                    wb,
                    {"page_id": 'week4points',
                        "type": 'data', 'value': points},
                    {"page_id": 'ineligible', "type":
                        'data', "value": ineligible},
                    {"page_id": 'wb2', "type": 'data', "value": unlock_wb2},
                    ]
        else:
            return []

    def consequences(self, game_state):
        return FinalPaper().resources(game_state, onopen=True)

    def autoshock(self, game_state):
        return funding_autoshocks('donors_conference',
                                  game_state['donors_conference'])


InstalledGames.register_game('donors_conference',
                             'Donors Conference',
                             DonorsConference())


class FinalPaper(GameInterface):

    """
    Week 8, Final Paper
    """

    def pages(self):
        return ('index', 'page2', 'page3')

    def template(self, page_id=None, public_state=None):
        game_context = {}

        if page_id == "watching_brief_1":
            return('file', servefile("FinalPaper_WatchingBrief1.pdf",
                                     "Third_Watching_Brief.pdf"))
        if page_id == "watching_brief_2":
            return('file', servefile("FinalPaper_WatchingBrief2.pdf",
                                     "Third_Watching_Brief.pdf"))
        if page_id == "watching_brief_3":
            return('file', servefile("FinalPaper_WatchingBrief3.pdf",
                                     "Third_Watching_Brief.pdf"))

        if page_id == "page2":
            return ('game_many/final_paper.html', game_context)
        if page_id == "page3":
            return ('game_many/final_paper2.html', game_context)
        return ('game_many/final_paper_intro.html', game_context)

    def variables(self, page_id=None):
        return ['final_paper']

    def public_variables(self, page_id=None):
        return ['final_paper']

    def resources(self, game_state, onopen=False, onclosed=False):
        if onopen and 'donors_conference' in game_state:
            # week 4 points carry over
            week4points = 0
            if 'funding_interventions' in game_state:
                week4points = funding_points(
                    game_state['funding_interventions'])
            week6points = funding_points(game_state['donors_conference'], 6)
            points = week4points + week6points
            # print points
            # teams who choose the 3-point option in any of the first 3
            # categories automatically get wb2
            funded = game_state['donors_conference']
            wb2_choices = [intervention for intervention in funded
                           if intervention in ['water-supply-low',
                                               'sanitation-low',
                                               'waste-low']]
            autowb2 = False
            if wb2_choices != []:
                autowb2 = True

            unlock_wb3 = False
            if autowb2 or (points > 32 and points < 59):
                wb = {"page_id": 'watching_brief_2', "type":
                      'file', "title": 'Third Watching Brief.pdf'}
            elif points < 33:
                wb = {"page_id": 'watching_brief_1', "type":
                      'file', "title": 'Third Watching Brief.pdf'}
            else:  # points > 58
                wb = {"page_id": 'watching_brief_3', "type":
                      'file', "title": 'Third Watching Brief.pdf'}
                unlock_wb3 = True
            return [wb,
                    {"page_id": 'wb3', "type": 'data', "value": unlock_wb3},
                    ]
        else:
            return []


InstalledGames.register_game('final_paper',
                             'Final Paper',
                             FinalPaper())

# helper function ##


def servefile(filename, name, mimetype="application/pdf"):
    # instead of serving the file directly, open it and pipe it over (for
    # security)
    path = InstalledGames.absolute_path("envirocon.game_many",
                                        "files/%s" % filename)
    # return 404 if the file DNE
    try:
        file_handle = open(path, "rb")
    except:
        raise Http404  # TODO this doesn't do what i expected
    response = HttpResponse(FileWrapper(file_handle), mimetype=mimetype)
    response['Content-Disposition'] = 'attachment; filename=%s' % name
    response['Content-Length'] = os.path.getsize(path)
    return response
