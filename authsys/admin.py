from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "is_staff", "is_active",)
    list_filter = ("username", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )

    search_fields = ("username",)
    ordering = ("username",)


admin.site.register(CustomUser, CustomUserAdmin)