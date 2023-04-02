from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from checkins import models, serializers
from checkins.permissions import RespondentOnly


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


class CheckinsListAPiView(generics.ListAPIView):
    serializer_class = serializers.CheckinListSerializer

    def get_queryset(self):
        return models.Checkin.objects.filter(user=self.request.user)
