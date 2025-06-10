from rest_framework import serializers
from .models import *
from rest_framework.fields import empty

class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ("id", "text")

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        exclude = ['quiz']

class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = '__all__'

class QuestionUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionUser
        exclude = ['user']