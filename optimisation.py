from math import sqrt
from pprint import pprint
from random import SystemRandom
from typing import List
from tqdm import tqdm

import matplotlib.pyplot as plt

from simulation import PurchaseOrder, Simulation

random = SystemRandom()


class Action:
    """A Single action that our Agent can choose to apply"""

    def __init__(self, step: int, recipient: PurchaseOrder) -> None:
        self.step = step
        self.recipient = recipient
        self.reward: float = 0

    def apply(self):
        """Alter the recipient by applying a step, limiting at 0"""
        self.recipient.amount = max(0, self.recipient.amount + self.step)

    def __repr__(self) -> str:
        return f"<Action with reward of {self.reward} for {self.recipient} {self.step}>"


class Agent:
    """An Epsilon-Greedy Agent with a collection of Actions based on given PurchaseOrders"""

    def __init__(self, purchase_orders: List[PurchaseOrder], eps: int):
        self.eps = eps
        self.actions = [Action(step, purchase_order) for purchase_order in purchase_orders for step in (-1, +1)]
        self.chosen_action: Action = None
        self.rewards: List[int] = []

    def choose_action(self) -> Action:
        """Either Explore a random action, or Exploit the action with best reward, depending on EPS"""
        if random.random() < self.eps:
            self.chosen_action = random.choice(self.actions)
        else:
            random.shuffle(self.actions)
            self.chosen_action = max(self.actions, key=lambda a: a.reward)

        return self.chosen_action

    def apply_reward(self, reward: int):
        """Update the latest Action with the given reward, and keep track of the reward internally"""
        if self.rewards:
            self.chosen_action.reward = reward - self.rewards[-1]
        self.rewards.append(reward)

    def plot(self):
        """Plots the Reward over timr throughout the optimisation"""
        plt.plot(self.rewards)
        plt.title("Reward over time")
        plt.xlabel("Iteration")
        plt.ylabel("Reward")
        plt.show()


def calculate_reward(simulation: Simulation) -> int:
    """Calculates the reward to give to the agent after a simulation"""
    number_of_purchases = sum(po.amount for po in simulation.purchase_orders)
    empty_penalty = sum(-100 for value in simulation.availabilities.values() if value < 3)
    return empty_penalty - 2*number_of_purchases


def run_optimiser(eps=0.2, iterations=4000):
    """Repeatedly use the agent to find optimum input to the simulation."""
    purchase_orders = [PurchaseOrder(time, 10) for time in range(0, 365, 30)]
    agent = Agent(purchase_orders, eps)
    for _ in tqdm(range(iterations)):
        agent.choose_action().apply()
        simulation = Simulation(purchase_orders)
        simulation.run()
        agent.apply_reward(calculate_reward(simulation))
    pprint(purchase_orders)
    pprint(agent.actions)
    # simulation.plot()
    return agent


if __name__ == "__main__":

    # agent = run_optimiser()
    # agent.plot()

    # Epsilon hyperparameter comparisons:
    for eps in (0, 0.1, 0.2, 0.3, 0.4, 0.5):
        agent = run_optimiser(eps)
        plt.plot(agent.rewards, label=eps)
    plt.legend()
    plt.show()
