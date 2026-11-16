import os
from services import JsonStorageService, FileLoggerService
from engine import GameEngine
from gui import ModernCatCafeGUI

def main():
    # Створення необхідних директорій
    os.makedirs("data", exist_ok=True)
    
    # Ініціалізація залежностей (Dependency Injection)
    storage_service = JsonStorageService()
    logger_service = FileLoggerService("app.log")
    
    # Створення ядра та GUI
    engine = GameEngine(storage=storage_service, logger=logger_service, config_path="data/config.json")
    app = ModernCatCafeGUI(engine)
    
    # Запуск графічного інтерфейсу
    app.mainloop()

if __name__ == "__main__":
    main()
