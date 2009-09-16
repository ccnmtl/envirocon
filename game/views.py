# Create your views here.
from django.template import RequestContext, loader
from django.http import HttpResponse,Http404
from django.conf import settings

from game.models import *
from game import signals as game_signals

# TODO this does not belong here...
Team = models.get_model('teams','team')
import simplejson as json

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

def gamelist(request):
    pass

def gamepage(request, gamename, page_id=None):
    if gamename not in Activity.gamechoices():
        raise Http404
    activity = Activity.objects.create(app=gamename)
    return game(request, activity, page_id)

def game(request, activity, page_id=None, first_time=True):
    activity.page_id = page_id #for easy access in template
    
    world_state = dict()
    for func,dict_val in game_signals.world_state.send(sender=activity,
                                                       request=request):
        for key in dict_val:
            world_state[key] = dict_val[key]

    #for k in activity.gamepublic_variables():
    #TODO: filter world_state for feeding into gametemplate
    # or maybe this is done by statefulgame
    
    template,game_context = activity.gametemplate(page_id,world_state)
    # bit-of-a-hack: "file" is returned when the app will complete the whole request
    if template == "file":
      return game_context


    t = loader.get_template(template)
    c = RequestContext(request,{
        'game' :  activity,
        'game_context' : game_context,
        'world_state' : world_state,
        #probably should query this from urls or something
        'GAME_MEDIA' : "%s/%s/" % (getattr(settings,'GAME_MEDIA',
                                           '/site_media'),
                                   activity.app),
    })
    #print c
    return HttpResponse(t.render(c))
