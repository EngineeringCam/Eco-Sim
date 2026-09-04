import sys
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from world import World

class main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ecosystem")
    clock = pygame.time.Clock()

    world = World()
    world.populate()

    font = pygame.font.SysFont(None, 24)

    running = True
    while running:
        # --- events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # add simple key controls (optional)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.k_r:
                    # reset
                    world = World()
                    world.populate()
        
        # --- update
        world.update()

        # --- draw
        screen.fill((30, 30, 30))
        world.draw(screen)

        # HUD: population counts
        text = f"Plants: {len(world.plants)} Prey: {len(world.prey)} Predators: {len(world.predators)}"
        img = font.render(text, True, (240, 240, 240))
        screen.blit(img, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

    if __name__ == "__main__":
        main()
        