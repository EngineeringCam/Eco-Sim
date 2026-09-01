import random
import pygame
import math
from utils import in_vision_cone, handle_turning
from agents import Plant, Prey, Predator
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLANT_COUNT, PREY_COUNT, PREDATOR_COUNT, EAT_RADIUS, PLANT_ENERGY,
    PREY_REPRODUCTION_AGE, PREY_REPRODUCTION_TIME, PREDATOR_REPRODUCTION_AGE, PREDATOR_REPRODUCTION_TIME,
    MOVEMENT_COST, SHOW_VISION_CONES, FLEE_TIMER
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
        self.handle_fleeing()
        self.move_agents()
        self.handle_eating()
        self.handle_reproduction_and_death()

        # occasional plant regrowth
        if self.tick_count % 5 == 0:
            self.spawn_plant()


    def move_agents(self):
        #Prey move
        for c in self.prey:
            if c.flee_timer > 0:
                # already fleeing.
                # Don't Look for food.
                pass
            else:
    
                target = self.find_closest_visible(c, self.plants)
    
                if target:
                    # turn toward target
                    handle_turning(c, target, True)
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

            target = self.find_closest_visible(c, self.prey)

            if target:
                # turn toward target
                handle_turning(c, target, True)
            else:
                # wander if nothing seen
                c.move_random()

            c.x += c.facing[0] * c.speed
            c.y += c.facing[1] * c.speed
            c.energy -= MOVEMENT_COST

            c.x = clamp(c.x, 0, SCREEN_WIDTH - 1)
            c.y = clamp(c.y, 0, SCREEN_HEIGHT - 1)


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

    
    def handle_fleeing(self):
        # Prey flee from predators
        for prey in self.prey:

            # If prey is already fleeing, continue fleeing
            if prey.flee_timer > 0:
                prey.flee_timer -= 1

                # Move directly away from the predator
                handle_turning(prey, prey.flee_from, False)

                continue  # Skip the rest of the loop to keep fleeing

            # If prey is not fleeing, check for predators in vision cone / Look for predators
            aggitator = None
            closest_dist = float("inf")

            for predator in self.predators:
                # Check if predator is in prey's vision cone
                if in_vision_cone(prey, predator):
                    # Check which predator in vision cone is closest
                    d = distance(prey, predator)
                    if d < closest_dist:
                        closest_dist = d
                        aggitator = predator

            # If predator is found in vision cone, set flee timer and move away from predator
            if aggitator:
                # Set timer for how long prey will flee
                prey.flee_timer = FLEE_TIMER
                prey.flee_from = aggitator

                # Immediately turn away from predator
                dx = prey.x - aggitator.x
                dy = prey.y - aggitator.y

                dist = math.hypot(dx, dy)

                if dist > 0:
                    prey.facing = [dx / dist, dy / dist]


    def handle_reproduction_and_death(self):
        # Prey reproduction and death
        for prey in list(self.prey):
            prey.age += 1
            prey.reproduceTimer += 1
            if prey.energy <= 0:
                try:
                    self.prey.remove(prey)
                except ValueError:
                    pass
                continue
            if prey.age >= PREY_REPRODUCTION_AGE:
                if prey.reproduceTimer >= PREY_REPRODUCTION_TIME:
                    prey.energy //= 2
                    child = Prey(prey.x + random.randint(-5, 5), prey.y + random.randint(-5, 5))
                    self.prey.append(child)
                    prey.reproduceTimer = 0

        # Predator reproduction and death
        for predator in list(self.predators):
            predator.age += 1
            predator.reproduceTimer += 1
            if predator.energy <= 0:
                try:
                    self.predators.remove(predator)
                except ValueError:
                    pass
                continue
            if predator.age >= PREDATOR_REPRODUCTION_AGE:
                if predator.reproduceTimer >= PREDATOR_REPRODUCTION_TIME:
                    predator.energy //= 2
                    child = Predator(predator.x + random.randint(-5, 5), predator.y + random.randint(-5, 5))
                    self.predators.append(child)
                    predator.reproduceTimer = 0

    def find_closest_visible(self, agent, candidates):
        target = None
        closest_dist = float("inf")

        for candidate in candidates:
            if in_vision_cone(agent, candidate):
                d = distance(agent, candidate)

                if d < closest_dist:
                    closest_dist = d
                    target = candidate

        return target
    

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