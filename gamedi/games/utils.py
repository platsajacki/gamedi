from django.db.models import Model


def get_file_path(instance: Model, filename: str) -> str:
    """
    Генерирует путь для сохранения файла на основе ID игры.
    """
    extension: str = filename.split('.')[-1]
    return f'game_files/game_{instance.game.slug}/{instance.__class__.__name__}/{instance.name}.{extension}'


def get_cover_path(instance: Model, filename: str) -> str:
    """
    Генерирует путь для сохранения обложки на основе ID игры.
    """
    return 'game_files/game_{instance.slug}/Covers/cover_{filename}'


def get_hover_path(instance: Model, filename: str) -> str:
    """
    Генерирует путь для сохранения скрытой обложки на основе ID игры.
    """
    return f'game_files/game_{instance.slug}/Covers/hover_{filename}'
