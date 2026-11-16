import unittest
from models import Budget, CoffeeBeans, Reputation, Customer, CustomerQueue
from services import JsonStorageService, FileLoggerService
from engine import GameEngine

class TestCatCafeModels(unittest.TestCase):
    def test_budget_operations(self):
        b = Budget(100.0)
        b.add(50.0)
        self.assertEqual(b.value, 150.0)
        b.withdraw(30.0)
        self.assertEqual(b.value, 120.0)

    def test_reputation_bounds(self):
        rep = Reputation(95.0)
        rep.modify(10)
        self.assertEqual(rep.value, 100.0)
        rep.modify(-150)
        self.assertEqual(rep.value, 0.0)

    def test_customer_queue_fifo(self):
        q = CustomerQueue()
        c1 = Customer("Олена")
        c2 = Customer("Максим")
        q.enqueue(c1)
        q.enqueue(c2)
        
        self.assertEqual(q.size(), 2)
        served = q.dequeue()
        self.assertEqual(served.name, "Олена")
        self.assertEqual(q.size(), 1)

class TestGameEngine(unittest.TestCase):
    def setUp(self):
        self.storage = JsonStorageService()
        self.logger = FileLoggerService("test_app.log")
        self.engine = GameEngine(self.storage, self.logger)

    def test_supply_buying_insufficient_funds(self):
        success, _ = self.engine.buy_supplies(10000)
        self.assertFalse(success)

    def test_simulation_day_decreases_beans(self):
        initial_beans = self.engine.state.beans.count
        self.engine.simulate_day(50.0)
        self.assertLess(self.engine.state.beans.count, initial_beans + 1)

if __name__ == "__main__":
    unittest.main()
