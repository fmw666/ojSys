from django.contrib import admin
from .models.drf import Article
from .models.users import CompetitionOrganizer, User, Participant
from .models.problem import Problem
from .models.context import Context


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


@admin.register(CompetitionOrganizer)
class CompetitionOrganizerAdmin(admin.ModelAdmin):
    pass


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    pass


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'header', 'ds_type', 'alg_type', 'author', 'public', 'create_date']
    list_filter = ('author', 'header', 'ds_type', 'alg_type')


@admin.register(Context)
class ContextAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'create_date']
    list_filter = ('author',)
