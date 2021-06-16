import random
from settings import *


class Bullet(game.sprite.Sprite):
    def __init__(self, x, y, laser_img):
        game.sprite.Sprite.__init__(self)
        self.laser_img = laser_img
        self.image = game.transform.scale(laser_img, (10, 30))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()
