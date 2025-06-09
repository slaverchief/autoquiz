from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from quiz.services import accept_and_decode_csv


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
        data = accept_and_decode_csv(csv_file)
        return HttpResponse()


