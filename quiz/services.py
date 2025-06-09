import csv
import typing
from io import TextIOWrapper
from django.core.files import File

def accept_and_decode_csv(csv_file: File) -> typing.Optional[list]:
    """
    получает на вход файл, проверяет, является ли он типом csv и извлекает из него данные в удобном видеаф
    """
    if not csv_file.name.endswith('.csv'):
        return
    try:
        decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
        reader = csv.reader(decoded_file)
        rows = [row for row in reader][1:]
        return rows
    except:
        return