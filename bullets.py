import pygame


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, imgPath):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imgPath)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self, alien_group, explosion_group, explosion_fx):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            from explosion import Explosion
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_fx.play()
            explosion_group.add(explosion)
