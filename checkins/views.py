from rest_framework import generics

from checkins import models, serializers
class QuestionsListAPiView(generics.ListAPIView):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer


class AnswersListAPiView(generics.ListAPIView):
    serializer_class = serializers.AnswerReadOnlySerializer

    def get_queryset(self):
        return models.Answer.objects.filter(checkin__user=self.request.user)


class CheckinsListAPiView(generics.ListAPIView):
    serializer_class = serializers.CheckinListSerializer

    def get_queryset(self):
        return models.Checkin.objects.filter(user=self.request.user)