from django.conf.urls import patterns, url


urlpatterns = patterns(
    'envirocon.teams.views',
    url(r'^admin$',
        'team_admin',
        name='team-admin'),

    url(r'^create/(?P<course_id>\w+)?/?$',
        'addteam',
        name='team-create'),
    url(r'^delete/(?P<team_id>\w+)/$',
        'deleteteam',
        name='team-delete'),

    url(r'^member/(?P<user_id>\w+)/(?P<team_id>\w+)?(/(?P<course_id>\w+))?/?$',
        'addmember',
        name='team-addmember'),
)
