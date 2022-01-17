import simpy
import matplotlib.pyplot as plt


class Item:
    def __init__(self, age: int, limit=100) -> None:
        self.age = age
        self.limit = limit

    def is_available(self):
        return self.age < self.limit


class Simulation:
    def __init__(self, run_length: int = 365) -> None:
        initial_ages = [0, 0, 0, 1, 1, 5, 5, 10, 10, 50, 50, 80, 80]
        age_limit = 100

        self.inventory = [Item(age, age_limit) for age in initial_ages]
        self.availabilities: dict[int, int] = {}

        self.environment = simpy.Environment()
        self.environment.process(self.daily_age_increment())
        self.environment.process(self.store_availabilities())
        self.environment.run(run_length)

    def daily_age_increment(self):
        while True:
            for item in self.inventory:
                item.age += 1
            yield self.environment.timeout(1)

    def store_availabilities(self):
        while True:
            available = sum(1 for item in self.inventory if item.is_available())
            self.availabilities[self.environment.now] = available
            yield self.environment.timeout(1)

    def plot(self):
        plt.plot(list(self.availabilities.keys()), list(self.availabilities.values()))
        plt.title('Availability over time')
        plt.xlabel('Simulation Timestep')
        plt.ylabel('Items Available')
        plt.show()


a = Simulation()
a.plot()
