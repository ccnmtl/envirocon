from django.db import models

Course = models.get_model('courseaffils', 'course')
Group = models.get_model('auth', 'group')


class TeamManager(models.Manager):

    def by_user(self, user, course=None):
        try:
            if user.is_anonymous():
                return None
            kw = {'group__user__pk': user.pk}
            if course:
                kw['course__pk'] = course.pk
            return Team.objects.get(**kw)
        except Team.DoesNotExist:
            return None

    def by_request(self, request):
        c = getattr(request, 'course', None)
        if c:
            try:
                return Team.objects.get(
                    group__user__pk=request.user.pk,
                    course__pk=c.pk
                )
            except Team.DoesNotExist:
                return None
        return None


class Team(models.Model):
    course = models.ForeignKey(Course)

    group = models.OneToOneField(Group)
    name = models.CharField(max_length=64)

    objects = TeamManager()

    class Meta:
        # so we have a 1,2,3,4, etc ref
        order_with_respect_to = 'course'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # auto-create group
        # TODO: to avoid team removal (without group removal)
        # try name for group and catch it with something alt name
        if self.group_id is None:
            group_name = ['Team %d: ' % (Team.objects.filter(
                course=self.course_id).count() + 1)]
            if self.course_id:
                group_name.append(self.course.title)
            if self.name:
                group_name.append(self.name)
            group_name_string = ' - '.join(group_name)
            extra = ''
            while True:
                self.group, created = Group.objects.get_or_create(
                    name=group_name_string + extra)
                if created:
                    break
                else:
                    if not extra:
                        extra = 'a'
                    extra = chr(ord(extra) + 1)
            if not self.name:
                self.name = self.group.name

        return super(Team, self).save(*args, **kwargs)

    def index(self):
        # if not (hasattr(self,'Meta') \
        #        and hasattr(self.Meta,'order_with_respect_to')):
        #    return None
        ordered_wrt = self._meta.order_with_respect_to.name
        # even more generic
        # peers = getattr(getattr(self,ordered_wrt),
        #                'get_%s_order'%self.__class__.__name__.lower()
        #                )()
        teams = getattr(self, ordered_wrt).get_team_order()
        if teams:
            return 1 + teams.index(self.id)
        else:
            return 1
