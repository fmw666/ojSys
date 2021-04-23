from django.contrib import admin
from .models.drf import Article
from .models.users import CompetitionOrganizer, User, Participant
from .models.problem import Problem


# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'create_date')
    list_filter = ('status',)
    list_per_page = 10


# admin.site.register(Article, ArticleAdmin)


# 用户类
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


# 竞赛组织者
@admin.register(CompetitionOrganizer)
class CompetitionOrganizerAdmin(admin.ModelAdmin):
    pass


# 普通用户
@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    pass


# 列题
@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'create_date', 'ds_type', 'alg_type']
    list_filter = ('author', 'ds_type', 'alg_type')

