from statefulgame.models import *
from django.contrib import admin

#class AssignmentAdmin(admin.ModelAdmin):
#    fields = ['course','name']

admin.site.register(Game)
admin.site.register(Assignment)
admin.site.register(Shock)
admin.site.register(Turn)
admin.site.register(State)
admin.site.register(Submission)
admin.site.register(SubmissionBackup)
