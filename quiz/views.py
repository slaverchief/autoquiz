from django.db import transaction
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from QuizTT.exceptions import InvalidQuizData
from quiz.serializers import *
from quiz.services import accept_and_decode_csv, create_quiz
from .models import *

class QuizApiView(ListAPIView):
    """
    для вывода списка всех квизов
    """
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.all()

class QuestionApiView(ListAPIView):
    """
    для вывода списка всех вопросов для конкретного квиза
    """
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(quiz=self.kwargs['pk'])


class UploadCSVView(View):
    """
    view для загрузки CSV на сервер
    """

    def get(self, request):
        return render(request, 'quiz/upload.html')

    def post(self, request):
        if 'csv_file' not in request.FILES:
            return HttpResponse(status=400)
        csv_file = request.FILES['csv_file']
        try:
            with transaction.atomic():  # объявляем транзакцию для создания тестирования
                create_quiz(accept_and_decode_csv(csv_file))
        except Exception as e:
            raise InvalidQuizData()
        return HttpResponse()


