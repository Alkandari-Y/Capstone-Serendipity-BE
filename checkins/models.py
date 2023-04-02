from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Question(models.Model):
    question = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id}: {self.question[:10]}"

class Checkin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="checkins")
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.date}: {self.user.username}" # type: ignore

class Answer(models.Model):
    class Meta:
        unique_together = ('checkin', 'question',)

    checkin = models.ForeignKey(Checkin, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer = models.CharField(max_length=255)

    
    def __str__(self):
        return f"{self.checkin.date}: {self.question.__str__()}"