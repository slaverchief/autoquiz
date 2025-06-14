from django.urls import path
from .views import *



urlpatterns = [
    path('login', LoginView.as_view(), name='token_obtain_pair'), # эндпоинт для авторизации
    path('user', UserView.as_view(), name="user_api")
]