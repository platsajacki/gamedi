from django.apps import AppConfig


class GamesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'games'
    verbose_name = 'Игры'

    def ready(self) -> None:
        """Функция, которая выполняется при загрузке приложения."""
        import games.signals  # noqa: F401
        return super().ready()
