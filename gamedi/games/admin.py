from django.contrib import admin

from .models import AdminGameFile, Game, Genre, UserGameFile


class AdminGameFileInline(admin.TabularInline):
    """
    Встроенное отображение файлов
    для администратора игры в административной панели.
    """
    model = AdminGameFile
    extra = 0
    ordering = ('order_number',)
    fields = (
        'name', 'order_number',
        'is_published', 'file',
    )


class UserGameFileInline(admin.TabularInline):
    """
    Встроенное отображение файлов
    для пользователя игры в административной панели.
    """
    model = UserGameFile
    extra = 0
    ordering = ('order_number',)
    fields = (
        'name', 'order_number',
        'is_published', 'file',
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройка панели администратора для модели 'Gener'."""
    list_display = (
        'id', 'name', 'description',
        'is_published', 'created'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    fields = (
        'name', 'slug',
        'is_published', 'description',
    )


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Настройка панели администратора для модели 'Game'."""
    list_display = (
        'order_number', 'is_published', 'name', 'genre',
        'price', 'discount', 'final_price', 'id', 'created'
    )
    list_display_links = ('name',)
    inlines = [
        AdminGameFileInline, UserGameFileInline
    ]
    search_fields = ('name',)
    ordering = ('order_number',)
    fieldsets = (
        (
            'Наименование и публикация',
            {
                'fields': (
                    'name', 'slug',
                    'order_number', 'is_published',
                ),
            }
        ),
        (
            'Параметры',
            {
                'fields': (
                    'genre', 'age_restriction', 'description',
                    'min_players', 'max_players', 'time',
                    'price', 'discount'
                ),
            }
        ),
        (
            'Файлы',
            {
                'fields': ('cover', 'hover_cover',),
            }
        ),
    )
