from os import path
from star import Star
from player import Player
from mobs import *


WIDTH = 600
HEIGHT = 600
FPS = 120


# запускаем окно
game.init()
game.mixer.init()  # для звука
screen = game.display.set_mode((WIDTH, HEIGHT))
game.display.set_caption("My Game")
clock = game.time.Clock()

# загрузка спрайтов
img_folder = path.join(path.dirname(__file__), "sprites")
player_img = game.image.load(path.join(img_folder, "playerShip3_green.png"))
meteor_imgs = [
    game.image.load(path.join(img_folder, "m1.png")),
    game.image.load(path.join(img_folder, "m2.png")),
    game.image.load(path.join(img_folder, "m3.png")),
    game.image.load(path.join(img_folder, "m4.png")),
]
laser_img = game.image.load(path.join(img_folder, "laserRed13.png"))

bg = game.image.load(path.join(img_folder, "bg.jpg")).convert()
bg_rect = bg.get_rect()

# загрузка звуков
snd_folder = path.join(path.dirname(__file__), "snd")
shoot_snd = game.mixer.Sound(path.join(snd_folder, "pew.wav"))
exp_snd = game.mixer.Sound(path.join(snd_folder, "expl6.wav"))
game.mixer.music.load(path.join(snd_folder, "music.mp3"))
game.mixer.music.set_volume(0.01)



font_name = game.font.match_font("arial")


def draw_text(surf, text, size, x, y):
    font = game.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmob():
    m = Mob(meteor_imgs)
    all_sprites.add(m)
    mobs.add(m)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct / 100) * bar_length
    outline_rect = game.Rect(x, y, bar_length, bar_height)
    fill_rect = game.Rect(x, y, fill, bar_height)
    game.draw.rect(surf, GREEN, fill_rect)
    game.draw.rect(surf, WHITE, outline_rect, 2)


# добавление спрайтов
player = Player(player_img, shoot_snd, laser_img)
all_sprites.add(player)

for i in range(8):
    newmob()

all_sprites.add([Star() for i in range(50)])


def run():
    # основной цикл
    game.mixer.music.play(loops=-1)
    score = 0
    running = True
    paused = False
    while running:
        clock.tick(FPS)

        for event in game.event.get():
            # проверить закрытие окна
            if event.type == game.QUIT:
                running = False
            elif event.type == game.KEYDOWN:
                if event.key == game.K_SPACE:
                    player.shoot()
                if event.key == game.K_p:
                    paused = not paused

        if not paused:
            # обновление
            all_sprites.update()

            hits = game.sprite.spritecollide(
                player, mobs, True, game.sprite.collide_rect_ratio(0.85)
            )
            for hit in hits:
                newmob()
                player.shield -= hit.rect.width * hit.rect.height // 128
                if player.shield <= 0:
                    running = False

            hits = game.sprite.groupcollide(mobs, bullets, True, True)
            for hit in hits:
                score += 7000 - (hit.rect.width * hit.rect.height)
                exp_snd.play()
                newmob()

            # рендеринг
            screen.fill(BLACK)
            screen.blit(bg, bg_rect)
            all_sprites.draw(screen)
            draw_text(screen, str(score), 18, WIDTH / 2, 40)
            draw_shield_bar(screen, 5, 5, player.shield)
            game.display.flip()

    game.quit()


if __name__ == "__main__":
    run()
