from django.db import models

from authsys.models import CustomUser


class Quiz(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Choice(models.Model):
    text = models.CharField(max_length=155)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Question(models.Model):
    content = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    choices = models.ManyToManyField("Choice", related_name="question")
    type = models.PositiveSmallIntegerField(default=1) # тип вопроса представлен малым интоми

    def __str__(self):
        return self.content

class QuestionUser(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="answers")
    answers = models.ManyToManyField("Choice")