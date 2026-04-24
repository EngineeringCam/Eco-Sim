import random
import math
from settings import PREY_ENERGY_START, PREDATOR_ENERGY_START

class PredatorAgent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = type

        # facing direction (unit vector)
        angle = random.uniform(0, 2 * math.pi)
        self.facing = [math.cos(angle), math.sin(angle)]

        # vision parameters
        self.vision_distance = 120
        self.vision_angle = math.pi / 3 # 60 degrees

        self.speed = 4

    def move_random(self):
        # small random steering instead of full random walk
        turn = random.uniform(-0.2, 0.2)
        cos_t = math.cos(turn)
        sin_t = math.sin(turn)

        fx, fy = self.facing
        self.facing = [
            fx * cos_t - fy * sin_t,
            fx * sin_t + fy * cos_t
        ]
        
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)

class PreyAgent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = type

        # facing direction (unit vector)
        angle = random.uniform(0, 2 * math.pi)
        self.facing = [math.cos(angle), math.sin(angle)]

        # vision parameters
        self.vision_distance = 80
        self.vision_angle = 3*math.pi / 2 # 270 degrees

        self.speed = 2

    def move_random(self):
        # small random steering instead of full random walk
        turn = random.uniform(-0.2, 0.2)
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
class Plant(PredatorAgent):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cos_half_vision = math.cos(self.vision_angle / 2)

class Prey(PreyAgent):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.energy = PREY_ENERGY_START
        self.cos_half_vision = math.cos(self.vision_angle / 2)

class Predator(PredatorAgent):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.energy = PREDATOR_ENERGY_START
        self.cos_half_vision = math.cos(self.vision_angle / 2)
