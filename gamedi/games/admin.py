from django.contrib import admin

from .models import Game, Gener, GameFile


class GameFileInline(admin.TabularInline):
    """Встроенное отображение файлов игры в административной панели."""
    model = GameFile
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
    inlines = [GameFileInline]
    search_fields = ('name',)
    list_filter = ('genre',)
