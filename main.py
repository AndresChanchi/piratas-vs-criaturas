import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FPS, WINDOW_TITLE
from player import Player

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    player = Player(scale=1.5)  # Valor
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic
        keys = pygame.key.get_pressed()
        player.update(keys)

        # Drawing
        screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(screen)
        pygame.display.flip()

        # Tick
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
