from collections import deque
from typing import List, Optional

class BaseResource:
    """Базовий клас ресурсу (Наслідування & Інкапсуляція)."""
    def __init__(self, value: float):
        self._value = float(value)

    @property
    def value(self) -> float:
        return self._value

    def _add(self, amount: float) -> None:
        self._value += amount

    def _subtract(self, amount: float) -> None:
        self._value -= amount


class Budget(BaseResource):
    """Клас управлінням бюджетом кафе."""
    def add(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Сума додання не може бути від'ємною.")
        self._add(amount)

    def withdraw(self, amount: float) -> bool:
        if amount < 0:
            raise ValueError("Сума зняття не може бути від'ємною.")
        self._subtract(amount)
        return self._value >= 0


class CoffeeBeans(BaseResource):
    """Клас запасу кавових зерен."""
    def __init__(self, count: int):
        super().__init__(count)

    @property
    def count(self) -> int:
        return int(self._value)

    def add_beans(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Кількість не може бути від'ємною.")
        self._add(amount)

    def consume(self, amount: int = 1) -> bool:
        if self._value >= amount:
            self._subtract(amount)
            return True
        return False


class Reputation(BaseResource):
    """Клас репутації кафе від 0 до 100."""
    def __init__(self, val: float = 70.0):
        super().__init__(max(0.0, min(100.0, val)))

    @property
    def value(self) -> float:
        return round(self._value, 1)

    def modify(self, delta: float) -> None:
        self._value = max(0.0, min(100.0, self._value + delta))


class Customer:
    """Модель клієнта кафе."""
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name


class CustomerQueue:
    """Черга обслуговування клієнтів (FIFO)."""
    def __init__(self):
        self.__queue: deque[Customer] = deque()

    def enqueue(self, customer: Customer) -> None:
        self.__queue.append(customer)

    def dequeue(self) -> Optional[Customer]:
        if self.is_empty():
            return None
        return self.__queue.popleft()

    def is_empty(self) -> bool:
        return len(self.__queue) == 0

    def size(self) -> int:
        return len(self.__queue)


class CafeState:
    """Загальний стан кафе."""
    def __init__(self, budget: float, beans: int, reputation: float, max_days: int):
        self.budget = Budget(budget)
        self.beans = CoffeeBeans(beans)
        self.reputation = Reputation(reputation)
        self.current_day: int = 1
        self.max_days: int = max_days
        self.is_bankrupt: bool = False
        self.history_logs: List[str] = []

    def log(self, message: str) -> None:
        self.history_logs.append(message)
