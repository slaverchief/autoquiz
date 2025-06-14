from .views import *
from django.urls import path

urlpatterns = [
    path("upload", UploadCSVView.as_view(), name="upload"),
    path('quiz/', QuizApiView.as_view(), name="quiz_api"),
    path("quiz/<int:pk>", GetAnswersView.as_view(), name="get_answers"),
    path('question/<int:pk>', QuestionApiView.as_view(), name='question_api'),
    path('choice/<int:pk>', ChoiceAPIView.as_view(), name='choice_api'),

]