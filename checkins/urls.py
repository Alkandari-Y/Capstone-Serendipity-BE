from django.urls import path
from checkins import views 


urlpatterns = [
    path('wellness-check/questions/', views.QuestionsListAPiView.as_view(), name="api_questions_list"),
    path('wellness-check/answers/', views.AnswersListAPiView.as_view(), name="api_questions_list"),
    path('wellness-check/checkins/', views.CheckinsListAPiView.as_view(), name="api_questions_list"),

]