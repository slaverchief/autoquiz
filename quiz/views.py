from django.db import transaction, connection
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from QuizTT.exceptions import BaseAppException
from quiz.serializers import *
from quiz.services import *
from quiz.models import *

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

class PerformChoiceApiView(CreateAPIView):
    """
    view для создания экземпляра ответа на вопрос
    """
    permission_classes = (IsAuthenticated, )
    model = QuestionUser
    serializer_class = QuestionUserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        try:
            with transaction.atomic():  # объявляем транзакцию для создания тестирования
                make_a_choice(data, user)
                return Response(status=201)
        except Exception as e:
            raise BaseAppException("допущена ошибка при отправлении ответа на вопрос")

class UploadCSVView(View):
    """
    view для загрузки CSV на сервер
    """
    # доступ только для суперпользователей
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)

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
            raise BaseAppException("допущена ошибка в CSV файле или файл неправильного расширения")
        return HttpResponse()


class GetAnswersView(APIView):
    """
    view для получения конкретного объекта тестирования вместе с ответами на вопрос от запросившего пользователя
    """
    serializer_class = QuizWithAnswersSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        return Response(data=get_quiz_with_answers(pk, request.user))