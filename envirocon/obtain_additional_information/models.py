from django.http import HttpResponse

# Create your models here.
from envirocon.game.installed_games import InstalledGames, GameInterface

pdfs = {
    # structure this differently if we need it ordered for checkbox listing
    # this is the order it was in originally
    'water': ('files/ExplainYourReportSelection_WaterResources.pdf',
              'Water Resources Management'),
    'agriculture': ('files/ExplainYourReportSelection_Agriculture.pdf',
                    'Agricultural Practices'),
    'economy': ('files/ExplainYourReportSelection_Economic.pdf',
                'Economic Profile'),
    'humanitarian': ('files/ExplainYourReportSelection_Humanitarian.pdf',
                     'Humanitarian Situation'),
    'political': ('files/ExplainYourReportSelection_PoliticalStability.pdf',
                  'Political Vulnerability Profile'),
    'environment': ('files/ExplainYourReportSelection_EnvironmentalHealth.pdf',
                    'Environmental Health'),
    'disasters': ('files/ExplainYourReportSelection_NaturalDisasters.pdf',
                  'Natural Disasters'),
    'population': ('files/ExplainYourReportSelection_Population.pdf',
                   'Population'),
    'wildlife': ('files/ExplainYourReportSelection_Wildlife.pdf', 'Wildlife'),
    'governance': (
        'files/ExplainYourReportSelection_EnvironmentalGovernance.pdf',
        'Environmental Governance'),
    'forest': ('files/ExplainYourReportSelection_ForestResources.pdf',
               'Forest Resources'),
}


class ObtainAdditionalInformation(GameInterface):

    def pages(self):
        return ('index', 'page2')

    def template(self, page_id=None, public_state=None):
        game_context = {'pdfs': pdfs}
        if page_id == "page2":
            return ('obtain_additional_information/index.html', game_context)
        if page_id in pdfs:
            path = InstalledGames.absolute_path(
                "envirocon.obtain_additional_information",
                pdfs[page_id][0])
            file_handle = open(path, "rb")
            response = HttpResponse(mimetype='application/pdf')
            response['Content-Disposition'] = \
                'attachment; filename=country_%s.pdf' % page_id
            response.write(file_handle.read())

            return ('file', response)

        # default first page
        return ('obtain_additional_information/intro.html', game_context)

    def variables(self, page_id=None):
        return ['additional_information']

    def public_variables(self):
        return ['additional_information']

    def resources(self, game_state, onopen=False, onclosed=False):
        if onclosed and 'additional_information' in game_state:
            return [{'page_id': report,
                     'type': 'file',
                     'title': '%s.pdf' % pdfs[report][1]}
                    for report in game_state['additional_information']]

        return []
InstalledGames.register_game('obtain_additional_information',
                             'Obtain Additional Information',
                             ObtainAdditionalInformation())
