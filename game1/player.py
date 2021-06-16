from bullets import *


class Player(game.sprite.Sprite):
    def __init__(self, player_img, shoot_snd, shoot_img):
        game.sprite.Sprite.__init__(self)
        self.image = game.transform.scale(player_img, (50, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 40
        self.speedx = 0
        self.last_update = game.time.get_ticks()
        self.shoot_snd = shoot_snd
        self.shoot_img = shoot_img
        self.shield = 100

    def update(self):
        self.speedx = 0
        keystate = game.key.get_pressed()
        if keystate[game.K_a]:
            self.speedx = -8
        if keystate[game.K_d]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = game.time.get_ticks()
        if now - self.last_update > 250:
            self.last_update = now
            bullet = Bullet(self.rect.centerx, self.rect.top, self.shoot_img)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.shoot_snd.play()
