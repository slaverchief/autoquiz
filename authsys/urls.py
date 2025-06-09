from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)


urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'), # эндпоинт для авторизации
    path('user', UserView.as_view())
]