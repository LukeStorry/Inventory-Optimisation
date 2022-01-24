# Inventory-Optimisation-Demo
#### Demo and slides for a talk about inventory modelling and strategy optimisation in Python.


Using [simpy](https://simpy.readthedocs.io/en/latest/) for discrete event simulation, [matplotlib](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.html) for graphs, the [epsilon-greedy algorithm](https://en.wikipedia.org/wiki/Multi-armed_bandit#:~:text=Epsilon%2Dgreedy,-strategy) for input optimisation, and the [reveal-js](https://revealjs.com/) framework for the presentation.

__Slides viewable [here](https://lukestorry.github.io/Inventory-Optimisation/slides.html)__

---
## Overview
![Discrete Events Diagram](assets/simulation.svg)
---
## Output
#### With only the Purchasing event
![availability diagram - only purchasing (goes up)](assets/availability_1_only_purchasing.png)
#### After adding aged stock clearout
![availability diagram - with stock clearout (goes up and down blockily)](assets/availability_2_with_stock_clearout.png)
#### After adding sales
![availability diagram - with clearout and sales (blocks are smoothed off by sales - realistic diagram)](assets/availability_3_with_clearout_and_sales.png)
#### Result of greedy-epsilon optimisation
![availability diagram - optimised (minimal spending, no out-of-stock)](assets/availability_optimised.png)
#### Comparison of different Epsilon values (reward per iteration)
![epsilon comparison](assets/epsilon_comparison.png)

---
## Setup & running
Install required packages: `pip install -r .\requirements.txt`

Run the scripts with: `python simulation.py` or `python optimisation.py`

---
## Creating your own optimiser
Either use the simple greedy-epsilon-agent-based optimiser as a starting point, or in a new file:
```python
from simulation import PurchaseOrder, Simulation

# Initial inputs
purchase_orders = [PurchaseOrder(0, 20), PurchaseOrder(100, 100)]

for iteration in range(100):
    simulation = Simulation(purchase_orders)
    simulation.run()
    simulation.plot()

    # Customise this calculation depending on requirements
    cost = sum(simulation.availabilities)
    
    # Calculate a new set of more-optimal inputs
    purchase_orders = [] 
```