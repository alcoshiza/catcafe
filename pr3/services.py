import json
import logging
from typing import Dict, Any
from interfaces import IStorageService, ILoggerService

class JsonStorageService(IStorageService):
    """Сервіс роботи з файлами JSON."""
    def load_config(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            # Дефолтні значення у разі відсутності файлу
            return {
                "initial_budget": 2500.0,
                "initial_coffee_beans": 20,
                "initial_reputation": 70,
                "max_days": 5,
                "price_per_pack": 25.0,
                "guest_names": ["Олена", "Максим", "Ірина", "Богдан", "Анастасія"]
            }

    def save_game_report(self, file_path: str, data: Dict[str, Any]) -> None:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


class FileLoggerService(ILoggerService):
    """Сервіс логування у файл app.log."""
    def __init__(self, log_filename: str = "app.log"):
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            encoding="utf-8"
        )
        self._logger = logging.getLogger("CatCafe")

    def log_info(self, message: str) -> None:
        self._logger.info(message)

    def log_warning(self, message: str) -> None:
        self._logger.warning(message)

    def log_error(self, message: str) -> None:
        self._logger.error(message)
