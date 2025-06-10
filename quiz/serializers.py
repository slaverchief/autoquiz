from rest_framework import serializers
from .models import Question, Quiz

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        exclude = ['quiz']

class QuizSerializer(serializers.ModelSerializer):



    class Meta:
        model = Quiz
        fields = '__all__'
