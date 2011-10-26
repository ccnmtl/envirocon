from teams.models import *
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

# set up in/out widget for the admin section
UserAdmin.filter_horizontal = ('user_permissions', 'groups')

class TeamAdmin(admin.ModelAdmin):
    fields = ['course','name']

admin.site.register(Team, TeamAdmin)
