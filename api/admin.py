from django.contrib import admin
from .models.drf import Article
from .models.user.user import User
from .models.user.contestorganizer import ContestOrganizer
from .models.user.participant import Participant
from .models.problem import Problem
from .models.contest import Contest
from .models.forum import Forum, ForumReply


# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'create_date')
    list_filter = ('status',)
    list_per_page = 10


# admin.site.register(Article, ArticleAdmin)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


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


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    pass


@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    pass
