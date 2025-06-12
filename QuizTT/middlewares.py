from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from QuizTT.exceptions import *


class CustomExceptionsHandler:
    """
    Middleware для обработки исключений, связанных с правилами бизнес логики приложения
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, BaseAppException):
            status = 400
            message = f"Ошибка со стороны клиента: {exception}"
        elif isinstance(exception, ObjectDoesNotExist):
            status = 400
            message = f"Объект не найден"
        else:
            status = 500
            message = "Непредвиденная ошибка"

        return HttpResponse(status=status, content=message)