from django.contrib import admin
from envirocon.statefulgame.models import Game, Assignment, Shock, Turn, \
    State, Submission, SubmissionBackup

admin.site.register(Game)
admin.site.register(Assignment)
admin.site.register(Shock)
admin.site.register(Turn)
admin.site.register(State)
admin.site.register(Submission)
admin.site.register(SubmissionBackup)
