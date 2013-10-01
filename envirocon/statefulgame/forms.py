from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminSplitDateTime
from django.core.urlresolvers import reverse
from envirocon.statefulgame.models import Assignment


class BasicAssignmentForm(forms.ModelForm):
    close_date = forms.DateTimeField(widget=AdminSplitDateTime)

    class Meta:
        model = Assignment
        fields = ('close_date', 'open')

    css = {'all': ['%s%s' % (settings.STATIC_URL, url) for url in
                  [  # 'css/base.css', #need modules stuff
                   'admin/css/forms.css',
                   ]
                   ]
           }
    js = ['%s%s' % (settings.STATIC_URL, url) for url in
          ['admin/js/jquery.js',
           'admin/js/jquery.init.js',
           'admin/js/core.js',
           'admin/js/admin/RelatedObjectLookups.js',
           'admin/js/getElementsBySelector.js',
           'admin/js/actions.js',
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
