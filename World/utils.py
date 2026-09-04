import math
import random

from settings import EAT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT, MOVEMENT_COST, SPRINT_COST

def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

def clamp(val, low, high):
    return max(low, min(high, val))

def in_vision_cone(agent, target):
    # Vector from agent to target
    dx = target.x - agent.x
    dy = target.y - agent.y

    dist_sq = dx*dx + dy*dy
    if dist_sq == 0 or dist_sq > agent.vision_distance**2:
        return False
    
    inv_dist = 1 / math.sqrt(dist_sq)
    to_target = (dx * inv_dist, dy * inv_dist)

    dot = (
        agent.facing[0] * to_target[0] +
        agent.facing[1] * to_target[1]
    )

    return dot >= agent.cos_half_vision

def handle_turning(agent, target, turn_towards):
    if turn_towards == True:
        dx = target.x - agent.x
        dy = target.y - agent.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            agent.facing = [dx / dist, dy / dist]
    else:
        dx = agent.x - target.x
        dy = agent.y - target.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            agent.facing = [dx / dist, dy / dist]

def die(agent, agent_list):
        if agent.energy <= 0:
            try:
                agent_list.remove(agent)
            except ValueError:
                pass
            return True
        
        return False

def reproduce(agent, agent_list, reproduction_age, reproduction_time, agent_class):
        if agent.age >= reproduction_age:
            if agent.reproduceTimer >= reproduction_time:

                # Take half of the parent's energy
                agent.energy //= 2

                # Create the child near the parent
                child = agent_class(
                    agent.x + random.randint(-5, 5),
                    agent.y + random.randint(-5, 5)
                )

                agent_list.append(child)

                # Reset reproduction timer
                agent.reproduceTimer = 0

def eat(eater, food, food_list, energy):
        dx = eater.x - food.x
        dy = eater.y - food.y

        if dx * dx + dy * dy < EAT_RADIUS * EAT_RADIUS:
            eater.energy += energy

            try:
                food_list.remove(food)
            except ValueError:
                pass

            return True

        return False

def move_at_speed(agent, speed, sprinting):
    agent.x += agent.facing[0] * speed
    agent.y += agent.facing[1] * speed

    if sprinting:
        agent.energy -= 2 * SPRINT_COST
    else:
        # pay movement cost
        agent.energy -= MOVEMENT_COST

    # clamp to screen
    agent.x = clamp(agent.x, 0, SCREEN_WIDTH - 1)
    agent.y = clamp(agent.y, 0, SCREEN_HEIGHT - 1)
