import pygame
import os
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    """
    Clase base para todos los enemigos, maneja animaciones, estados, vida y despawn.
    """
    def __init__(self, x, y, scale=1.0, speed=2, health=1, damage=1, folder=""):
        super().__init__()
        self.scale = scale
        self.speed = speed
        self.health = health
        self.damage = damage
        self.state = 'swim'  # 'swim', 'attack', 'hurt', 'death'
        self.animations = {}
        self.frame_index = 0
        self.frame_speed = 0.15
        self.base_folder = folder
        self.load_animations(self.base_folder)

        swim_frames = self.animations.get('swim', [])
        if not swim_frames:
            raise FileNotFoundError(
                f"No swim frames found for enemy '{self.base_folder}' in assets/images/characters/enemies/{self.base_folder}/swim"
            )

        self.image = swim_frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))

    def load_animations(self, base_folder):
        """Carga animaciones para cada estado: swim, attack, hurt, death."""
        root = os.path.join('assets', 'images', 'characters', 'enemies', base_folder)
        for state in ['swim', 'attack', 'hurt', 'death']:
            path = os.path.join(root, state)
            frames = []
            if os.path.isdir(path):
                files = sorted([f for f in os.listdir(path) if f.endswith('.png')])
                for fname in files:
                    img_path = os.path.join(path, fname)
                    try:
                        img = pygame.image.load(img_path).convert_alpha()
                    except Exception:
                        continue
                    w = int(img.get_width() * self.scale)
                    h = int(img.get_height() * self.scale)
                    frames.append(pygame.transform.scale(img, (w, h)))
            self.animations[state] = frames

    def update(self, player):
        """Actualiza animación, movimiento y despawn fuera de pantalla."""
        self.animate()
        self.move(player)
        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        if not screen_rect.colliderect(self.rect):
            self.kill()

    def animate(self):
        """Reproduce la animación del estado actual."""
        frames = self.animations.get(self.state, [])
        if not frames:
            return
        self.frame_index = (self.frame_index + self.frame_speed) % len(frames)
        self.image = frames[int(self.frame_index)]

    def move(self, player):
        """Movimiento por defecto, a sobrescribir en subclases."""
        pass

    def take_damage(self, amount):
        self.health -= amount
        self.state = 'death' if self.health <= 0 else 'hurt'

# ---------------------------------------------
# Clases específicas de enemigos con polimorfismo
# ---------------------------------------------
class Anguila(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, scale=1.0, speed=3, health=2, damage=1, folder='anguila')
    def move(self, player):
        # Mueve horizontal de izquierda a derecha
        self.rect.x += self.speed
        # Estado de ataque si alineado horizontalmente con el jugador
        if abs(self.rect.centery - player.rect.centery) < 20:
            self.state = 'attack'
        else:
            self.state = 'swim'

class Tiburon(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, scale=1.0, speed=2, health=3, damage=2, folder='tiburon')
    def move(self, player):
        # Mueve horizontal de derecha a izquierda
        self.rect.x -= self.speed
        # Estado de ataque si alineado horizontalmente con el jugador
        if abs(self.rect.centery - player.rect.centery) < 20:
            self.state = 'attack'
        else:
            self.state = 'swim'

class Medusa(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, scale=1.0, speed=3, health=3, damage=1, folder='medusa')
    def move(self, player):
        # Se mueve vertical de forma aleatoria arriba-abajo
        if random.choice([True, False]):
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed
        self.state = 'swim'

class BossFish(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, scale=1.5, speed=1, health=20, damage=3, folder='boss_fish')
    def move(self, player):
        # Persigue al jugador lentamente
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(1, (dx*dx + dy*dy)**0.5)
        self.rect.x += int(self.speed * dx/dist)
        self.rect.y += int(self.speed * dy/dist)
        self.state = 'swim'
        # Flip horizontal para mirar al jugador
        if dx < 0:
            self.image = pygame.transform.flip(self.image, True, False)

# ---------------------------------------------
# Spawner de enemigos
# ---------------------------------------------
class EnemyManager:
    def __init__(self, group, player):
        self.group = group
        self.player = player
        self.spawn_timer = 0       # para normales
        self.total_timer = 0       # para jefe
        self.boss_spawned = False

    def update(self, dt):
        """Genera enemigos comunes y jefe con posiciones de spawn ajustadas."""
        self.spawn_timer += dt
        self.total_timer += dt
        # Spawn cada 2s hasta 210s (3m30s)
        if 2000 <= self.spawn_timer < 5000:
            enemy_cls = random.choice([Anguila, Tiburon, Medusa])
            # Posición inicial según tipo de enemigo
            if enemy_cls is Anguila:
                x = 0  # nace en borde izquierdo dentro de pantalla
                y = random.randint(0, SCREEN_HEIGHT - 48)
            elif enemy_cls is Tiburon:
                x = SCREEN_WIDTH  # nace en borde derecho dentro de pantalla
                y = random.randint(0, SCREEN_HEIGHT - 48)
            else:  # Medusa
                x = random.randint(0, SCREEN_WIDTH - 48)
                # puede nacer arriba o abajo del área
                y = 0 if random.choice([True, False]) else SCREEN_HEIGHT - 48
            enemy = enemy_cls(x, y)
            self.group.add(enemy)
            self.spawn_timer = 0
        # Boss al minuto 1 (60000ms)
        if self.total_timer >= 60000 and not self.boss_spawned:
            boss = BossFish(x=SCREEN_WIDTH + 100, y=SCREEN_HEIGHT // 2)
            self.group.add(boss)
            self.boss_spawned = True
