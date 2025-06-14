import pygame, sys
from constants import *
from player import Player
from weapon import Cannon
from menu import menu_loop, pause_menu

def main():

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    # --- Botón de pausa ---
    pause_img = pygame.image.load("assets/images/ui/pause_button.png").convert_alpha()
    pause_img = pygame.transform.scale(pause_img, (48, 48))
    pause_rect = pause_img.get_rect(topright=(SCREEN_WIDTH - 10, 10))

    # --- Sprites y grupos ---
    player = Player(x=100, y=SCREEN_HEIGHT//2 - 64, scale=1.5)
    all_sprites = pygame.sprite.Group(player)

    projectiles = pygame.sprite.Group()
    all_cannons = pygame.sprite.Group()

    # --- Instanciación de cañones ---
    # Cañones laterales arriba, logica de weapon, al carajo la modularización
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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                res = pause_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_rect.collidepoint(event.pos):
                    res = pause_menu()
                    if res == "restart":
                        return main()
                    elif res == "home":
                        return menu_loop(main)

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
        player.draw(screen)
        all_cannons.draw(screen)
        projectiles.draw(screen)
        screen.blit(pause_img, pause_rect)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.init()
    menu_loop(main)