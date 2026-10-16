import random
import math
from settings import PREDATOR_REPRODUCTION_TIME, PREY_ENERGY_START, PREDATOR_ENERGY_START, PREY_REPRODUCTION_TIME, MIN_REPRO_TIME, MAX_REPRO_TIME

class Agent:
    def __init__(self, x, y, age, reproduceTimer, reproduction_mean=None):
        self.x = x
        self.y = y
        self.age = age
        self.reproduceTimer = reproduceTimer

        # Each species has its own average reproduction time
        self.reproduction_mean = reproduction_mean

        # Randomly assigned reproduction target
        self.reproTime = None
        if reproduction_mean is not None:
            self.reset_repro_time()

        # facing direction (unit vector)
        angle = random.uniform(0, 2 * math.pi)
        self.facing = [math.cos(angle), math.sin(angle)]

        # vision parameters
        self.vision_distance = 100
        self.vision_angle = math.pi / 2 # 90 degrees

        self.speed = 3

    def reset_repro_time(self):
        minimum = MIN_REPRO_TIME
        maximum = MAX_REPRO_TIME
        mean = self.reproduction_mean

        if mean is None:
            raise ValueError("Agent has no reproduction mean")

        if not minimum <= mean <= maximum:
            raise ValueError("Reproduction mean must be between minimum and maximum")

        # Calculate the mode for the desired average
        mode = 3 * mean - minimum - maximum

        if not minimum <= mode <= maximum:
            raise ValueError("Reproduction mean is incompatible with the triangular distribution bounds")

        self.reproTime = round(random.triangular(minimum, maximum, mode))
        self.reproduceTimer = 0

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
        super().__init__(x, y, age=0, reproduceTimer=0, reproduction_mean=PREY_REPRODUCTION_TIME)
        self.energy = PREY_ENERGY_START

        self.vision_distance = 80
        self.vision_angle = 3 * math.pi / 2 # 270 degrees
        self.walk_speed = 2
        self.sprint_speed = 3
        self.flee_timer = 0
        self.flee_from = None

        isinstance(Agent, Prey)
        self.cos_half_vision = math.cos(self.vision_angle / 2)

class Predator(Agent):
    def __init__(self, x, y):
        super().__init__(x, y, age=0, reproduceTimer=0, reproduction_mean=PREDATOR_REPRODUCTION_TIME)
        self.energy = PREDATOR_ENERGY_START

        self.vision_distance = 120
        self.vision_angle = math.pi / 3 # 60 degrees
        self.walk_speed = 2
        self.sprint_speed = 5

        isinstance(Agent, Predator)
        self.cos_half_vision = math.cos(self.vision_angle / 2)
