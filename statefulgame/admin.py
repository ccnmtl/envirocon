from statefulgame.models import *
from django.contrib import admin

#class AssignmentAdmin(admin.ModelAdmin):
#    fields = ['course','name']

admin.site.register(Game)
admin.site.register(Assignment)
admin.site.register(Shock)
