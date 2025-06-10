from .views import *
from django.urls import path

urlpatterns = [
    path("upload", UploadCSVView.as_view()),
    path('quiz/', QuizApiView.as_view()),
    path('question/<int:pk>', QuestionApiView.as_view()),
    path('question/', PerformChoiceApiView.as_view())
]