import pygame

from bullets import Bullets


class AlienBullets(Bullets):
    def __init__(self, x, y):
        super().__init__(x, y, "img/alien_bullet.png")

    def update(self, screen_height, spaceship_group, spaceship, explosion2_fx, explosion_group):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            explosion2_fx.play()
            spaceship.health_remaining -= 1
            from explosion import Explosion
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)
