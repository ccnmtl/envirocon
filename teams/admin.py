from teams.models import *
from django.contrib import admin

class TeamAdmin(admin.ModelAdmin):
    fields = ['course','name']

admin.site.register(Team, TeamAdmin)
