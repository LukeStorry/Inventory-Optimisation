from random import choice, random, seed

from typing import List
from simulation import Simulation, PurchaseOrder


seed(42)


class Action:
    def __init__(self, step: int, recipient: PurchaseOrder, parameter_name: str) -> None:
        self.step = step
        self.recipient = recipient
        self.parameter_name = parameter_name
        self.reward: float = 0

    def apply(self):
        print(f"Applying {self}")
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

    def choose_action(self) -> Action:
        if random() < self.eps:
            print("Explore", end=' ')
            self.chosen_action = choice(self.actions)
        else:
            print("Exploit", end=' ')
            self.chosen_action = max(self.actions, key=lambda a: a.reward)

        return self.chosen_action

    def apply_reward(self, reward: float):
        print(f"Reward: {reward}")
        self.chosen_action.reward = reward


if __name__ == "__main__":
    purchase_orders = [PurchaseOrder(date, 0) for date in range(10)]
    Simulation(purchase_orders).plot()
    agent = Agent(0.2, purchase_orders)
    
    for iteration in range(10):
        print(iteration, end=' ')
        agent.choose_action().apply()
        simulation = Simulation(purchase_orders)
        agent.apply_reward(5000 - simulation.calculate_mean_squared_error())

    simulation.plot()

