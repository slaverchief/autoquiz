from django.db import transaction, IntegrityError
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import  Response
from quiz.serializers import *
from quiz.services import *
from quiz.models import *

# параметры схемы для описания path параметров
QUIZ_PK_PARAM = OpenApiParameter(name="id", location=OpenApiParameter.PATH, type=int, required=True,description="ID конкретного теcта")
ANSWER_PK_PARAM = OpenApiParameter(name="id", location=OpenApiParameter.PATH, type=int, required=True, description="ID конкретного ответа на вопрос")
QUESTION_PK_PARAM = OpenApiParameter(name="id", location=OpenApiParameter.PATH, type=int, required=True, description="ID конкретного вопроса")


class QuizApiView(ListAPIView):
    """
    Эндпоинт для вывода списка всех доступных тестов
    """
    serializer_class = QuizSerializer
    authentication_classes = ()

    def get_queryset(self):
        return Quiz.objects.all()

class QuestionApiView(ListAPIView):
    """
    Эндпоинт для вывода списка всех вопросов для конкретного теста
    """
    serializer_class = QuestionSerializer
    authentication_classes = ()

    @extend_schema(parameters=[QUIZ_PK_PARAM])
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz=self.kwargs['pk'])



class ChoiceAPIView(UpdateAPIView, CreateAPIView):
    serializer_class = QuestionUserSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ["PATCH", "POST"]



    def create(self, request, *args, **kwargs):
        data = request.data
        data['question'] = self.kwargs['pk']
        user = request.user
        try:
            with transaction.atomic():
                make_a_choice(data, user)
                return Response(status=201)
        except BaseAppException as e:
            raise BaseAppException(e)
        except IntegrityError as e:
            raise BaseAppException("вы уже ответили на этот вопрос")

    def get_queryset(self):
        return QuestionUser.objects.filter(pk=self.kwargs['pk'])

    @extend_schema(responses = {201: None}, parameters=[QUESTION_PK_PARAM])
    def post(self, request, *args, **kwargs):
        """
        Эндпоинт для ответа на вопрос
        """
        return super().post(request, *args, **kwargs)

    @extend_schema(parameters=[ANSWER_PK_PARAM])
    def patch(self, request, *args, **kwargs):
        """
        Эндпоинт для редактирования ответа на вопрос
        """
        quiz = self.get_object().question.quiz
        if request.user in quiz.users_passed.all():
            raise BaseAppException("вы уже завершили этот тест")
        return super().patch(request, *args, **kwargs)

class GetAnswersView(APIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = QuizWithAnswersSerializer

    @extend_schema(parameters=[QUIZ_PK_PARAM])
    def get(self, request, pk: str):
        """
        Эндроинт для получения конкретного объекта тестирования вместе с ответами на вопрос от запросившего пользователя
        """
        return Response(data=get_quiz_with_answers(pk, request.user))

    @extend_schema(responses = {200: {"type": "integer"}}, request = None, parameters=[QUIZ_PK_PARAM])
    def post(self, request, pk):
        """
        Эндпоинт для подсчёта оценки для конкретного теста и его завершения
        """
        res = count_grade(pk, request.user)
        return Response(res)

class UploadCSVView(View):
    """
    Страница для загрузки CSV на сервер
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


