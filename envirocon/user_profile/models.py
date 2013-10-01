from django.contrib.auth.models import User
from django.db import models
import simplejson as json


class UserProfile(models.Model):
    user = models.ForeignKey(User, primary_key=True)

    # json blobs are awesome!
    profile_info = models.TextField(blank=True)

    class Meta:
        permissions = (
            ('view_other_profiles', 'Can view user profiles'),
            ('edit_own_profile', 'Can create and edit their own profile'),
        )

    def save(self, *args, **kwargs):
        # will raise ValueError
        json.loads(self.profile_info)
        if 'profile_info' in kwargs:
            json.loads(kwargs['profile_info'])

        super(UserProfile, self).save(*args, **kwargs)
