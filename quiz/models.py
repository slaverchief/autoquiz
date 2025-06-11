from django.db import models

from authsys.models import CustomUser

# модель конкретного тестирования
class Quiz(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users_passed = models.ManyToManyField(CustomUser, related_name="tests_passed", blank=True) # пользователи, завершившие тест

    def __str__(self):
        return self.name

# модель конкретного варианта выбора вопросе
class Choice(models.Model):
    text = models.CharField(max_length=155)
    is_correct = models.BooleanField(default=False) # флаг, обозначающий, является ли вариант ответа правильным
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="choices")

    def __str__(self):
        return self.text

# модель конкретного вопроса
class Question(models.Model):
    content = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    type = models.PositiveSmallIntegerField(default=1) # тип вопроса представлен малым интом

    def __str__(self):
        return self.content

# модель конкретного ответа на вопрос
class QuestionUser(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="answers")
    answers = models.ManyToManyField("Choice") # ответы, выбранные пользователем

    class Meta:
        unique_together = ('question', 'user')

