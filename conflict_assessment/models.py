from django.db import models
from django.http import HttpResponse
import os.path

# Create your models here.
from game.installed_games import InstalledGames,GameInterface

class ConflictAssessment(GameInterface):
    def pages(self):
        return ('index',)

    def template(self,page_id=None,public_state=None):
        #documents = {"Country Narrative":"country_narrative.pdf"}
        game_context = {'sampledata':"hello"}#, documents:documents}
        # register documents for game
        #self.register_documents({"Country Narrative": "{{
        if page_id == "country_narrative2":
          # instead of serving the file directly, open it and pipe it over (for security)
          path = os.path.abspath(".") + "/conflict_assessment/files/country_narrative.pdf"
          file = open(path,"rb")
          response = HttpResponse(mimetype='application/pdf')
          response['Content-Disposition'] = 'attachment; filename=country_narrative.pdf'
          response.write(file.read())
          
          return ('file',response)

        if page_id == "country_narrative":
          return ('conflict_assessment/narrative.html',game_context)

        return ('conflict_assessment/index.html',game_context)
    
    def variables(self,page_id=None):
        return ['conflict_assessment']
        
    #def register_documents(self,state,document_name,document_url):
        #document_list = state.world_state["documents"]
        #document_list.append("%s:%s", (document_name, document_url)
    #    pass

InstalledGames.register_game('conflict_assessment',
                             'Conflict Assessment',
                             ConflictAssessment() )
