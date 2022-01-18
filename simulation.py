from typing import List

import matplotlib.pyplot as plt
import simpy


class PurchaseOrder:
    """An object to store Orders of an amount of Items on a certain day"""

    def __init__(self, day: int, amount: int) -> None:
        self.day = day
        self.amount = amount

    def __repr__(self) -> str:
        return f"<PurchaseOrder for {self.amount} at {self.day}>"


class Item:
    """A single degradable inventory Item"""

    def __init__(self, age: int) -> None:
        self.age = age

    def __repr__(self) -> str:
        return f"<Item with age of {self.age}>"


class Simulation:
    """A Simulation of inventory over time"""

    def __init__(self,
                 purchase_orders=List[PurchaseOrder],
                 initial_ages=[0, 0, 0, 1, 1, 5, 5, 10, 10, 50, 50, 80, 80],
                 age_limit=100):

        self.age_limit = age_limit
        self.inventory = [Item(age) for age in initial_ages]
        self.availabilities: dict[int, int] = {}
        self.purchase_orders = sorted(purchase_orders, key=lambda p: p.day)

    def run(self, run_length: int = 365):
        self.environment = simpy.Environment()
        self.environment.process(self.daily_age_increment())
        self.environment.process(self.handle_purchases())
        self.environment.process(self.store_availabilities())
        self.environment.run(run_length)

    def daily_age_increment(self):
        """Simpy Generator to increase the age of all Items each day"""
        while True:
            for item in self.inventory:
                item.age += 1  # + random()
            yield self.environment.timeout(1)

    def store_availabilities(self):
        """Simpy Generator to monitor the total availability each day"""
        while True:
            available = sum(1 for item in self.inventory if item.age < self.age_limit)
            self.availabilities[self.environment.now] = available
            yield self.environment.timeout(1)

    def handle_purchases(self):
        """Simpy Generator to create Items from PurchaseOrders and add them to the inventory"""
        for purchase in self.purchase_orders:
            yield self.environment.timeout(purchase.day - self.environment.now)
            self.inventory.extend(([Item(0) for _ in range(purchase.amount)]))

    def calculate_mean_squared_error(self, target=30) -> int:
        """Calculates the MSD of the availabilities compared to a target, Post-Simulation"""
        sum_of_squared_error = sum((target - value)**2 for value in self.availabilities.values())
        return round(sum_of_squared_error/len(self.availabilities))

    def calculate_sum_under_target(self, target=30) -> int:
        """Calculates the amount of under-stocking across all days, Post-Simulation"""
        return sum((target - value) for value in self.availabilities.values() if value < target)

    def plot(self, target: int = 30):
        """Plots the availabilities on a line chart"""
        plt.plot(list(self.availabilities.keys()), list(self.availabilities.values()))
        plt.axhline(y=target, color='r', linestyle='--')
        plt.title('Availability over time')
        plt.xlabel('Simulation Timestep')
        plt.ylabel('Items Available')
        plt.ylim(ymin=0)
        plt.show()


if __name__ == "__main__":
    p = [PurchaseOrder(time, 5) for time in range(10, 500, 15)]
    s = Simulation(p)
    s.run()
    print(s.calculate_mean_squared_error())
    print(s.calculate_sum_under_target())
    s.plot()
