from django.db.models import Model


def get_file_path(instance: Model, filename: str) -> str:
    """Генерирует путь для сохранения файла на основе slug игры."""
    extension: str = filename.split('.')[-1]
    return (
        f'game_files/game_'
        f'{instance.game.slug}/{instance.__class__.__name__}/{instance.name}.{extension}'  # type: ignore[attr-defined]
    )


def get_cover_path(instance: Model, filename: str) -> str:
    """Генерирует путь для сохранения обложки на основе slug игры."""
    return f'game_files/game_{instance.slug}/Covers/cover_{filename}'  # type: ignore[attr-defined]


def get_hover_path(instance: Model, filename: str) -> str:
    """Генерирует путь для сохранения скрытой обложки на основе slug игры."""
    return f'game_files/game_{instance.slug}/Covers/hover_{filename}'  # type: ignore[attr-defined]
