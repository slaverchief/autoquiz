from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.apps import apps

# Переписан класс менеджера, дабы не приходилось вводить email при суперпользователя
class CustomManager(UserManager):
    def _create_user_object(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("Нужно ввести имя пользователя")
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        return user

class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    email = None
    date_joined = None
    REQUIRED_FIELDS = []
    EMAIL_FIELD = None
    objects = CustomManager()