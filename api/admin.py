from django.contrib import admin
from .models.user.user import User
from .models.user.organizer import Organizer
from .models.user.participant import Participant
from .models.problem import Problem
from .models.contest import Contest, ContestInfoResult
from .models.forum import Forum, ForumReply


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'is_p', 'is_o', 'is_admin']
    list_filter = ('is_p', 'is_o', 'is_admin')


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    pass


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    pass


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'header', 'ds_type', 'alg_type', 'author', 'public', 'create_date']
    list_filter = ('author', 'header', 'ds_type', 'alg_type')


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
    list_filter = ('author',)


@admin.register(ContestInfoResult)
class ContestInfoResultAdmin(admin.ModelAdmin):
    list_display = ['contest', 'user', 'spend_time', 'ranking', 'pass_problems_cnt']
    list_filter = ('contest', 'user', 'ranking')

    def pass_problems_cnt(self, obj):
        return obj.pass_problems.count()
    pass_problems_cnt.short_description = '通过题目数'


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author']
    list_filter = ('author',)


@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    pass
