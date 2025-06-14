import pygame
import os

from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Key mapping for firing:
KEY_SCHEMES = {
    "wasd": {"forward": pygame.K_j, "lateral": pygame.K_k, "mortar": pygame.K_l},
    "arrows": {"forward": pygame.K_SPACE, "lateral": pygame.K_v, "mortar": pygame.K_b}
}

# Mapping direction to folder names (subfolders for lateral up/down)
FOLDER_MAP = {
    'forward': os.path.join('weapons', 'cannon_forward'),
    'up': os.path.join('weapons', 'cannon_lateral', 'lateral_up'),
    'down': os.path.join('weapons', 'cannon_lateral', 'lateral_down'),
    'mortar': os.path.join('weapons', 'mortar')
}

class Cannon(pygame.sprite.Sprite):
    """
    A basic cannon that fires projectiles and shows a brief firing animation.
    """
    def __init__(self, parent, direction='forward', offset=(0, 0), scale=1.0, scheme='wasd'):
        super().__init__()
        self.parent = parent
        self.direction = direction  # 'forward', 'up', 'down', or 'mortar'
        self.offset = offset
        self.scale = scale
        self.scheme = KEY_SCHEMES[scheme]

        # Determine folder for this cannon
        folder = os.path.join('assets', 'images', FOLDER_MAP[direction])
        # Load all png files in folder
        files = sorted([f for f in os.listdir(folder) if f.lower().endswith('.png')])
        if not files:
            raise FileNotFoundError(f"No images found for cannon '{direction}' in {folder}")

        # Static image: use first file as default appearance
        static_path = os.path.join(folder, files[0])
        img = pygame.image.load(static_path).convert_alpha()
        w = int(img.get_width() * scale)
        h = int(img.get_height() * scale)
        self.static_image = pygame.transform.scale(img, (w, h))
        self.image = self.static_image
        self.rect = self.image.get_rect()

        # Load fire animation frames: assume files[0]..[n] indicate animation
        self.fire_frames = []
        for fname in files:
            path = os.path.join(folder, fname)
            frame = pygame.image.load(path).convert_alpha()
            fw = int(frame.get_width() * scale)
            fh = int(frame.get_height() * scale)
            self.fire_frames.append(pygame.transform.scale(frame, (fw, fh)))

        self.firing = False
        self.frame_index = 0
        self.frame_speed = 0.2

        # Cooldown control
        self.cooldown = 500  # ms
        self.last_shot_time = 0

    def update(self, current_time, key_state):
        # Position cannon on parent
        self.rect.centerx = self.parent.rect.x + self.offset[0]
        self.rect.centery = self.parent.rect.y + self.offset[1]

        # Determine firing key
        if self.direction == 'forward': fire_key = self.scheme['forward']
        else: fire_key = self.scheme['lateral']  # up/down share same key
        if self.direction == 'mortar': fire_key = self.scheme['mortar']

        # Handle input & cooldown
        fire_pressed = False
        if self.direction == 'forward':
            fire_pressed = key_state[pygame.K_j] or key_state[pygame.K_SPACE]
        elif self.direction == 'up':
            fire_pressed = key_state[pygame.K_k] or key_state[pygame.K_v]
        elif self.direction == 'down':
            fire_pressed = key_state[pygame.K_l] or key_state[pygame.K_b]
        else:  # mortar
            fire_pressed = key_state[pygame.K_n] or key_state[pygame.K_i]

        if fire_pressed and current_time - self.last_shot_time >= self.cooldown:
            return self._start_firing(current_time)

        # Animate firing if active
        if self.firing:
            self.frame_index += self.frame_speed
            if self.frame_index >= len(self.fire_frames):
                self.firing = False
                self.frame_index = 0
                self.image = self.static_image
            else:
                self.image = self.fire_frames[int(self.frame_index)]
        else:
            self.image = self.static_image

        # On fire start, spawn projectiles
        # Note: can integrate return here if needed

    def _start_firing(self, current_time):
        self.firing = True
        self.frame_index = 0
        self.last_shot_time = current_time
        return self.fire_projectiles()

    def fire_projectiles(self):
        """Return list of CannonBall instances based on direction."""
        from weapon import CannonBall
        velocities = {
            'forward': [(10, 0)],
            'up': [(0, -10)],
            'down': [(0, 10)],
            'mortar': [(8, -8)]
        }
        projectiles = []
        for vel in velocities.get(self.direction, []):
            cb = CannonBall(self.rect.center, vel)
            projectiles.append(cb)
        return projectiles

class CannonBall(pygame.sprite.Sprite):
    """
    Projectile fired by Cannon. Automatically kills itself off-screen.
    """
    def __init__(self, pos, velocity):
        super().__init__()
        img = pygame.image.load('assets/images/weapons/cannon_ball.png').convert_alpha()
        self.image = img
        self.rect = self.image.get_rect(center=pos)
        self.velocity = pygame.math.Vector2(velocity)

    def update(self, *args):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if not pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).colliderect(self.rect):
            self.kill()
