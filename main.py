import pygame, sys
from constants import *
from player import Player
from weapon import Cannon
from menu import menu_loop, pause_menu
from collisions import (
    handle_projectile_enemy_collisions,
    handle_player_enemy_collisions
)

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

    # --- Grupos de enemigos ---
    from enemy import EnemyManager, Anguila, Tiburon, Medusa, BossFish

    enemies = pygame.sprite.Group()
    enemy_manager = EnemyManager(enemies, player)

    projectiles = pygame.sprite.Group()
    all_cannons = pygame.sprite.Group()

    # --- Instanciación de cañones ---
    # Cañones laterales arriba, logica de weapon, al carajo la modularización y signle of truth
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
        dt = clock.tick(FPS)
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
        enemies.update(player)

        current_time = pygame.time.get_ticks()
        key_state = pygame.key.get_pressed()
        # Actualiza cañones y dispara
        for cannon in all_cannons:
            shots = cannon.update(current_time, key_state)
            if shots:
                for shot in shots:
                    projectiles.add(shot)

        projectiles.update()

        # --- Lógica de enemigos ---
        enemy_manager.update(dt)      # crea nuevos enemigos cuando toca
        enemies.update(player)        # mueve y anima a cada enemigo

        #colisiones
        handle_projectile_enemy_collisions(projectiles, enemies)
        handle_player_enemy_collisions(player, enemies)

        # --- Dibujado ---
        screen.fill(BACKGROUND_COLOR)
        player.draw(screen)
        all_cannons.draw(screen)
        projectiles.draw(screen)

        # ② Barra de salud
        BAR_WIDTH = 100
        BAR_HEIGHT = 10
        bar_x = player.rect.centerx - BAR_WIDTH // 2
        bar_y = player.rect.top - BAR_HEIGHT - 5
        health_ratio = player.health / player.max_health
        # fondo gris
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, BAR_WIDTH, BAR_HEIGHT))
        # salud verde
        pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, int(BAR_WIDTH * health_ratio), BAR_HEIGHT))

        # ③ Botón de pausa y flip
        screen.blit(pause_img, pause_rect)
        pygame.display.flip()

        # --- Dibujar enemigos ---
        enemies.draw(screen)

        screen.blit(pause_img, pause_rect)
        pygame.display.flip()

        # --- GAME OVER ---
        if player.health <= 0:
            font = pygame.font.SysFont(None, 72)
            text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(3000)  # Espera 3 segundos
            return menu_loop(main)  # Regresa al menú principal

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.init()
    menu_loop(main)