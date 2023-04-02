from rest_framework import serializers

from checkins import models

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = "__all__"

class AnswerReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = "__all__"
    
    question = QuestionSerializer(read_only=True)

class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = "__all__"
    

class CheckinListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Checkin
        fields = ["id", "date", "answers"]
    
    answers = AnswerReadOnlySerializer(many=True, read_only=True)