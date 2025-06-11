import csv
import typing
from io import TextIOWrapper
from django.core.files import File
from django.db.models import Count

from QuizTT.exceptions import BaseAppException
from .models import *
from .serializers import QuizWithAnswersSerializer


def accept_and_decode_csv(csv_file: typing.Union[File, TextIOWrapper]) -> typing.Optional[list]:
    """
    Получает на вход файл, проверяет, является ли он типом csv и извлекает из него данные в удобном виде
    """
    if not csv_file.name.endswith('.csv'):
        return
    try:
        if isinstance(csv_file, TextIOWrapper):
            decoded_file = csv_file
        else:
            decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
        reader = csv.DictReader(decoded_file)
        data = []
        for row in reader:
            title = row['test_title']
            question_text = row['question_text']
            question_type = row["question_type"]
            choices = row['choices'].split("|")
            correct_answers = row['correct_answers'].split("|")
            data.append((title, question_text, question_type, choices, correct_answers))
        return data
    except:
        return

def create_question(quiz: Quiz, text: str, qtype: int, choices: list[str], corrects: list[str]):
    """
    Создает конкретный экземпляр вопроса
    """
    corrects = set(corrects) # переводим в тип сет для ускорения(поиск в сете ведётся за O(1))
    question = Question.objects.create(content=text, quiz=quiz, type=qtype)
    for choice in choices:
        c = Choice.objects.create(text=choice, question=question)
        if choice in corrects:
            c.is_correct = True
        c.save()

def create_quiz(data: list):
    """
    Создает конкретный экземпляр теста
    """
    quiz = Quiz.objects.create(name=data[0][0])  # вынимаем test_title
    for vals in data:
        text = vals[1]
        qtype = int(vals[2])
        choices = vals[3]
        corrects = vals[4]
        create_question(quiz, text, qtype, choices, corrects)

def make_a_choice(data: dict, user: CustomUser):
    """
    Создает конкретный экземпляр ответа на вопрос(регистрирует ответ на вопрос)
    """
    question = Question.objects.get(pk=data['question'])
    quiz = question.quiz
    if user in quiz.users_passed.all():
        raise BaseAppException("вы уже завершили этот тест")
    choices = set([obj.pk for obj in question.choices.all()])  # создаем сет вариантов ответа для того чтобы ускорить выборку
    answers = data['answers']
    # если в ответе пользователь указывает вариант, который не предусмотрен в тесте, это воспринимается как ошибка
    for ans in answers:
        if ans not in choices:
            raise
    m = QuestionUser.objects.create(user=user, question=question)
    m.answers.set(data['answers'])
    m.save()


def get_quiz_with_answers(quiz_pk: int, user: CustomUser):
    """
    Выполняет выборку с объектом тестирования и ответами на его вопросы
    """
    quiz = Quiz.objects.get(pk=quiz_pk)
    questions = quiz.questions.all()
    qs = QuestionUser.objects.filter(user=user, question__in=questions)
    s = QuizWithAnswersSerializer({"quiz": quiz, "questions": qs})
    return s.data

def count_grade(quiz_pk: int, user: CustomUser):
    """
    Подсчёт оценки для конкретного пользователя на конкретном тесте.
    Алгоритм работает так, что сначала подсчитывается достигнутая
    сумма - сумма отношений количества правильных ответов на общее количество ответов.
    Достигнутая сумма делится на количество вопросов в тесте, умножается на 100 и округляется до 2 знаков.
    """
    quiz = Quiz.objects.get(pk=quiz_pk)
    if user not in quiz.users_passed.all():
        quiz.users_passed.add(user)
    questions = quiz.questions.all()
    perfect_sum = len(questions)*1
    # используем prefetch_related, так как дальше проходимся по списку объектов: их надо выгрузить заранее
    objects = QuestionUser.objects.filter(user=user, question__in=questions).prefetch_related('answers').annotate(Count("answers"))
    reached_sum = 0
    for qs in objects:
        correct_amount = 0
        answers = qs.answers.all()
        ans_amount = qs.answers__count
        for answer in qs.answers.all():
            correct_amount += int(answer.is_correct)
        reached_sum += correct_amount/ans_amount
    return round((reached_sum/perfect_sum)*100, 2)