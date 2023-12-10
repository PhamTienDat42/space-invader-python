import pygame
import random
from pygame import mixer

from alienbullets import AlienBullets
from aliens import Aliens
from spaceship import SpaceShip

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

# define colors
white = (255, 255, 255)

clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

rows = 5
cols = 5

# bullet cooldown in milliseconds
alien_cooldown = 1000
last_alien_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
# 0 is no game over, 1 means player has won, -1 means player has lost
game_over = 0
start_countdown = False

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Alien Shooter')

# load img
bg = pygame.image.load("img/bg.png")

# define fonts
font20 = pygame.font.SysFont('Constantia', 20)
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

# load sounds
explosion_fx = pygame.mixer.Sound("img/explosion.wav")
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound("img/explosion2.wav")
explosion2_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("img/laser.wav")
laser_fx.set_volume(0.25)


def draw_bg():
    screen.blit(bg, (0, 0))


# define function for creating text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_text_blinking(text, font, text_col, x, y, blink_speed=500):
    current_time = pygame.time.get_ticks()
    blink_state = (current_time // blink_speed) % 2 == 0  # Điều này tạo ra hiệu ứng nhấp nháy

    if blink_state:
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))


spaceship_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()


# create player
def create_player():
    global spaceship
    spaceship = SpaceShip(int(screen_width / 2), screen_height - 100, 3)
    spaceship_group.add(spaceship)


create_player()


def reset_game():
    spaceship_group.empty()
    bullet_group.empty()
    alien_group.empty()
    alien_bullet_group.empty()
    explosion_group.empty()

    create_aliens()
    create_player()


def create_aliens():
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)


create_aliens()

run = True
while run:
    clock.tick(fps)

    # draw background
    draw_bg()

    if countdown == 0:
        time_now = pygame.time.get_ticks()
        # shoot
        if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
            attacking_alien = random.choice(alien_group.sprites())
            alien_bullet = AlienBullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bullet_group.add(alien_bullet)
            last_alien_shot = time_now

        # check if all the aliens have been killed
        if len(alien_group) == 0:
            game_over = 1

        if game_over == 0:
            # update spaceship
            game_over = spaceship.update(screen_width, screen, laser_fx, bullet_group, explosion_group)

            # update sprite groups
            bullet_group.update(alien_group, explosion_group, explosion_fx)
            alien_group.update()
            alien_bullet_group.update(screen_height, spaceship_group, spaceship, explosion2_fx, explosion_group)
        else:
            draw_text_blinking('Press Enter To Play Again!!!', font20, white,
                               int(screen_width / 2 - 100),
                               int(screen_height / 2 + 50))
            if game_over == -1:
                draw_text('GAME OVER!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 100))
            if game_over == 1:
                draw_text('YOU WIN!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 100))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                reset_game()
                countdown = 3
                last_count = pygame.time.get_ticks()
                game_over = 0
                start_countdown = False
                last_alien_shot = pygame.time.get_ticks()

    if start_countdown == False:
        draw_text_blinking('Press Enter To Play!', font20, white,
                           int(screen_width / 2 - 100),
                           int(screen_height / 2 + 50))

    if countdown > 0 and start_countdown:
        draw_text('GET READY!', font40, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
        draw_text(str(countdown), font40, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer

    explosion_group.update()

    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)

    pygame.display.update()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            start_countdown = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()

pygame.quit()
