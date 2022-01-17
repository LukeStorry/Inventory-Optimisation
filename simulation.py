from typing import List
import simpy
import matplotlib.pyplot as plt


class PurchaseOrder:
    def __init__(self, date: int, amount: int) -> None:
        self.date = date
        self.amount = amount

    def __repr__(self) -> str:
        return f"<PurchaseOrder for {self.amount} at {self.date}>"


class Item:
    def __init__(self, age: int) -> None:
        self.age = age

    def is_available(self):
        return self.age < self.limit

    def __repr__(self) -> str:
        return f"<Item with age of {self.age}>"


class Simulation:
    def __init__(self, purchase_orders=List[PurchaseOrder], run_length: int = 365) -> None:
        initial_ages = [0, 0, 0, 1, 1, 5, 5, 10, 10, 50, 50, 80, 80]
        self.age_limit = 100

        self.inventory = [Item(age) for age in initial_ages]
        self.availabilities: dict[int, int] = {}

        self.environment = simpy.Environment()
        self.environment.process(self.daily_age_increment())
        self.environment.process(self.handle_purchases(purchase_orders))
        self.environment.process(self.store_availabilities())
        self.environment.run(run_length)

    def daily_age_increment(self):
        while True:
            for item in self.inventory:
                item.age += 1  # + random()
            yield self.environment.timeout(1)

    def store_availabilities(self):
        while True:
            available = sum(1 for item in self.inventory if item.age < self.age_limit)
            self.availabilities[self.environment.now] = available
            yield self.environment.timeout(1)

    def handle_purchases(self, purchase_orders: List[PurchaseOrder]):
        for purchase in sorted(purchase_orders, key=lambda p: p.date):
            yield self.environment.timeout(purchase.date - self.environment.now)
            self.inventory.extend(([Item(0) for _ in range(purchase.amount)]))

    def calculate_mean_squared_error(self, target=30) -> int:
        sum_of_squared_error = sum((target - value)**2 for value in self.availabilities.values())
        return round(sum_of_squared_error/len(self.availabilities))

    def plot(self):
        plt.plot(list(self.availabilities.keys()), list(self.availabilities.values()))
        plt.title('Availability over time')
        plt.xlabel('Simulation Timestep')
        plt.ylabel('Items Available')
        plt.ylim(ymin=0)
        plt.show()


if __name__ == "__main__":
    p = [PurchaseOrder(time, 6) for time in range(50, 500, 15)]
    s = Simulation(p)
    # s.plot()
    print(s.calculate_mean_squared_error())
