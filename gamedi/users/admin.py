from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Настройка панели администратора для модели 'User'."""
    fieldsets = UserAdmin.fieldsets + (('Игры', {'fields': ('games',)}),)  # type: ignore[operator]
