import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE

def load_button(name, x, y, size=48):
    """Carga una imagen de botón y devuelve la imagen escalada y su rect."""
    try:
        img = pygame.image.load(f"assets/images/ui/{name}_button.png").convert_alpha()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {name}_button.png en assets/images/ui/")
        sys.exit()
    img = pygame.transform.scale(img, (size, size))
    rect = img.get_rect(topleft=(x, y))
    return img, rect

def menu_loop(start_callback):
    """Pantalla de inicio (con botones Start y Quit)."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    # Fondo
    try:
        bg = pygame.image.load("assets/images/ui/background_menu.png").convert()
        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except FileNotFoundError:
        print("Error: No se encontró background_menu.png en assets/images/ui/")
        sys.exit()

    # Botones centrados verticalmente con padding entre ellos
    button_width = 100
    button_height = 80
    button_spacing = 30

    # Calcular posiciones centradas horizontalmente
    total_width = button_width * 2 + button_spacing
    start_x = SCREEN_WIDTH // 2 - total_width // 2
    y_pos = SCREEN_HEIGHT // 2 - button_height // 2

    # Cargar imágenes de botones con posición calculada
    start_img, start_rect = load_button("start", start_x, y_pos, size=button_width)
    quit_img, quit_rect = load_button("quit", start_x + button_width + button_spacing, y_pos, size=button_width)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(e.pos):
                    pygame.time.delay(1000)
                    start_callback()
                    return
                elif quit_rect.collidepoint(e.pos):
                    pygame.quit()
                    sys.exit()

        screen.blit(bg, (0, 0))
        screen.blit(start_img, start_rect)
        screen.blit(quit_img, quit_rect)
        pygame.display.flip()
        clock.tick(FPS)

    # Cargar botones centrados verticalmente con separación
    button_size = 100
    button_spacing = 30  # espacio entre los botones

    total_height = 2 * button_size + button_spacing
    start_y = SCREEN_HEIGHT // 2 - total_height // 2

    start_img, start_rect = load_button("start", SCREEN_WIDTH // 2 - button_size // 2, start_y, size=button_size)
    quit_img, quit_rect = load_button("quit", SCREEN_WIDTH // 2 - button_size // 2, start_y + button_size + button_spacing, size=button_size)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and start_rect.collidepoint(e.pos):
                pygame.time.delay(500)
                start_callback()  # Llama a main()
                return

        screen.blit(bg, (0, 0))
        screen.blit(start_img, start_rect)
        pygame.display.flip()
        clock.tick(FPS)

def pause_menu():
    """Menú de pausa que se activa desde main."""
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    # Posición de botones
    pad = 10
    size = 48
    x = SCREEN_WIDTH - size - pad
    y0 = pad

    # Carga de botones
    cont_img, cont_rect = load_button("continue", x, y0)
    rest_img, rest_rect = load_button("restart", x, y0 + (size + pad))
    home_img, home_rect = load_button("home", x, y0 + 2 * (size + pad))

    # Texto de pausa
    paused = True
    font = pygame.font.Font(None, 60)
    text = font.render("PAUSED", True, (255, 255, 255))
    trect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT //  2 - 20))

    while paused:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if cont_rect.collidepoint(e.pos):
                    return "continue"
                elif rest_rect.collidepoint(e.pos):
                    return "restart"
                elif home_rect.collidepoint(e.pos):
                    return "home"

        # Fondo oscuro translúcido
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        screen.blit(text, trect)
        screen.blit(cont_img, cont_rect)
        screen.blit(rest_img, rest_rect)
        screen.blit(home_img, home_rect)

        pygame.display.flip()
        clock.tick(FPS)
