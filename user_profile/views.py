from django.http import Http403
from django.db.models.loading import get_model
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

UserProfile = get_model('user_profile','UserProfile')
User = get_model('auth','User')

def profile(request,user_id=None):
    user = request.user
    if request.method =='POST' \
           and not user.is_anonymous() \
           and user.has_perm('user_profile.edit_own_profile'):
        if request.POST.has_key('profile_info'):
            profile_info = request.POST.get('profile_info','{}')
        
            profile = UserProfile.object.get(user=user)
            if not profile:
                profile = UserProfile.objects.create(user=user,
                                                     profile_info=profile_info,
                                                     )
            else:
                profile.profile_info = profile_info
                profile.save()
            
        user_info = {} #saved on User record
        if request.POST.has_key('first_name'):
            user_info['first_name'] = request.POST['first_name']
        if request.POST.has_key('last_name'):
            user_info['last_name'] = request.POST['last_name']
        if request.POST.has_key('email'):
            user_info['email'] = request.POST['email']
            
        if user_info:
            request.user.save(**user_info)
        
    else:
        template = 'user_profile.profile.html'
        if user_id==request.user.id or request.user.has_perm('user_profile.view_other_profiles'):
            if user_id==request.user.id:
                template = 'user_profile.profileform.html'
            if user_id:
                user = get_object_or_404(User, pk=user_id)
            profile = UserProfile.objects.get(user=user)
        else:
            raise Http403('Forbidden')

    return render_to_response(template,
                              {'user':user,
                               'profile':profile,
                               },
                              context_instance=RequestContext(request))

