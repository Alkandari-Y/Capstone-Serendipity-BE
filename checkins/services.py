from rest_framework.views import status
from django.db import IntegrityError
from rest_framework.serializers import ValidationError

from checkins import models


def serialize_answers_to_list(answers_list, serializer):
    return [
        answer_serializer
        for answer in answers_list
        if (answer_serializer := serializer(data=answer)).is_valid(raise_exception=True)
    ]


def create_checkin_for_user(user):
    try:
        checkin = models.Checkin.objects.create(user=user)
    except IntegrityError as e:
        if "checkins_checkin.date" in str(e):
            raise ValidationError(
                detail={"checkin": ["Daily checkin limit reached!"]},
                code=status.HTTP_400_BAD_REQUEST,
            )
    return checkin


def create_answers_for_daily_checkin(checkin, answers):
    for answer in answers:
        try:
            answer.save(checkin=checkin)
        except IntegrityError as e:
            raise ValidationError(
                detail={
                    "Answer": [
                        f"An answer for question with id {answer.validated_data['question'].id} already exists for your current daily checkin!"
                    ]
                },
                code=status.HTTP_400_BAD_REQUEST,
            )
