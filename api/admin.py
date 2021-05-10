from django.contrib import admin
from .models.user.user import User
from .models.user.contestorganizer import ContestOrganizer
from .models.user.participant import Participant
from .models.problem import Problem
from .models.contest import Contest, ContestInfoResult
from .models.forum import Forum, ForumReply


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'is_p', 'is_oc', 'is_admin']
    list_filter = ('is_p', 'is_oc', 'is_admin')


@admin.register(ContestOrganizer)
class ContestOrganizerAdmin(admin.ModelAdmin):
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
    list_display = ['contest', 'user', 'ranking', 'pass_problem']
    list_filter = ('contest', 'user', 'ranking')


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author']
    list_filter = ('author',)


@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    pass
