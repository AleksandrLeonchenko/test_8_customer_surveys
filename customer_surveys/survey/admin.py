from django.contrib import admin
from .models import Survey, Question, Answer, AnswerGroup, UserStatistics


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title',)
    filter_horizontal = ('participants', 'questions',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'answer_group', 'parent_question')
    list_display_links = ('id', 'text', 'answer_group', 'parent_question')
    list_filter = ('id', 'text', 'answer_group', 'parent_question')
    search_fields = ('text',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'question', 'group', 'next_question', 'number_answer')
    list_display_links = ('id', 'text', 'question', 'group', 'next_question', 'number_answer')
    list_filter = ('id', 'text', 'question', 'group', 'next_question', 'number_answer')
    search_fields = ('text', 'survey__title', 'question__text')


@admin.register(AnswerGroup)
class AnswerGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(UserStatistics)
class UserStatisticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'survey', 'answers_given', 'questions_answered', 'timestamp')
    list_display_links = ('id', 'user', 'survey', 'answers_given', 'questions_answered', 'timestamp')
    list_filter = ('id', 'user', 'survey')
    search_fields = ('id', 'user', 'survey')
