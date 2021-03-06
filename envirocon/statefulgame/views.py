from django.contrib.auth.models import Group, User
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, Http404, HttpResponseForbidden, \
    HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from envirocon.game.views import game
from envirocon.statefulgame.forms import BasicAssignmentForm
from envirocon.statefulgame.models import Assignment, Shock, Turn, \
    SubmissionBackup, Submission, Game, State
from envirocon.teams.models import Team
import csv
import re
import simplejson as json


def assignment_page(request, assignment_id, faculty_view=None,
                    user_id=None, page_id=None):
    assignment = get_object_or_404(
        Assignment, pk=assignment_id,
        game__course=getattr(request, "course", None))
    assignment.auto_close()
    # we can assume request.course from now on
    user = request.user
    faculty_info = None
    if faculty_view and request.course.is_faculty(request.user):
        user = User.objects.get(pk=user_id)
        faculty_info = {'teams': [{'r': team, }
                                  for team in request.course.team_set.all()],
                        'shocks': Shock.objects.all(),
                        #'next_assignment':assignment.get_next_in_order(),
                        }
        if not page_id and 'page2' in assignment.gamepages():
            page_id = 'page2'

    team = Team.objects.by_user(user, getattr(request, "course", None))
    if team is None:
        raise Http404

    if not team.state.resource_access(assignment, page_id, user):
        return HttpResponseForbidden(
            'You do not have access to this activity resource at this time.')
    turn = assignment.turn(team)
    if turn:
        if not faculty_info and not turn.visible:
            return HttpResponseForbidden()
        team.state.world_slice(assignment.gamepublic_variables())
        resources = team.state.resources(user)
        resources_by_app = {}
        for act_meta in resources:  # all resources
            if not act_meta['a'].app in resources_by_app:
                resources_by_app[act_meta['a'].app] = OrderedDict()
            for r in act_meta['res']:  # each resource
                resources_by_app[act_meta['a'].app][r['page_id']] = r
    editable = turn.open and not faculty_info
    world_state = {'duedate': turn.assignment.close_date,
                   'individual': turn.assignment.individual,
                   'turn_id': turn.id,
                   'published': turn.published(user),
                   'editable': editable,
                   'faculty_info': faculty_info,
                   'resources': resources,
                   'resources_by_app': resources_by_app,
                   'team': team,
                   'assignment': assignment,
                   'turn': turn,
                   'user_id': user.id,
                   'submission': assignment.submission(team, user),
                   }

    return game(request, assignment, page_id=page_id,
                extra_world_state=world_state)


def assignment_video(request, assignment_id):
    assignment = get_object_or_404(
        Assignment, pk=assignment_id,
        game__course=getattr(request, "course", None))

    user = request.user

    team = Team.objects.by_user(user, getattr(request, "course", None))
    if team is None:
        raise Http404

    # if not team.state.resource_access(assignment,page_id,user):
    # return HttpResponseForbidden('You do not have access to this activity
    # resource at this time.')

    turn = assignment.turn(team)
    if turn and not turn.visible:
        return HttpResponseForbidden()

    video = assignment.activity_ptr.gamevideo()
    if not video:
        raise Http404

    return render_to_response('game/video.html',
                              {'video': video,
                               'user_id': user.id,
                               },
                              context_instance=RequestContext(request))

# saves an assignment blob to the database


def save_assignment(request):
    data = request.REQUEST.get('data', None)
    try:
        turn_id = request.REQUEST['turn_id']
    except:
        return HttpResponseForbidden()

    turn = Turn.objects.get(id=turn_id)
    turn.assignment.auto_close()

    state = turn.team.state

    SubmissionBackup.objects.create(
        author=request.user,
        turn=turn,
        data=data,
    )

    if not turn.open:
        return HttpResponseForbidden()
    if turn.assignment.individual:
        submission, created = Submission.objects.get_or_create(
            author=request.user, turn=turn)
    else:
        try:
            submission = Submission.objects.get(turn=turn)
            created = False
        except Submission.DoesNotExist:
            submission = Submission(turn=turn, author=request.user)
            created = True
        # save global state if we have public vars
        pubs = turn.assignment.gamepublic_variables()
        world = state.world_ro
        dirty = False
        if data != "":
            for k, v in json.loads(data).items():
                if k in pubs:
                    world.setdefault('app_vars', {})
                    world['app_vars'][k] = v
                    dirty = True
            if dirty:
                state.save_world(world)
    submission.data = data
    submission.author = request.user
    if not request.REQUEST.get('published', 'NO').startswith('Default'):
        submission.published = (
            request.REQUEST.get('published', 'Draft').find('Draft') < 0)
    submission.save()

    video_page = reverse('assignment-video', args=[turn.assignment.id])
    doc = {'created': created, 'redirect':
           video_page if turn.assignment.activity_ptr.gamevideo() else '/'}
    return HttpResponse(json.dumps(doc), 'application/json')


def get_assignment_data(request, turn_id, user_id):
    user = request.user
    is_faculty = request.course.is_faculty(request.user)

    if user_id and is_faculty:
        user = User.objects.get(pk=user_id)

    team = Team.objects.by_user(user, getattr(request, "course", None))

    turn = get_object_or_404(Turn, pk=turn_id, team=team)
    data = team.state.world_slice(turn.assignment.gamepublic_variables())
    try:
        if turn.assignment.individual:
            submission = Submission.objects.get(author=user, turn=turn)
        else:
            submission = Submission.objects.get(turn=turn)
        if submission.data != "":
            data.update(json.loads(submission.data))
    except Submission.DoesNotExist:
        pass
    serialized_data = '{}'
    if data:
        serialized_data = json.dumps(data)
    protected_data = False
    if is_faculty:
        protected_data = turn.assignment.gameconsequences(data)

    if "jsonp" in request.GET:
        return HttpResponse("%s(%s,%s)" % (request.GET["jsonp"],
                                           serialized_data,
                                           json.dumps(protected_data)))
    return HttpResponse(serialized_data)


def de_html(maybe_string):
    if not isinstance(maybe_string, unicode):
        return maybe_string  # not string
    # avoiding entities, we could probably use a library for fancier stuff
    # remove tags naively
    return re.sub('<[/\w][^>]*>', '', maybe_string).encode("utf-8")

# helper function for get_assignment_csv


def format_data(data):
    formatted = {}
    filter_list = ["published", "turn_id", "author"]

    app_key = data.keys()[0]
    app_data = data[app_key]

    # dictionary stored
    if isinstance(app_data, dict):
        for key in app_data.keys():
            if key not in filter_list:
                formatted[key] = de_html(app_data[key])

    else:
        formatted[app_key] = de_html(app_data)

    return formatted


def get_assignment_csv(request, assignment_id):
    if not request.course.is_faculty(request.user):
        return HttpResponseForbidden()

    assignment = Assignment.objects.get(pk=assignment_id)
    course = request.course

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = \
        'attachment; filename="%s.csv"' % assignment.name
    writer = csv.writer(response)  # ,quoting=csv.QUOTE_NONNUMERIC)

    headers = []
    rows = []

    if assignment.individual:
        default_headers = ["UNI", "Full Name"]
        headers = default_headers[:]

        for student in course.students:
            team = Team.objects.by_user(student, course)
            # ignore students who have not been assigned to a team
            if not team:
                continue

            turn = Turn.objects.get(team=team, assignment=assignment)
            row = [student, student.get_full_name()]
            data = {}
            try:
                sub = Submission.objects.get(author=student, turn=turn)
                data = json.loads(sub.data)

            except (Submission.DoesNotExist, ValueError):
                row.append("Nothing submitted.")

            if data:
                formatted = format_data(data)

                for header in formatted.keys():
                    if header not in headers:
                        headers.append(header)

                # add to row -- being careful of order (so headers match data)
                for header in headers:
                    try:
                        row.append(formatted[header])
                    except:
                        if header not in default_headers:
                            row.append("")

            rows.append(row)

    else:  # group assignment
        default_headers = ["Team", "Team Members"]
        headers = default_headers[:]

        for team in course.team_set.all():
            try:
                group = Group.objects.get(name=team.name)
            except Group.DoesNotExist:
                continue
            members = ', '.join(["%s (%s)" % (member, member.get_full_name())
                                for member in group.user_set.all()])
            turn = Turn.objects.get(team=team, assignment=assignment)
            row = [team.name, members]
            data = {}

            try:
                sub = Submission.objects.get(turn=turn)
                data = json.loads(sub.data)

            except (Submission.DoesNotExist, ValueError):
                row.append("Nothing submitted.")

            if data:
                formatted = format_data(data)

                for header in formatted.keys():
                    if header not in headers:
                        headers.append(header)

                # add to row -- being careful of order (so headers match data)
                for header in headers:
                    try:
                        row.append(formatted[header])
                    except:
                        if header not in default_headers:
                            row.append("")

            rows.append(row)

    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)

    return response


def current_turn(request):
    user = request.user
    team = Team.objects.by_user(user, getattr(request, "course", None))
    if not team:
        return HttpResponseRedirect('/')
    turn = team.state.current_turn()

    if turn:
        return HttpResponseRedirect(reverse("assignment-page",
                                            args=[turn.assignment.id]))
    else:
        return HttpResponseRedirect('/?message=no+activity+ready')


def faculty_view(request, game_id=None):
    """
    list assignments (change due dates/ open|close)
    see teams:
      set turn (manually) per-team
         AND globally (through assignments list above)

    """
    if request.user not in request.course.faculty \
            and not request.user.is_staff:
        return HttpResponseForbidden()

    game = None
    if game_id:
        game = get_object_or_404(Game, pk=game_id, course=request.course)
    else:
        game = Game.objects.filter(course=request.course)[0]

    if request.method == 'POST':
        pass

    return render_to_response('statefulgame/faculty_view.html',
                              {'course': request.course,
                               'game': game,
                               },
                              context_instance=RequestContext(request))


def faculty_assignment_review(request):
    """
    view assignments

    """
    data = {}
    if request.user.is_staff or request.user in request.course.faculty:
        data['assignments'] = Assignment.objects.filter(
            game__course=request.course)
    return render_to_response('statefulgame/faculty_view.html',
                              {'course': request.course,
                               'game': game,
                               },
                              context_instance=RequestContext(request))


def team_view_data(request, teams=None, game=None):
    """
    past assignments (with title,status,shock)

    """
    just_advanced = False
    is_faculty = (request.user in request.course.faculty)
    AssignmentFormSet = inlineformset_factory(Game, Assignment,
                                              can_delete=False,
                                              form=BasicAssignmentForm,
                                              extra=0)

    if game is None:
        games = request.course.game_set.all()
        if not games:
            return {}
        else:
            game = games[0]

    team = Team.objects.by_user(request.user, getattr(request, 'course', None))
    teams = []
    if is_faculty:
        teams = Team.objects.filter(course=getattr(request, 'course', None))
        if request.method == 'POST':
            post_forms = AssignmentFormSet(
                request.POST, request.FILES, instance=game)
            if post_forms.is_valid():
                post_forms.save()
    else:
        if team:
            teams = [team]

    for tm in teams:
        just_advanced = (
            State.objects.get(team=tm).advance_turn() or just_advanced)

    assignment_forms = AssignmentFormSet(instance=game)

    assignments = [{'auto_closed': f.instance.auto_close(),
                    'data': f.instance,
                    'form': f,
                    'teams': [], 'hidden': True, 'current': False, }
                   for f in assignment_forms.forms]

    for tm in teams:
        for d in assignments:
            turn = d['data'].turn(tm)
            if turn.visible:
                d['hidden'] = False
            if tm == team:
                if turn == tm.state.turn and turn.open:
                    d['current'] = True
                d['my_submission'] = d['data'].submission(team, request.user)
            d['teams'].append({
                'turn': turn,
                'data': tm,
                'sub': d['data'].submission(tm, request.user, is_faculty)})
    return {'teams': teams,
            'assignments': assignments,
            'is_faculty': is_faculty,
            'formset': assignment_forms,
            'team': team,  # user's team (implies a student)
            'just_advanced': just_advanced,
            }


def split_team(request):
    """divide a team into two new teams"""
    if not request.user.is_staff:
        return HttpResponseForbidden('Only staff can split a team.')
    if request.method == "POST":
        old_team = get_object_or_404(
            Team, pk=request.POST['team_id'], course=request.course)
        splitter = get_object_or_404(User, username=request.POST['splitter'])

        new_team = Team.objects.create(course=request.course)
        old_team.group.user_set.remove(splitter)
        new_team.group.user_set.add(splitter)

        # duplicate shocks, state, submissions,
        for old_turn in old_team.turn_set.all():
            new_turn = Turn.objects.get(
                team=new_team, assignment=old_turn.assignment)
            new_turn.shock = old_turn.shock
            new_turn.save()

            if old_turn.assignment.individual:
                old_turn.submission_set.filter(
                    author=splitter).update(turn=new_turn)
            else:  # probably just one
                for sub in old_turn.submission_set.all():
                    sub.id = None
                    sub.turn = new_turn
                    sub.save(force_insert=True)

        new_state = State.objects.get(team=new_team)
        new_state.world_state = old_team.state.world_state
        new_state.turn = Turn.objects.get(
            team=new_team, assignment=old_team.state.turn.assignment)
        new_state.save()
        return HttpResponseRedirect('/')
    else:
        return render_to_response('statefulgame/split_team.html',
                                  {'course': request.course,
                                   'game': game,
                                   },
                                  context_instance=RequestContext(request))


def set_turn(request):
    """team_id,assignment_id,shock_id
    OR team_id,assignment_id,shock_name,shock_outcome
    """
    if request.method == 'POST' and request.course.is_faculty(request.user):
        team = get_object_or_404(
            Team, pk=request.POST['team_id'], course=request.course)
        assignment = get_object_or_404(
            Assignment, pk=request.POST['assignment_id'],
            game__course=request.course)
        turn = assignment.turn(team)
        # no has_key here because shock_id could equal ''
        if (request.POST.get('shock_id', False) or
                'shock_name' in request.POST):
            if request.POST.get('shock_id', False):
                if request.POST['shock_id'] == 'none':
                    shock = None
                else:
                    shock = get_object_or_404(
                        Shock, pk=request.POST['shock_id'])
            else:
                shock = Shock.objects.create(
                    name=request.POST['shock_name'],
                    outcome=request.POST['shock_outcome'])
            turn.shock = shock
            turn.save()
            return HttpResponse(shock)
        elif request.POST.get('set_turn', False):
            team.state.turn = turn
            team.state.save()
            # would auto-advance, so make them drafts
            if turn.complete() and turn.next() and turn.next().assignment.open:
                # we do it to all subs, so if we push back to an
                # individual assn all the team members are equally fsck'd
                subs = Submission.objects.filter(turn=turn, archival=False)
                for sub in subs:
                    sub.published = False
                    sub.save()

            return HttpResponse(turn.id)


class OrderedDict:
    # mostly
    # if you set it here, it'll be the SAME DAMN DICT FOR ALL
    dic = None
    array = None

    def __init__(self):
        self.dic = {}
        self.array = []

    def __getitem__(self, key):
        return self.dic[key]

    def __setitem__(self, key, val):
        if key in self.dic:
            self.dic[key] = val
        else:
            self.array.append(key)
            self.dic[key] = val

    def has_key(self, key):
        if key in self.dic:
            return True
        return False

    def values(self):
        return [self.dic[k] for k in self.array]

    def items(self):
        return [(k, self.dic[k]) for k in self.array]
