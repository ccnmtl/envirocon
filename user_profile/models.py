from django.db import models
from django.db.models.loading import get_model
import simplejson as json

User = get_model('auth', 'User')

class UserProfile(models.Model):
    user = models.ForeignKey(User, primary_key=True)

    #json blobs are awesome!
    profile_info = models.TextField(blank=True)

    class Meta:
        permissions = (
            ('view_other_profiles','Can view user profiles'),
            ('edit_own_profile','Can create and edit their own profile'),
            )
        
    def save(self,*args, **kwargs):
        #will raise ValueError
        json.loads(self.profile_info)
        if kwargs.has_key('profile_info'):
            json.loads(kwargs['profile_info'])

        super(UserProfile, self).save(*args, **kwargs)
