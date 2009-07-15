# Create your views here.
from django.template import RequestContext, loader
from django.http import HttpResponse

from game.models import *


#CUSTOM CONTEXT PROCESSOR
#see/set TEMPLATE_CONTEXT_PROCESSORS in settings_shared.py
#also note that we need RequestContext instead of the usual Context
def relative_root(request):
    """returns a string like '../../../' to get back to the root level"""
    from_top = request.path.count('/')-1
    relative_root_path = '../' * from_top
    return {'relative_root':relative_root_path,
            'GAME_MEDIA': relative_root_path + 'site_media/'
            }

def game(request, game, page_id=None):
    game.page_id = page_id #for easy access in template
    
    template,game_context = game.template(page_id)
    
    t = loader.get_template(template)
    c = RequestContext(request,{
        'game' :  game,
        'game_context' : game_context,
    })
    return HttpResponse(t.render(c))
