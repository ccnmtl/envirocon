from django.test import TestCase
from envirocon.game_many.models import (
    ConflictAssessment, ExplainYourReportSelection, RecommendingInterventions,
    FundingInterventions, TrackingYourProjects, ResultsFramework, FinalPaper,
    DonorsConference)


class TestConflictAssessmentMethods(TestCase):

    def setUp(self):
        self.model = ConflictAssessment()

    def test_caseassesment_pages(self):
        self.assertEquals(self.model.pages(),
                          ('index', 'page2'))

    def test_caseassesment_template_no_id(self):
        self.assertEquals(self.model.template(),
                          ('game_many/conflict_assessment_intro.html',
                           {'sampledata': "hello"}))

    def test_caseassesment_template_page2(self):
        self.assertEquals(self.model.template(page_id="page2"),
                          ('game_many/conflict_assessment.html',
                           {'sampledata': "hello"}))

    def test_caseassesment_variables(self):
        self.assertEquals(self.model.variables(),
                          ['conflict_assessment'])

    def test_caseassesment_resources_no_var(self):
        self.assertEquals(self.model.resources(game_state="game_state"),
                          [])


class TestExplainYourReportSelectionMethods(TestCase):

    def setUp(self):
        self.model = ExplainYourReportSelection()

    def test_exprepsel_pages(self):
        self.assertEquals(self.model.pages(),
                          ('index', 'page2'))

    def test_exprepsel_template_no_id(self):
        self.assertEquals(
            self.model.template(),
            ('game_many/explain_your_report_selection_intro.html',
             {'sampledata': "hello"}))

    def test_exprepsel_template_page2(self):
        self.assertEquals(self.model.template(page_id="page2"),
                          ('game_many/explain_your_report_selection.html',
                           {'sampledata': "hello"}))

    def test_exprepsel_variables(self):
        self.assertEquals(self.model.variables(),
                          ['explain_your_report_selection'])


class TestRecommendingInterventionsMethods(TestCase):

    def setUp(self):
        self.model = RecommendingInterventions()

    def test_recinters_pages(self):
        self.assertEquals(self.model.pages(),
                          ('index', 'page2'))

    def test_recinters_template_no_id(self):
        self.assertEquals(self.model.template(),
                          ('game_many/recommending_interventions_intro.html',
                           {'sampledata': "hello"}))

    def test_recinters_template_page2(self):
        self.assertEquals(self.model.template(page_id="page2"),
                          ('game_many/recommending_interventions.html',
                           {'sampledata': "hello"}))

    def test_recinters_variables(self):
        self.assertEquals(self.model.variables(),
                          ['recommending_interventions'])

    def test_recinters_resources_no_var(self):
        self.assertEquals(self.model.resources(game_state="game_state"),
                          [])

    def test_recinters_resources_onopen(self):
        self.assertEquals(
            self.model.resources(game_state="game_state", onopen=True),
            [{"page_id": 'watching_brief',
              "type": 'file',
              "title": 'First Watching Brief.pdf',
              }])


class TestFundingInterventionsMethods(TestCase):

    def setUp(self):
        self.model = FundingInterventions()

    def test_fundinginters_pages(self):
        self.assertEquals(self.model.pages(),
                          ('index', 'page2'))

    def test_fundinginters_template_no_id(self):
        self.assertEquals(self.model.template(),
                          ('game_many/funding_interventions_intro.html',
                           {'sampledata': "hello"}))

    def test_fundinginters_template_page2(self):
        self.assertEquals(self.model.template(page_id="page2"),
                          ('game_many/funding_interventions.html',
                           {'sampledata': "hello"}))

    def test_fundinginters_variables(self):
        self.assertEquals(self.model.variables(),
                          ['funding_interventions'])

    def test_fundinginters_public_variables(self):
        self.assertEquals(self.model.public_variables(),
                          ['funding_interventions'])


class TestTrackingYourProjectsMethods(TestCase):

    def setUp(self):
        self.model = TrackingYourProjects()

    def test_trackyourproj_pages(self):
        self.assertEquals(self.model.pages(),
                          ('index', 'page2'))

    def test_trackyourproj_variables(self):
        self.assertEquals(self.model.variables(),
                          ['tracking_your_projects'])


class TestResultsFrameworkMethods(TestCase):

    def setUp(self):
        self.model = ResultsFramework()

    def test_resultsframe_pages(self):
        self.assertEquals(self.model.pages(),
                          ('index', 'page2'))

    def test_resultsframe_template_no_id(self):
        self.assertEquals(self.model.template(),
                          ('game_many/results_framework_intro.html',
                           {'sampledata': "hello"}))

    def test_resultsframe_template_page2(self):
        self.assertEquals(self.model.template(page_id="page2"),
                          ('game_many/results_framework.html',
                           {'sampledata': "hello"}))

    def test_resultsframe_variables(self):
        self.assertEquals(self.model.variables(),
                          ['results_framework'])

    def test_resultsframe_resources_no_var(self):
        self.assertEquals(self.model.resources(game_state="game_state"),
                          [])

    def test_resultsframe_resources_onopen(self):
        self.assertEquals(
            self.model.resources(game_state="game_state", onopen=True),
            [{"page_id": 'overview',
              "type": 'file',
              "title": 'Results Framework Overview.pdf',
              },
             {"page_id": 'matrices',
             "type": 'file',
             "title": 'Cluster Matrices.xls'}])


class TestDonorsConferenceMethods(TestCase):

    def setUp(self):
        self.model = DonorsConference()

    def test_donersconf_pages(self):
        self.assertEquals(self.model.pages(),
                          ('index', 'page2'))

    def test_donersconf_variables(self):
        self.assertEquals(self.model.variables(),
                          ['donors_conference'])

    def test_donersconf_public_variables(self):
        self.assertEquals(self.model.public_variables(),
                          ['donors_conference'])


class TestFinalPaperMethods(TestCase):

    def setUp(self):
        self.model = FinalPaper()

    def test_final_paper_pages(self):
        self.assertEquals(self.model.pages(),
                          ('index', 'page2', 'page3'))

    def test_final_paper_template_no_id(self):
        self.assertEquals(self.model.template(),
                          ('game_many/final_paper_intro.html', {}))

    def test_final_paper_template_page2(self):
        self.assertEquals(self.model.template(page_id="page2"),
                          ('game_many/final_paper.html', {}))

    def test_final_paper_template_page3(self):
        self.assertEquals(self.model.template(page_id="page3"),
                          ('game_many/final_paper2.html', {}))

    def test_final_paper_variables(self):
        self.assertEquals(self.model.variables(),
                          ['final_paper'])

    def test_final_paper_public_variables(self):
        self.assertEquals(self.model.public_variables(),
                          ['final_paper'])
