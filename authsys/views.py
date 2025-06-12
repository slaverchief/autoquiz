from drf_spectacular.utils import extend_schema
from rest_framework.settings import api_settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings

class LoginView(TokenObtainPairView):
    """
    Эндпоинт для авторизации пользователя по логину и паролю
    """

    permission_classes = [AllowAny]

class UserView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request):
        """
        Эндпоинт для получения ID текущего авторизованного пользователя
        """
        serializer = self.serializer_class(instance=request.user)
        return Response(serializer.data)

    @extend_schema(auth=[], responses=TokenObtainPairSerializer)
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Эндпоинт для создания пользователя
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.save()
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid()
        return Response(status=200, data=serializer.validated_data)