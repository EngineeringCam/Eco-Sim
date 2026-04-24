import random
import pygame
import math
from utils import in_vision_cone
from agents import Plant, Prey, Predator
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLANT_COUNT, PREY_COUNT, PREDATOR_COUNT, EAT_RADIUS, PLANT_ENERGY,
    PREY_REPRODUCE_THRESHOLD, PREDATOR_REPRODUCE_THRESHOLD, MOVEMENT_COST, SHOW_VISION_CONES
)
from utils import distance, clamp

def draw_vision_cone(agent, screen, color=(255,255,0)):
    steps = max(3, int(agent.vision_angle * 10))  # scale detail with angle
    base_angle = math.atan2(agent.facing[1], agent.facing[0])

    points = [(agent.x, agent.y)]
    for i in range(steps + 1):
        a = base_angle - agent.vision_angle/2 + i * agent.vision_angle / steps
        x = agent.x + agent.vision_distance * math.cos(a)
        y = agent.y + agent.vision_distance * math.sin(a)
        points.append((x, y))

    pygame.draw.polygon(screen, color, points, 1)

class World:
    def __init__(self):
        self.plants = []
        self.prey = []
        self.predators = []
        self.tick_count = 0

    def populate(self):
        for _ in range(PLANT_COUNT):
            self.plants.append(Plant(random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT)))
        for _ in range(PREY_COUNT):
            self.prey.append(Prey(random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT)))
        for _ in range(PREDATOR_COUNT):
            self.predators.append(Predator(random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT)))

    def update(self):
        self.tick_count += 1
        self.move_agents()
        self.handle_eating()
        self.handle_reproduction_and_death()

        # occasional plant regrowth
        if self.tick_count % 5 == 0:
            self.spawn_plant()

    def move_agents(self):
        #Prey move
        for c in self.prey:
            target = None
            closest_dist = float("inf")

            for plant in self.plants:
                if in_vision_cone(c, plant):
                    d = distance(c, plant)
                    if d < closest_dist:
                        closest_dist = d
                        target = plant

            if target:
                # turn toward target
                dx = target.x - c.x
                dy = target.y - c.y
                dist = math.hypot(dx, dy)
                if dist > 0:
                    c.facing = [dx / dist, dy / dist]
            else:
                c.move_random()

            c.x += c.facing[0] * c.speed
            c.y += c.facing[1] * c.speed

            # pay movement cost
            c.energy -= MOVEMENT_COST

            # clamp to screen
            c.x = clamp(c.x, 0, SCREEN_WIDTH -1)
            c.y = clamp(c.y, 0, SCREEN_HEIGHT - 1)

        # Predators move
        for c in self.predators:
            target = None
            closest_dist = float("inf")

            for prey in self.prey:
                if in_vision_cone(c, prey):
                    d = distance(c, prey)
                    if d < closest_dist:
                        closest_dist = d
                        target = prey

            if target:
                # turn toward target
                dx = target.x - c.x
                dy = target.y - c.y
                dist = math.hypot(dx, dy)
                if dist > 0:
                    c.facing = [dx / dist, dy / dist]
            else:
                # wander if nothing seen
                c.move_random()

            c.x += c.facing[0] * c.speed
            c.y += c.facing[1] * c.speed
            c.energy -= MOVEMENT_COST

            c.x = clamp(c.x, 0, SCREEN_WIDTH - 1)
            c.y = clamp(c.y, 0, SCREEN_HEIGHT - 1)

    #def turn_to_target(target, c)
     #   dx

    def handle_eating(self):
        # Prey eat plants
        for prey in list(self.prey):
            for plant in list(self.plants):
                dx = prey.x - plant.x
                dy = prey.y - plant.y
                if dx*dx + dy*dy < EAT_RADIUS * EAT_RADIUS:
                    prey.energy += PLANT_ENERGY
                    try:
                        self.plants.remove(plant)
                    except ValueError:
                        pass
                    break # one plant per tick
        
        # Predators eat prey
        for predator in list(self.predators):
            for prey in list(self.prey):
                dx = predator.x - prey.x
                dy = predator.y - prey.y
                if dx*dx + dy*dy < EAT_RADIUS * EAT_RADIUS:
                    predator.energy += prey.energy // 2 # predator gains some of prey's energy
                    try:
                        self.prey.remove(prey)
                    except ValueError:
                        pass
                    break

    def handle_reproduction_and_death(self):
        # Prey reproduction and death
        for prey in list(self.prey):
            if prey.energy <= 0:
                try:
                    self.prey.remove(prey)
                except ValueError:
                    pass
                continue
            if prey.energy >= PREY_REPRODUCE_THRESHOLD:
                prey.energy //= 2
                child = Prey(prey.x + random.randint(-5, 5), prey.y + random.randint(-5, 5))
                self.prey.append(child)

        # Predator reproduction and death
        for predator in list(self.predators):
            if predator.energy <= 0:
                try:
                    self.predators.remove(predator)
                except ValueError:
                    pass
                continue
            if predator.energy >= PREDATOR_REPRODUCE_THRESHOLD:
                predator.energy //= 2
                child = Predator(predator.x + random.randint(-5, 5), predator.y + random.randint(-5, 5))
                self.predators.append(child)

    def spawn_plant(self):
        # add one plant at random Location
        self.plants.append(Plant(random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT)))

    def draw(self, screen):
        # draw plants
        for plant in self.plants:
            pygame.draw.circle(screen, (20, 150, 20), (int(plant.x), int(plant.y)), 3)

        #draw prey
        for prey in self.prey:
            pygame.draw.circle(screen, (50, 120, 230), (int(prey.x), int(prey.y)), 6)
            if SHOW_VISION_CONES:
                draw_vision_cone(prey, screen)

        for predator in self.predators:
            pygame.draw.circle(screen, (200, 30, 30), (int(predator.x), int(predator.y)), 8)
            if SHOW_VISION_CONES:
                draw_vision_cone(predator, screen)