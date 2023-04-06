from rest_framework.views import status
from django.db import IntegrityError
from rest_framework.serializers import ValidationError

from datetime import  date

from checkins import models


def serialize_answers_to_list(answers_list, serializer):
    if len(answers_list) == 0:
        raise ValidationError(
                detail={
                    "Answer": [
                        f"No answers created!"
                    ]
                },
                code=status.HTTP_400_BAD_REQUEST,
            )
    return [
        answer_serializer
        for answer in answers_list
        if (answer_serializer := serializer(data=answer)).is_valid(raise_exception=True)
    ]


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


def create_checkin_for_user(user, serializer=None, answers_list=None):
    try:
        checkin = models.Checkin.objects.create(user=user, created_at=date.today())
    except IntegrityError as e:
        if "checkins_checkin.created_at" in str(e):
            raise ValidationError(
                detail={"checkin": ["Daily checkin limit reached!"]},
                code=status.HTTP_400_BAD_REQUEST,
            )
    if answers_list is not None:
        create_answers_for_daily_checkin(checkin, answers_list)
    if serializer is not None:
        return serializer(instance=checkin).data
