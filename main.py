# main.py

import pygame
import sys

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FPS, WINDOW_TITLE
from player import Player
from weapon import Cannon

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    # --- Sprites y grupos ---
    player = Player(x=100, y=SCREEN_HEIGHT//2 - 64, scale=1.5)
    all_sprites = pygame.sprite.Group(player)

    projectiles = pygame.sprite.Group()
    all_cannons = pygame.sprite.Group()

    # --- Instanciación de cañones ---
    # Cañones laterales arriba
    cannon_up_left = Cannon(
        parent=player,
        direction='up',
        offset=(player.rect.width * 0.25, player.rect.height * 0.2),
        scale=0.5
    )
    cannon_up_right = Cannon(
        parent=player,
        direction='up',
        offset=(player.rect.width * 0.75, player.rect.height * 0.2),
        scale=0.5
    )

    # Cañones laterales abajo
    cannon_down_left = Cannon(
        parent=player,
        direction='down',
        offset=(player.rect.width * 0.25, player.rect.height * 0.8),
        scale=0.5
    )
    cannon_down_right = Cannon(
        parent=player,
        direction='down',
        offset=(player.rect.width * 0.75, player.rect.height * 0.8),
        scale=0.5
    )

    # Cañones frontales (eje X)
    cannon_fwd = Cannon(
        parent=player,
        direction='forward',
        offset=(player.rect.width, player.rect.height * 0.45),
        scale=0.5
    )
    cannon_fwd2 = Cannon(
        parent=player,
        direction='forward',
        offset=(player.rect.width, player.rect.height * 0.55),
        scale=0.5
    )

    all_cannons.add(
        cannon_up_left, cannon_up_right,
        cannon_down_left, cannon_down_right,
        cannon_fwd, cannon_fwd2
    )

    running = True
    while running:
        # --- Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Lógica de juego ---
        keys = pygame.key.get_pressed()
        player.update(keys)

        current_time = pygame.time.get_ticks()
        key_state = pygame.key.get_pressed()
        # Actualiza cañones y dispara
        for cannon in all_cannons:
            shots = cannon.update(current_time, key_state)
            if shots:
                for shot in shots:
                    projectiles.add(shot)

        projectiles.update()

        # --- Dibujado ---
        screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(screen)
        all_cannons.draw(screen)
        projectiles.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
