from abc import ABC, abstractmethod
from typing import Dict, Any, List

class IStorageService(ABC):
    """Інтерфейс для збереження та зчитування даних з файлів."""
    @abstractmethod
    def load_config(self, file_path: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def save_game_report(self, file_path: str, data: Dict[str, Any]) -> None:
        pass

class ILoggerService(ABC):
    """Інтерфейс для логування подій."""
    @abstractmethod
    def log_info(self, message: str) -> None:
        pass

    @abstractmethod
    def log_warning(self, message: str) -> None:
        pass

    @abstractmethod
    def log_error(self, message: str) -> None:
        pass

class IEvent(ABC):
    """Абстрактний клас для форс-мажорних подій (Поліморфізм & Абстракція)."""
    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def options(self) -> List[str]:
        pass

    @abstractmethod
    def execute(self, game_state: Any, choice_index: int) -> str:
        pass
