import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, x=100, y=100, scale=1.0):
        super().__init__()
        self.animation_frames = []
        self.current_frame = 0
        self.animation_speed = 0.15  # entre menor, más rápido

        self.load_images(scale)
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.speed = 5
        #Gatos, cats montado
        self.cat_frames = [
            pygame.image.load(f"assets/images/characters/cats/PirateCat ({i}).png").convert_alpha()
            for i in range(1, 4)
        ]
        self.cat_index = 0
        self.cat_image = self.cat_frames[self.cat_index]

    def load_images(self, scale):
        image_folder = "assets/images/characters/player"
        for i in range(1, 13):  # 1 a 12 inclusive
            path = os.path.join(image_folder, f"player ({i}).png")
            img = pygame.image.load(path).convert_alpha()

            width = int(img.get_width() * scale)
            height = int(img.get_height() * scale)
            img = pygame.transform.scale(img, (width, height))

            self.animation_frames.append(img)

    def update(self, keys):
        # Movimiento
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Animación
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.animation_frames):
            self.current_frame = 0

        self.image = self.animation_frames[int(self.current_frame)]

        #Animación gato
        self.cat_index = (self.cat_index + 0.1) % len(self.cat_frames)
        self.cat_image = self.cat_frames[int(self.cat_index)]

        # Dibujar
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        # Dibujar gato con offset (5 px a la izquierda, centrado en Y respecto al barco)
        cat_x = self.rect.x + 5
        cat_y = self.rect.y + (self.rect.height // 2 - self.cat_image.get_height() // 2)
        surface.blit(self.cat_image, (cat_x, cat_y))