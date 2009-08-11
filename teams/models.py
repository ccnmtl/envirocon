from django.db import models

Course = models.get_model('courseaffils','course')
Group = models.get_model('auth','group')

class TeamManager(models.Manager):
    def by_user(self, user, course=None):
        try:
            kw = {'group__user__pk':user.pk}
            if course:
                kw['course__pk'] = course.pk
            return Team.objects.get(**kw)
        except Team.DoesNotExist:
            return None
        
    def by_request(self, request):
        c = getattr(request,'actual_course_object',None)
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
        #so we have a 1,2,3,4, etc ref
        order_with_respect_to = 'course'

    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        #auto-create group
        if self.group_id is None:
            group_name = ['Team %d: ' % (Team.objects.count()+1) ]
            if self.course_id:
                group_name.append(self.course.title)
            if self.name:
                group_name.append(self.name)
            self.group = Group.objects.create(name=' - '.join(group_name))
            
        return super(Team, self).save(*args, **kwargs)

    def index(self):
        #if not (hasattr(self,'Meta') \
        #        and hasattr(self.Meta,'order_with_respect_to')):
        #    return None
        ordered_wrt = self._meta.order_with_respect_to.name
        #even more generic
        #peers = getattr(getattr(self,ordered_wrt),
        #                'get_%s_order'%self.__class__.__name__.lower()
        #                )()
        teams = getattr(self,ordered_wrt).get_team_order()
        if teams:
            return 1+teams.index(self.id)
        else:
            return 1
