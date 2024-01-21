from django.contrib import admin

from purchases.models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    """Настройка панели администратора для модели 'Purchase'."""
    _fields = ('user', 'game', 'price', 'status', 'created', 'updated')
    list_display = _fields
    fields = _fields
    readonly_fields = _fields
    list_display_links = ('user',)
    search_fields = ('user', 'status')
    list_filter = ('user', 'game', 'status',)
    ordering = ('updated', 'status')

    def has_add_permission(self, request, obj=None):
        """Отключает возможность добавления новых объектов 'Purchase' через административный интерфейс."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Отключает возможность удаления объектов 'Purchase' через административный интерфейс."""
        return False
