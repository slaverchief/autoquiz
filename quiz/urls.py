from .views import UploadCSVView
from django.urls import path

urlpatterns = [
    path("upload", UploadCSVView.as_view())
]