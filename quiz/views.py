from django.db import transaction, IntegrityError
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from QuizTT.exceptions import BaseAppException
from quiz.serializers import *
from quiz.services import *
from quiz.models import *

QUIZ_PK_PARAM = OpenApiParameter(name="id", location=OpenApiParameter.PATH, type=int, required=True,description="ID конкретного теcта") # параметр схемы для описания параметра pk объекта теста


class QuizApiView(ListAPIView):
    """
    Эндпоинт для вывода списка всех доступных тестов
    """
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.all()

class QuestionApiView(ListAPIView):
    """
    Эндпоинт для вывода списка всех вопросов для конкретного теста
    """
    serializer_class = QuestionSerializer

    @extend_schema(parameters=[QUIZ_PK_PARAM])
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz=self.kwargs['pk'])

class PerformChoiceApiView(CreateAPIView):
    """
    Эндпоинт для ответа на вопрос
    """
    permission_classes = (IsAuthenticated, )
    model = QuestionUser
    serializer_class = QuestionUserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        try:
            with transaction.atomic():
                make_a_choice(data, user)
                return Response(status=201)
        except BaseAppException as e:
            raise BaseAppException(e)
        except IntegrityError as e:
            raise BaseAppException("вы уже ответили на этот вопрос")
        except Exception as e:
            raise BaseAppException("допущена ошибка при отправлении ответа на вопрос")

class UploadCSVView(View):
    """
    Эндпоинт для загрузки CSV на сервер
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
        except AssertionError as e:
            raise BaseAppException("допущена ошибка в CSV файле или файл неправильного расширения")
        return HttpResponse()


class GetAnswersView(APIView):
    """
    Эндроинт для получения конкретного объекта тестирования вместе с ответами на вопрос от запросившего пользователя
    """
    serializer_class = QuizWithAnswersSerializer
    permission_classes = (IsAuthenticated, )
    @extend_schema(parameters=[QUIZ_PK_PARAM])
    def get(self, request, pk: str):
        return Response(data=get_quiz_with_answers(pk, request.user))

    @extend_schema(description="Эндпоинт для подсчёта оценки для конкретного теста и его завершения",
                   responses = {200: {"type": "integer"}},
                   parameters=[QUIZ_PK_PARAM])
    def post(self, request, pk):
        res = count_grade(pk, request.user)
        return Response(res)