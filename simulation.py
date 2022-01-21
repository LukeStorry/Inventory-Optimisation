import random
from dataclasses import dataclass
from typing import List

import matplotlib.pyplot as plt
import simpy


@dataclass
class PurchaseOrder:
    """An object to store Orders of an amount of Items on a certain day"""
    day: int
    amount: int


@dataclass
class Item:
    """A single degradable inventory Item"""
    age: int


class Simulation:
    """A Simulation of inventory over time"""

    def __init__(self, purchase_orders: List[PurchaseOrder]):
        self.age_limit = 90
        initial_ages = [0, 0, 0, 1, 1, 5, 5, 10, 10, 50, 50, 80, 80]
        self.inventory = [Item(age) for age in initial_ages]
        self.availabilities: dict[int, int] = {}
        self.purchase_orders = sorted(purchase_orders, key=lambda p: p.day)

    def run(self, run_length: int = 365):
        random.seed(42)
        self.environment = simpy.Environment()
        self.environment.process(self.daily_age_increment())
        self.environment.process(self.weekly_stock_clearout())
        self.environment.process(self.handle_sales())
        self.environment.process(self.handle_purchases())
        self.environment.process(self.monitor_availabilities())
        self.environment.run(run_length)
        return self.availabilities

    def daily_age_increment(self):
        """Simpy Generator to increase the age of all Items each day"""
        while True:
            for item in self.inventory:
                item.age += 1
            yield self.environment.timeout(1)

    def weekly_stock_clearout(self):
        """Simpy Generator to remove over-aged Items from inventory each week"""
        while True:
            self.inventory = [item for item in self.inventory if item.age < self.age_limit]
            yield self.environment.timeout(7)

    def handle_sales(self):
        """Simpy Generator to simulate the sale of items"""
        while True:
            yield self.environment.timeout(random.random())
            if self.inventory:
                del self.inventory[0]

    def handle_purchases(self):
        """Simpy Generator to create Items from PurchaseOrders and add them to the inventory"""
        for purchase in self.purchase_orders:
            yield self.environment.timeout(purchase.day - self.environment.now)
            self.inventory.extend(([Item(0) for _ in range(purchase.amount)]))

    def monitor_availabilities(self):
        """Simpy Generator to monitor the total inventory size each day"""
        while True:
            self.availabilities[self.environment.now] = len(self.inventory)
            yield self.environment.timeout(1)

    def plot(self):
        """Plots the availabilities on a line chart, with an optional requirement line"""
        plt.title("Availability over time")
        plt.xlabel("Simulation Timestep")
        plt.ylabel("Items Available")
        plt.plot(list(self.availabilities.keys()), list(self.availabilities.values()))
        plt.xlim(xmin=0)
        plt.ylim(ymin=0)
        plt.show()


if __name__ == "__main__":
    p = [
        PurchaseOrder(20, 250),
        PurchaseOrder(100, 250),
        PurchaseOrder(150, 250),
        PurchaseOrder(200, 250),
        PurchaseOrder(280, 250),
    ]
    s = Simulation(p)
    s.run()
    s.plot()
