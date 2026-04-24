import math

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