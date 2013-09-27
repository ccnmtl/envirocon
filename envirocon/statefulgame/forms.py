from django import forms
from django.db import models
from django.contrib.admin.widgets import AdminSplitDateTime
from django.core.urlresolvers import reverse
from django.conf import settings

from envirocon.statefulgame.models import *


class BasicAssignmentForm(forms.ModelForm):
    close_date = forms.DateTimeField(widget=AdminSplitDateTime)

    class Meta:
        model = Assignment
        fields = ('close_date', 'open')

    css = {'all': ['%s%s' % (settings.ADMIN_MEDIA_PREFIX, url) for url in
                  [  # 'css/base.css', #need modules stuff
                   'css/forms.css',
                   ]
                   ]
           }
    js = ['%s%s' % (settings.ADMIN_MEDIA_PREFIX, url) for url in
          ['js/core.js',
           'js/admin/RelatedObjectLookups.js',
           'js/getElementsBySelector.js',
           'js/actions.js',
           ]
          ]

    @property
    def media(self):
        media = forms.Media(js=self.js, css=self.css)
        media.add_js([reverse('jsi18n')])
        # copied from django.forms.forms
        for field in self.fields.values():
            media = media + field.widget.media
        return media
