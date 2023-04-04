from django.db import IntegrityError
from rest_framework import generics
from rest_framework.views import Response, status
from rest_framework.serializers import ValidationError

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


class CheckinsListAPiView(generics.ListCreateAPIView):
    serializer_class = serializers.CheckinListSerializer

    def get_queryset(self):
        return models.Checkin.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        checkin = models.Checkin(user=request.user)
        valid_answers = []

        for data in request.data:
            answer_serializer = serializers.AnswerCreateSerializer(data=data)
            if answer_serializer.is_valid(raise_exception=True):
                valid_answers.append(answer_serializer)

        try:
            checkin.save()
            for answer in valid_answers:
                answer.save(checkin=checkin)
        except IntegrityError as e:
            if "checkins_checkin.date" in str(e):
                raise ValidationError(detail={"checkin":["Daily checkin limit reached"]}, code=status.HTTP_400_BAD_REQUEST)
            elif "checkins_answer" in str(e):
                raise ValidationError(detail={"Answer":["Answers for this question already created for your daily checkin!"]}, code=status.HTTP_400_BAD_REQUEST)

        return Response(
            data=self.serializer_class(checkin).data, status=status.HTTP_201_CREATED
        )