import random
import math
from settings import PREDATOR_REPRODUCTION_TIME, PREY_ENERGY_START, PREDATOR_ENERGY_START, PREY_REPRODUCTION_TIME

class Agent:
    def __init__(self, x, y, age, reproduceTimer):
        self.x = x
        self.y = y
        self.age = age
        self.reproduceTimer = reproduceTimer

        # facing direction (unit vector)
        angle = random.uniform(0, 2 * math.pi)
        self.facing = [math.cos(angle), math.sin(angle)]

        # vision parameters
        self.vision_distance = 100
        self.vision_angle = math.pi / 2 # 90 degrees

        self.speed = 3

    def move_random(self):
        # small random steering instead of full random walk
        if random.randint(1, 15) < 3:  # 20% chance to turn
            turn = random.uniform(-1.0, 1.0)
            cos_t = math.cos(turn)
            sin_t = math.sin(turn)

            fx, fy = self.facing
            self.facing = [
                fx * cos_t - fy * sin_t,
                fx * sin_t + fy * cos_t
            ]
        
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)

# Using PredatorAgent for now, even though it is not a predator. Change later.
class Plant(Agent):
    def __init__(self, x, y):
        super().__init__(x, y, age=0, reproduceTimer=0)
        self.cos_half_vision = math.cos(self.vision_angle / 2)

class Prey(Agent):
    def __init__(self, x, y):
        super().__init__(x, y, age=0, reproduceTimer=0)
        self.energy = PREY_ENERGY_START

        self.vision_distance = 80
        self.vision_angle = 3 * math.pi / 2 # 270 degrees
        self.speed = 2
        self.flee_timer = 0
        self.flee_from = None

        isinstance(Agent, Prey)
        self.cos_half_vision = math.cos(self.vision_angle / 2)

class Predator(Agent):
    def __init__(self, x, y):
        super().__init__(x, y, age=0, reproduceTimer=0)
        self.energy = PREDATOR_ENERGY_START

        self.vision_distance = 120
        self.vision_angle = math.pi / 3 # 60 degrees
        self.speed = 4

        isinstance(Agent, Predator)
        self.cos_half_vision = math.cos(self.vision_angle / 2)
