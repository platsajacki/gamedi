from django.db.models import Model


def get_file_path(instance: Model, filename: str) -> str:
    """
    Генерирует путь для сохранения файла на основе ID игры.
    """
    extension = filename.split('.')[-1]
    return f'game_files/game_{instance.game.id}/{instance.name}.{extension}'
