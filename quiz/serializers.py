from rest_framework import serializers
from .models import *

class ChoiceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объекта варианта ответа на вопрос
    """
    class Meta:
        model = Choice
        fields = ("id", "text")

class QuestionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объекта вопроса
    """
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        exclude = ['quiz']

class QuizSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объекта тестирования
    """
    class Meta:
        model = Quiz
        fields = '__all__'
        extra_kwargs = {
            'users_passed': {'write_only': True}
        }


class QuestionUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объекта выбора ответа в вопросе
    """
    class Meta:
        model = QuestionUser
        exclude = ['user', 'id']

class QuizWithAnswersSerializer(serializers.Serializer):
    """
    Сериализатор для тестирования вместе с вариантами ответа на вопросы в тестировании
    """
    quiz = QuizSerializer()
    questions = QuestionUserSerializer(many=True)