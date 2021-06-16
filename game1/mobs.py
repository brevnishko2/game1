import random
from settings import *


class Mob(game.sprite.Sprite):
    def __init__(self, meteors_imgs):
        game.sprite.Sprite.__init__(self)
        self.meteor_imgs = meteors_imgs
        self.image = game.transform.scale(
            random.choice(self.meteor_imgs),
            (random.randint(30, 80), random.randint(30, 80)),
        )
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (
            self.rect.top > HEIGHT + 10
            or self.rect.left < -25
            or self.rect.right > WIDTH + 20
        ):
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)
            self.speedx = random.randrange(-3, 3)
