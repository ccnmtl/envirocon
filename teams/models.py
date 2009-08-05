from django.db import models

Course = models.get_model('courseaffils','course')
Group = models.get_model('auth','group')

class Team(models.Model):
    course = models.ForeignKey(Course)
    
    group = models.OneToOneField(Group)
    name = models.CharField(max_length=64)

    class Meta:
        #so we have a 1,2,3,4, etc ref
        order_with_respect_to = 'course'

    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        #auto-create group
        if self.group_id is None:
            group_name = ['Team: ']
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
        ordered_wrt = self.Meta.order_with_respect_to
        #even more generic
        #peers = getattr(getattr(self,ordered_wrt),
        #                'get_%s_order'%self.__class__.__name__.lower()
        #                )()
        teams = getattr(self,ordered_wrt).get_team_order()
        if teams:
            return 1+teams.index(self.id)
        else:
            return 1
