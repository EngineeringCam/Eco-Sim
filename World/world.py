import random
import pygame
import math
from utils import eat, in_vision_cone, handle_turning, die, reproduce, move_at_speed
from agents import Plant, Prey, Predator
from terrain import Cover
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
        self.cover = []
        self.tick_count = 0

    def populate(self):
        for _ in range(PLANT_COUNT):
            self.plants.append(Plant(random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT)))
        for _ in range(PREY_COUNT):
            self.prey.append(Prey(random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT)))
        for _ in range(PREDATOR_COUNT):
            self.predators.append(Predator(random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT)))

        self.cover.append(Cover(300, 200, 250, 150))
        self.cover.append(Cover(800, 400, 300, 200))
        self.cover.append(Cover(500, 600, 200, 100))

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
                move_at_speed(c, c.sprint_speed, sprinting=True)
                pass
            else:
    
                target = self.find_closest_visible(c, self.plants)
    
                if target:
                    # turn toward target
                    handle_turning(c, target, True)
                    move_at_speed(c, c.walk_speed, sprinting=False)
                else:
                    # wander if nothing seen
                    c.move_random()
                    move_at_speed(c, c.walk_speed, sprinting=False)

        # Predators move
        for c in self.predators:

            target = self.find_closest_visible(c, self.prey)

            if target:
                # turn toward target
                handle_turning(c, target, True)
                move_at_speed(c, c.sprint_speed, sprinting=True)
            else:
                # wander if nothing seen
                c.move_random()
                move_at_speed(c, c.walk_speed, sprinting=False)


    def handle_eating(self):
        # Prey eat plants
        for prey in list(self.prey):
            for plant in list(self.plants):
                if eat(prey, plant, self.plants, PLANT_ENERGY):
                    break  # one plant per tick

        # Predators eat prey
        for predator in list(self.predators):
            for prey in list(self.prey):
                # Predator gets 75% of the prey's energy when it eats it
                energy = prey.energy // 1.5

                if eat(predator, prey, self.prey, energy):
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
            aggitator = self.find_closest_visible(prey, self.predators)

            # If predator is found in vision cone, set flee timer and move away from predator
            if aggitator:
                # Set timer for how long prey will flee
                prey.flee_timer = FLEE_TIMER
                prey.flee_from = aggitator

                # Immediately turn away from predator
                handle_turning(prey, aggitator, False)


    def handle_reproduction_and_death(self):
        # Prey reproduction and death
        for prey in list(self.prey):
            prey.age += 1
            prey.reproduceTimer += 1
    
            if die(prey, self.prey):
                continue
            
            reproduce(
                prey,
                self.prey,
                PREY_REPRODUCTION_AGE,
                PREY_REPRODUCTION_TIME,
                Prey
            )
    
        # Predator reproduction and death
        for predator in list(self.predators):
            predator.age += 1
            predator.reproduceTimer += 1
    
            if die(predator, self.predators):
                continue
            
            reproduce(
                predator,
                self.predators,
                PREDATOR_REPRODUCTION_AGE,
                PREDATOR_REPRODUCTION_TIME,
                Predator
            )


    def find_closest_visible(self, agent, candidates):
        target = None
        closest_dist = float("inf")

        for candidate in candidates:
            if in_vision_cone(agent, candidate, self.cover):
                d = distance(agent, candidate)

                if d < closest_dist:
                    closest_dist = d
                    target = candidate

        return target


    def in_cover(self, agent):
        for cover in self.cover:

            if (cover.x <= agent.x <= cover.x + cover.width) and (cover.y <= agent.y <= cover.y + cover.height):
                return True

        return False


    def has_line_of_sight(self, agent, target):
        if self.in_cover(target) and self.in_cover(agent):
            # agents can see other agents in cover if they are also in cover
            return True

        # Check if the line between agent and target intersects any cover
        for cover in self.cover:
            if self.line_intersects_rect(agent.x, agent.y, target.x, target.y, cover):
                return False  # Line of sight is blocked

        return True  # No cover blocks the line of sight


    def line_intersects_rect(self, x1, y1, x2, y2, rect):
        # Check if the line segment from (x1, y1) to (x2, y2) intersects the rectangle defined by rect
        rect_lines = [
            ((rect.x, rect.y), (rect.x + rect.width, rect.y)),  # Top
            ((rect.x, rect.y), (rect.x, rect.y + rect.height)),  # Left
            ((rect.x + rect.width, rect.y), (rect.x + rect.width, rect.y + rect.height)),  # Right
            ((rect.x, rect.y + rect.height), (rect.x + rect.width, rect.y + rect.height))  # Bottom
        ]

        for (rx1, ry1), (rx2, ry2) in rect_lines:
            if self.lines_intersect(x1, y1, x2, y2, rx1, ry1, rx2, ry2):
                return True

        return False


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


        # Draw cover
        cover_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        for cover in self.cover:
            pygame.draw.rect(cover_surface, (128, 128, 128, 150), (cover.x, cover.y, cover.width, cover.height))

        screen.blit(cover_surface, (0, 0))