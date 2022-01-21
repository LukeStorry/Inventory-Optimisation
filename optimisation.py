from dataclasses import dataclass
from pprint import pprint
from random import choice, seed, random
from typing import List

import matplotlib.pyplot as plt
from tqdm import tqdm

from simulation import PurchaseOrder, Simulation


@dataclass
class Action:
    """A Single action that our Agent can choose to apply"""
    step: int
    recipient: PurchaseOrder
    reward: int = 0

    def apply(self):
        """Alter the recipient by applying a step, limiting at 0"""
        self.recipient.amount = max(0, self.recipient.amount + self.step)


class Agent:
    """An Epsilon-Greedy Agent with a collection of Actions based on given PurchaseOrders"""

    def __init__(self, purchase_orders: List[PurchaseOrder], eps: int):
        self.eps = eps
        self.actions = [Action(step, purchase_order) for purchase_order in purchase_orders for step in (-1, +1)]
        self.chosen_action: Action = None
        self.rewards: List[int] = []

    def choose_action(self) -> Action:
        """Either Explore a random action, or Exploit the action with best reward, depending on EPS"""
        if random() < self.eps:
            self.chosen_action = choice(self.actions)
        else:
            self.chosen_action = max(self.actions, key=lambda a: a.reward)

        return self.chosen_action

    def give_reward(self, reward: int):
        """Update the latest Action with the given reward, and keep track of the reward internally"""
        self.chosen_action.reward = reward
        self.rewards.append(reward)

    def plot(self):
        """Plots the Reward over time throughout the optimisation"""
        plt.plot(self.rewards)
        plt.title("Reward over time")
        plt.xlabel("Iteration")
        plt.ylabel("Reward")
        plt.show()


def calculate_reward(simulation: Simulation) -> int:
    """Calculates the reward to give to the agent after a simulation"""
    number_of_purchases = sum(po.amount for po in simulation.purchase_orders)
    empty_penalty = sum(-4 for value in simulation.availabilities.values() if value == 0)
    return 1000 + empty_penalty - number_of_purchases


def run_optimiser(eps=0.2, iterations=2000):
    """Repeatedly use the agent to find optimum input to the simulation."""
    purchase_orders = [PurchaseOrder(time, 20) for time in range(0, 365, 30)]
    agent = Agent(purchase_orders, eps)
    for i in tqdm(range(iterations)):
        seed(i)
        agent.choose_action().apply()
        simulation = Simulation(purchase_orders)
        simulation.run()
        agent.give_reward(calculate_reward(simulation))
    pprint(purchase_orders)
    pprint(agent.actions)
    simulation.plot()
    return agent


if __name__ == "__main__":
    agent = run_optimiser()
    print(agent.rewards[-1])
    agent.plot()

    # Epsilon hyperparameter comparisons:
    # for eps in (0, 0.1, 0.2, 0.3, 0.4, 0.5):
    #     agent = run_optimiser(eps)
    #     plt.plot(agent.rewards, label=eps)
    # plt.legend()
    # plt.show()
