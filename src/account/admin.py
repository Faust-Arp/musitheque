from django.contrib import admin
from account.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "password",
        "is_active",
        "is_staff",
        "is_admin",
    )
