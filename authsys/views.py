from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.request import Request
from .serializers import *

class UserView(APIView):
    serializer_class = UserSerializer

    # получение текущего пользователя
    @extend_schema(description="Эндпоинт для получения ID текущего авторизованного пользователя")
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=403)
        serializer = self.serializer_class(instance=request.user)
        return Response(serializer.data)

    # запрос на создание пользователя
    @extend_schema(description="Эндпоинт для создания пользователя")
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.save()
        token_data = RefreshToken.for_user(user_obj)
        refresh, access = str(token_data), str(token_data.access_token)
        return Response(status=200, data={"access": access})