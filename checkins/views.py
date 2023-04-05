from rest_framework import generics
from rest_framework.views import Response, status

from checkins import models, serializers
from checkins.permissions import RespondentOnly
from checkins.services import (
    serialize_answers_to_list,
    create_checkin_for_user,
    create_answers_for_daily_checkin,
)


class QuestionsListAPiView(generics.ListAPIView):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer


class AnswersListAPiView(generics.ListAPIView):
    serializer_class = serializers.AnswerReadOnlySerializer

    def get_queryset(self):
        return models.Answer.objects.filter(checkin__user=self.request.user)


class AnswerDetailUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = models.Answer.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "answer_id"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.AnswerReadOnlySerializer
        return serializers.AnswerUpdateSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return super().get_permissions()
        return [RespondentOnly()]


class CheckinsListAPiView(generics.ListCreateAPIView):
    serializer_class = serializers.CheckinListSerializer

    def get_queryset(self):
        return models.Checkin.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        valid_answers = serialize_answers_to_list(
            request.data, serializers.AnswerCreateSerializer
        )
        checkin = create_checkin_for_user(
            user=request.user,
            serializer=self.serializer_class,
            answers_list=valid_answers,
        )
        return Response(data=checkin, status=status.HTTP_201_CREATED)
