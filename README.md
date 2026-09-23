# Eco-Sim

Eco-Sim is a Python/Pygame multi-agent ecosystem simulation and an ongoing hobby project focused on exploring simulation programming, artificial life, and software development.

The simulation models a small ecosystem containing **plants, prey, and predators**. Agents can move through the environment, search for food using vision cones, flee from predators, eat, lose energy through movement, reproduce, and die when they run out of energy. The project is being developed incrementally, with new mechanics and improvements actively underway.

## Features

- 🌱 **Plants** that provide energy to prey
- 🐇 **Prey** that search for plants and flee from predators
- 🐺 **Predators** that hunt visible prey
- 👁️ **Vision cones** that determine which nearby agents can be detected
- ⚡ **Energy systems** that affect survival and reproduction
- 🏃 **Different movement behaviors**, including walking, hunting, and fleeing
- 🧬 **Reproduction and population growth**
- 💀 **Agent death** when energy is depleted
- 🌿 **Plant regrowth** over time
- 🖥️ **Pygame visualization** of the simulated ecosystem
- 🛠️ **Ongoing development** with additional simulation mechanics and improvements underway

## How to Run

### Requirements

You will need:

- Python 3
- Pygame

Install Pygame with:

```bash
pip install pygame
```

### Start the Simulation

Clone or download the project, navigate to the project directory, and run:

```bash
python main.py
```

A Pygame window should open and display the simulated ecosystem.

Press **R** while the simulation is running to reset the ecosystem and generate a new population.

To close the simulation, close the Pygame window.

## How the Simulation Works

Eco-Sim is designed around several types of agents interacting with one another.

**Prey** search their surroundings for plants. When they detect food within their vision cone, they move toward it. When they detect a predator, they flee for a period of time. Prey consume plants to gain energy, while movement consumes energy.

**Predators** search their vision cones for prey and pursue visible prey. Predators consume prey when they get close enough and gain a portion of the prey's energy. Their movement also consumes energy.

Both prey and predators can reproduce after reaching the appropriate age and reproduction interval. Agents that run out of energy die and are removed from the simulation.

Plants can be consumed by prey, and new plants periodically appear in the environment.

## Project Status

**Eco-Sim is actively being developed.**

The current version is best thought of as a foundation for a larger and more sophisticated ecosystem simulation rather than a finished product. The project is intentionally being expanded over time as new ideas, behaviors, environmental mechanics, and improvements are implemented.

**More updates are underway, and the simulation will continue to evolve as development progresses.**

## Purpose

This project began as a small hobby project intended to help develop programming and software-development skills. It is also an opportunity to experiment with multi-agent systems, simulation behavior, object-oriented programming, and game-development concepts in Python.

The project is not intended to represent a scientifically accurate ecological model. Instead, it provides a sandbox for experimenting with interacting agents and seeing how relatively simple rules can produce changing population dynamics.
