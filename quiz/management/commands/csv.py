from django.core.management.base import BaseCommand
from django.db import transaction

from QuizTT.exceptions import InvalidQuizData
from quiz.services import create_quiz, accept_and_decode_csv

class Command(BaseCommand):
    help = 'Все связанное с CSV файлами'

    def add_arguments(self, parser):
        parser.add_argument(type=str, dest="action")
        parser.add_argument(type=str, dest="action_subject")

    def handle(self, *args, **options):
        if options['action'] == "import":
            filename = options['action_subject']
            with open(filename, 'r') as f:
                try:
                    with transaction.atomic():  # объявляем транзакцию для создания тестирования
                        create_quiz(accept_and_decode_csv(f))
                except Exception as e:
                    raise InvalidQuizData()
            print("Файл импортирован")