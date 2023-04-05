from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Question(models.Model):
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question[:20]


class Checkin(models.Model):
    class Meta:
        unique_together = (
            "user",
            "created_at",
        )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="checkins")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Checkin ID {self.pk}"


class Answer(models.Model):
    class Meta:
        unique_together = (
            "checkin",
            "question",
        )

    checkin = models.ForeignKey(
        Checkin, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    answer = models.CharField(max_length=255)

    @property
    def user(self):
        return self.checkin.user

    def __str__(self):
        return f"Answer ID {self.pk} - {self.user}"
