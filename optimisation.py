from random import choice, random, seed
from typing import List

import matplotlib.pyplot as plt

from simulation import PurchaseOrder, Simulation

seed(42)


class Action:
    def __init__(self, step: int, recipient: PurchaseOrder, parameter_name: str) -> None:
        self.step = step
        self.recipient = recipient
        self.parameter_name = parameter_name
        self.reward: float = 0

    def apply(self):
        old_value = getattr(self.recipient, self.parameter_name)
        new_value = max(0, old_value + self.step)
        setattr(self.recipient, self.parameter_name, new_value)

    def __repr__(self) -> str:
        return f"<Action with reward of {self.reward} of {self.parameter_name} {self.step} for {self.recipient}>"


class Agent:
    def __init__(self, eps: float, purchase_orders: List[PurchaseOrder]) -> None:
        self.eps = eps
        self.actions = [Action(step, purchase_order, parameter_name)
                        for purchase_order in purchase_orders
                        for parameter_name in ("date", "amount")
                        for step in (-1, 1)
                        ]
        self.chosen_action: Action = None
        self.rewards: List[float] =[]

    def choose_action(self) -> Action:
        if random() < self.eps:
            self.chosen_action = choice(self.actions)
        else:
            self.chosen_action = max(self.actions, key=lambda a: a.reward)

        return self.chosen_action

    def apply_reward(self, reward: float):
        self.rewards.append(reward)
        self.chosen_action.reward = reward

    def plot(self):
        plt.plot(self.rewards)
        plt.title('Reward over time')
        plt.xlabel('Iteration')
        plt.ylabel('Reward')
        plt.show()


if __name__ == "__main__":
    purchase_orders = [PurchaseOrder(0, 0) for _ in range(10)]

    agent = Agent(0.2, purchase_orders)
    
    for iteration in range(10000):
        agent.choose_action().apply()
        simulation = Simulation(purchase_orders)
        reward = 1000 - simulation.calculate_mean_squared_error()
        agent.apply_reward(reward)

    agent.plot()
    simulation.plot()

