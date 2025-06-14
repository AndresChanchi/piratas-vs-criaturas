import pygame


def handle_projectile_enemy_collisions(projectiles, enemies):
    """
    Detecta colisiones entre proyectiles y enemigos.
    Cada proyectil que impacta causa daño al enemigo y se destruye.
    Si el enemigo queda "death", se elimina del grupo.
    """
    # iterar copia de proyectiles para evitar modificar durante la iteración
    for projectile in projectiles.sprites():
        hits = pygame.sprite.spritecollide(projectile, enemies, False)
        if hits:
            for enemy in hits:
                # Asumimos que projectile tiene atributo damage
                damage = getattr(projectile, 'damage', 1)
                enemy.take_damage(damage)
                # Eliminar el proyectil
                projectile.kill()
                # Si muere, ejecutar animación de muerte y luego kill
                if enemy.state == 'death':
                    # Opcional: podría esperar a que termine death animation
                    enemy.kill()


def handle_player_enemy_collisions(player, enemies):
    """
    Detecta colisiones entre el jugador y enemigos.
    Si chocan, el jugador recibe daño y el enemigo se destruye.
    """
    hits = pygame.sprite.spritecollide(player, enemies, False)
    for enemy in hits:
        # Asumimos que player tiene método take_damage o atributo health
        damage = getattr(enemy, 'damage', 1)
        # Siempre invocamos take_damage; asegúrate de que Player lo implemente.
        player.take_damage(damage)
        # Elimina enemigo tras colisión
        enemy.kill()
