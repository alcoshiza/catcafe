import random
from typing import List, Tuple, Dict, Any, Optional
from interfaces import IStorageService, ILoggerService, IEvent
from models import CafeState, Customer, CustomerQueue
from events import EventFactory

class GameEngine:
    """Ядро гри зі збереженням стану та DI."""
    def __init__(self, storage: IStorageService, logger: ILoggerService, config_path: str = "data/config.json"):
        self._storage = storage
        self._logger = logger
        self.config_path = config_path
        self.config = self._storage.load_config(config_path)

        self.price_per_pack = self.config.get("price_per_pack", 25.0)
        self.guest_names = self.config.get("guest_names", ["Гість"])
        self.event_factory = EventFactory()

        self.last_shift_customers: List[Dict[str, Any]] = []
        self.last_shift_stats: Dict[str, Any] = {}
        self.shift_history: List[Dict[str, Any]] = []
        self.last_event_result: Optional[str] = None
        self.last_supplies_bought: int = 0
        self.last_supplies_cost: float = 0.0

        # Оновлений список котиків згідно з побажаннями
        self.resident_cats = [
            {"name": "Барсік", "breed": "Британський лежень", "mood": "Спить на м'якому кріслі 💤", "icon": "🐱"},
            {"name": "Скумбрія", "breed": "Смугаста мисливиця", "mood": "Постійно вимагає свіжу рибку 🐟", "icon": "🐈"},
            {"name": "Прікол", "breed": "Рудий бешкетник", "mood": "Влаштовує хаос та ганяє мух ⚡", "icon": "😼"},
            {"name": "Люся", "breed": "Перська принцеса", "mood": "Зверхньо оцінює гостей кафе 👑", "icon": "✨"},
            {"name": "Тузік", "breed": "Дворовий охоронець", "mood": "Думає, що він грізний сторожовий пес 🐕", "icon": "🛡️"},
            {"name": "Шарік", "breed": "Шотландська пампушка", "mood": "Круглий як булочка, любить обійми 🥐", "icon": "🍩"},
            {"name": "Кульок", "breed": "Сіамський ніндзя", "mood": "Шелестить пакетами о 3-й ночі 🛍️", "icon": "📦"}
        ]

        self.init_game()
        self._logger.log_info("Ігрове ядро успішно ініціалізовано.")

    def init_game(self, max_days: Optional[int] = None) -> None:
        """Ініціалізація або перезапуск гри з можливістю налаштування кількості днів."""
        total_days = max_days if max_days is not None else self.config.get("max_days", 5)
        self.state = CafeState(
            budget=self.config.get("initial_budget", 2500.0),
            beans=self.config.get("initial_coffee_beans", 20),
            reputation=self.config.get("initial_reputation", 70.0),
            max_days=total_days
        )
        self.last_shift_customers.clear()
        self.last_shift_stats.clear()
        self.shift_history.clear()
        self.last_event_result = None
        self.last_supplies_bought = 0
        self.last_supplies_cost = 0.0

    def set_max_days(self, days: int) -> None:
        """Масштабування тривалості гри користувачем."""
        if days < 1:
            raise ValueError("Тривалість гри повинна бути не менше 1 дня.")
        self.state.max_days = days
        self._logger.log_info(f"Тривалість гри змінено на {days} днів.")

    def buy_supplies(self, amount: int) -> Tuple[bool, str]:
        """Купівля зерен."""
        if amount <= 0:
            self.last_supplies_bought = 0
            self.last_supplies_cost = 0.0
            return True, "Закупівлю пропущено."

        total_cost = amount * self.price_per_pack
        if self.state.budget.value < total_cost:
            msg = f"Недостатньо коштів! Потрібно {total_cost} грн, у вас {self.state.budget.value:.2f} грн."
            self._logger.log_warning(msg)
            return False, msg

        self.state.budget.withdraw(total_cost)
        self.state.beans.add_beans(amount)
        self.last_supplies_bought = amount
        self.last_supplies_cost = total_cost
        msg = f"Придбано {amount} порцій зерен за {total_cost:.2f} грн."
        self._logger.log_info(msg)
        return True, msg

    def get_random_event(self) -> IEvent:
        return self.event_factory.get_random_event()

    def process_event_choice(self, event: IEvent, choice_index: int) -> str:
        res = event.execute(self.state, choice_index)
        self.last_event_result = res
        self._logger.log_info(f"Подія '{event.title}': {res}")
        self._check_bankruptcy()
        return res

    def simulate_day(self, cup_price: float) -> List[str]:
        """Обслуговування черги відвідувачів та збереження структурованих даних для GUI."""
        logs = []
        rep = self.state.reputation.value
        base_guests = max(3, int((rep / 10.0) - (cup_price / 20.0)))
        num_guests = max(1, base_guests + random.randint(-1, 2))

        queue = CustomerQueue()
        for _ in range(num_guests):
            name = random.choice(self.guest_names)
            queue.enqueue(Customer(name))

        logs.append(f"--- Кафе відчинилося! Черга: {queue.size()} відвідувачів ---")
        served = 0
        drinks = ["Капучино", "Лате з пінкою", "Флет Вайт", "Еспресо", "Раф-кава", "Карамельний макіато", "Мокачино"]

        self.last_shift_customers.clear()

        while not queue.is_empty():
            customer = queue.dequeue()
            if customer is None:
                break

            drink_name = random.choice(drinks)

            if self.state.beans.count >= 1:
                self.state.beans.consume(1)
                self.state.budget.add(cup_price)
                served += 1
                logs.append(f"☕ {customer.name} отримав(-ла) каву (+{cup_price:.2f} грн).")
                self.last_shift_customers.append({
                    "name": customer.name,
                    "drink": drink_name,
                    "served": True,
                    "price": cup_price,
                    "rep_delta": 0.0,
                    "status_text": f"Замовлення виконано (+{cup_price:.2f} грн)"
                })
            else:
                self.state.reputation.modify(-4)
                logs.append(f"❌ {customer.name} пішов(-ла) без кави! Нестача зерен (-4 репутації).")
                self.last_shift_customers.append({
                    "name": customer.name,
                    "drink": drink_name,
                    "served": False,
                    "price": 0.0,
                    "rep_delta": -4.0,
                    "status_text": "Не вистачило зерен (-4 репутації)"
                })

        logs.append(f"Підсумок зміни: обслуговано {served} із {num_guests} гостей.")
        self._logger.log_info(f"День {self.state.current_day} завершено. Обслуговано: {served}.")

        # Зберігаємо статистику поточної зміни
        self.last_shift_stats = {
            "day": self.state.current_day,
            "total_guests": num_guests,
            "served": served,
            "unserved": num_guests - served,
            "revenue": served * cup_price,
            "rep_delta": (num_guests - served) * -4.0,
            "cup_price": cup_price
        }

        self.shift_history.append(dict(self.last_shift_stats))

        self._check_bankruptcy()
        return logs

    def next_day(self) -> None:
        self.state.current_day += 1

    def _check_bankruptcy(self) -> None:
        if self.state.budget.value < 0:
            self.state.is_bankrupt = True
            self._logger.log_warning("Бюджет від'ємний! Оголошено банкрутство.")

    def save_final_report(self, file_path: str = "data/report.json") -> None:
        report = {
            "final_budget": self.state.budget.value,
            "final_beans": self.state.beans.count,
            "final_reputation": self.state.reputation.value,
            "days_passed": self.state.current_day,
            "is_bankrupt": self.state.is_bankrupt
        }
        self._storage.save_game_report(file_path, report)
        self._logger.log_info(f"Звіт успішно збережено в {file_path}")
