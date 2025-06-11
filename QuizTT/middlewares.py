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
            return HttpResponse(status=400, content=f"Ошибка со стороны клиента: {exception}")
        return HttpResponse(status=500, content="Произошла непредвиденная ошибка")