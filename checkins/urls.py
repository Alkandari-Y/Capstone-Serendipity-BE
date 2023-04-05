from django.urls import path
from checkins import views


urlpatterns = [
    path(
        "wellness-check/questions/",
        views.QuestionsListAPiView.as_view(),
        name="api_questions_list",
    ),
    path(
        "wellness-check/answers/",
        views.AnswersListAPiView.as_view(),
        name="api_answers_list",
    ),
    path(
        "wellness-check/answers/<int:answer_id>/",
        views.AnswerDetailUpdateAPIView.as_view(),
        name="api_answer_detail_edit",
    ),
    path(
        "wellness-check/checkins/",
        views.CheckinsListAPiView.as_view(),
        name="api_checkins_list",
    ),
    path(
        "wellness-check/feelings/",
        views.FeelingAPIView.as_view(),
        name="api_feelings_stats",
    ),
    path(
        "wellness-check/wellness-check/feeling-options//",
        views.FeelingTypesAPIView.as_view(),
        name="api_feelings_stats",
    ),
]
