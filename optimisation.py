from pprint import pprint
from random import choice, random, seed
from typing import List
from tqdm import tqdm

import matplotlib.pyplot as plt

from simulation import PurchaseOrder, Simulation

seed(20)


class Action:
    """A Single action that our Agent can choose to apply"""

    def __init__(self, step: int, recipient: PurchaseOrder, parameter_name: str) -> None:
        self.step = step
        self.recipient = recipient
        self.parameter_name = parameter_name
        self.reward: float = 0

    def apply(self):
        """Alter the recipient by applying a step, limiting at 0"""
        old_value = getattr(self.recipient, self.parameter_name)
        new_value = max(0, old_value + self.step)
        setattr(self.recipient, self.parameter_name, new_value)

    def __repr__(self) -> str:
        return f"<Action with reward of {self.reward} of {self.parameter_name} {self.step} for {self.recipient}>"


class Agent:
    """An Epsilon-Greedy Agent with a collection of Actions based on given PurchaseOrders"""

    def __init__(self, purchase_orders: List[PurchaseOrder], eps: int):
        self.eps = eps
        self.actions = [Action(step, purchase_order, parameter_name)
                        for purchase_order in purchase_orders
                        for parameter_name in ("day", "amount")
                        for step in (-1, +1)
                        ]
        self.chosen_action: Action = None
        self.rewards: List[int] = []

    def choose_action(self) -> Action:
        """Either Explore a random action, or Exploit the action with best reward, depending on EPS"""
        if random() < self.eps:
            self.chosen_action = choice(self.actions)
        else:
            self.chosen_action = max(self.actions, key=lambda a: a.reward)

        return self.chosen_action

    def apply_reward(self, reward: int):
        """Update the latest Action with the given reward, and keep track of the reward internally"""
        self.rewards.append(reward)
        self.chosen_action.reward = reward

    def plot(self):
        """Plots the Reward over timr throughout the optimisation"""
        plt.plot(self.rewards)
        plt.title('Reward over time')
        plt.xlabel('Iteration')
        plt.ylabel('Reward')
        plt.show()


def run_optimiser(eps=0.2, iterations=5000, target=20):
    """Repeatedly use the agent to find optimum input to the simulation."""
    purchase_orders = [PurchaseOrder(200, 5) for _ in range(10)]
    agent = Agent(purchase_orders, eps)
    for _ in tqdm(range(iterations)):
        agent.choose_action().apply()
        simulation = Simulation(purchase_orders)
        simulation.run()
        agent.apply_reward(1000 - simulation.calculate_mean_squared_error(target) - simulation.calculate_sum_under_target(target))
    simulation.plot(target)
    return agent


if __name__ == "__main__":
    for eps in [0.2]:  # (0, 0.1, 0.2, 0.3, 0.4, 0.5):
        agent = run_optimiser(eps)
        plt.plot(agent.rewards, label=eps)

    plt.legend()
    plt.show()
