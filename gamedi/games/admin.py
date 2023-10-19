from django.contrib import admin

from .models import Game, Gener, AdminGameFile, UserGameFile


class AdminGameFileInline(admin.TabularInline):
    """
    Встроенное отображение файлов
    для администратора игры в административной панели.
    """
    model = AdminGameFile
    extra = 0


class UserGameFileInline(admin.TabularInline):
    """
    Встроенное отображение файлов
    для пользователя игры в административной панели.
    """
    model = UserGameFile
    extra = 0


@admin.register(Gener)
class GenerAdmin(admin.ModelAdmin):
    """Настройка панели администратора для модели 'Gener'."""
    list_display = ('id', 'name', 'discription',)
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Настройка панели администратора для модели 'Game'."""
    list_display = (
        'id', 'name', 'genre', 'price',
        'discount', 'final_price',
    )
    list_display_links = ('name',)
    inlines = [
        AdminGameFileInline, UserGameFileInline
    ]
    search_fields = ('name',)
    list_filter = ('genre',)
