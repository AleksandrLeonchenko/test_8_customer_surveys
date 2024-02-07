from django.urls import path
from django.contrib.auth import views as auth_views

from .api import (
    SurveyView,
    NumberRespondents,
    NumberAnswers,
    OrderingQuestions,
    ResponseRate,
    SurveyStatistics,
)
from .views import RegisterUserView, HomeView


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='survey/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='register'), name='logout'),
    path('survey/<int:pk>/', SurveyView.as_view(), name='survey_view'),
    path('survey/<int:pk>/respondents/', NumberRespondents.as_view(), name='number_respondents'),
    path('survey/<int:survey_id>/statistics/', SurveyStatistics.as_view(), name='survey_statistics'),
    path('survey/<int:survey_id>/respondents/<int:question_id>/', NumberAnswers.as_view(), name='number_respondents'),
    path('survey/<int:survey_id>/ordering/', OrderingQuestions.as_view(), name='surveys_ordering'),
    path('survey/<int:survey_id>/response_rate/<int:question_id>/', ResponseRate.as_view(), name='response_rate'),
]
