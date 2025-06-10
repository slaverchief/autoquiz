import csv
import typing
from io import TextIOWrapper
from django.core.files import File
from .models import *

def accept_and_decode_csv(csv_file: typing.Union[File, TextIOWrapper]) -> typing.Optional[list]:
    """
    получает на вход файл, проверяет, является ли он типом csv и извлекает из него данные в удобном видеаф
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
    corrects = set(corrects) # переводим в тип сет для ускорения(поиск в сете ведётся за O(1))
    question = Question.objects.create(content=text, quiz=quiz, type=qtype)
    for choice in choices:
        c = Choice.objects.create(text=choice)
        if choice in corrects:
            c.is_correct = True
        c.save()
        question.choices.add(c)

def create_quiz(data):
    quiz = Quiz.objects.create(name=data[0][0])  # вынимаем test_title
    for vals in data:
        text = vals[1]
        qtype = int(vals[2])
        choices = vals[3]
        corrects = vals[4]
        create_question(quiz, text, qtype, choices, corrects)
