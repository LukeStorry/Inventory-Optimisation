import pprint
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
        # print(f"Applying {self}")
        old_value = getattr(self.recipient, self.parameter_name)
        setattr(self.recipient, self.parameter_name, old_value + self.step)

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


if __name__ == "__main__":
    purchase_orders = [PurchaseOrder(id, 100, 10) for id in range(10)]
    agent = Agent(0.2, purchase_orders)
    pprint(agent.actions)