from abc import ABCMeta, abstractmethod
from typing import Any


class BaseService(metaclass=ABCMeta):
    """Абстрактный базовый класс для создания сервисов."""
    def __call__(self) -> Any:
        """Вызывает сервис для выполнения бизнес-логики."""
        return self.act()

    @abstractmethod
    def act(self) -> Any:
        """Абстрактный метод, который должен быть реализован в классе-наследнике. Содержит бизнес-логику сервиса."""
        raise NotImplementedError('Не релизован сервис в классе.')
