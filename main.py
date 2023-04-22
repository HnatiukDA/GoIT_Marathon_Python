import pygame
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT, K_w, K_s, K_a, K_d
import random

pygame.init()

FPS = pygame.time.Clock()

# Dysplay size
HEIGHT = 800
WIDTH = 1200

# Text
FONT = pygame.font.SysFont("Comic Sans", 30)

# Colors
COLOR_WHITE = ('#ffffff')
COLOR_BLACK = ('#000000')
COLOR_RED = ('#ff0000')
COLOR_GREEN = ('#00ff00')
COLOR_GOLD = ('#ffd700')

main_dysplay = pygame.display.set_mode((WIDTH, HEIGHT))

# Resources
PLAYER_IMAGE = "res/player.png"

PLAYER_IMAGE_PATH = "res/Goose"
PLAYER_IMAGES = os.listdir(PLAYER_IMAGE_PATH)
CLOUD_IMAGE = "res/cloud.png"
ENEMY_IMAGE = "res/enemy.png"
BONUS_IMAGE = "res/bonus.png"


bg = pygame.transform.scale(pygame.image.load(
    "res/background.png"), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

# Set up player
player_size = [182, 76]
player_position = (WIDTH/9 - player_size[0]/2, HEIGHT/2 - player_size[1]/2)
# player = pygame.Surface(player_size)
# player.fill(COLOR_BLACK)
player = pygame.image.load(PLAYER_IMAGE)
player_rect = pygame.Rect(*player_position, *player_size)
# player_rect = pygame.Rect(WIDTH/2 - player_size(1)/2, HEIGHT/2 - player_size(2)/2 )
player_speed = (0, 0)


# Events
CHANGE_PLAYER_IMAGE = pygame.USEREVENT + 1
pygame.time.set_timer(CHANGE_PLAYER_IMAGE, 200)

CREATE_ENEMY = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_ENEMY, 1500)

enemies = []

CREATE_BONUS = pygame.USEREVENT + 3
pygame.time.set_timer(CREATE_BONUS, 3500)

bonuses = []

CREATE_CLOUD = pygame.USEREVENT + 4
pygame.time.set_timer(CREATE_CLOUD, 500)

clouds = []

score = 0

image_index = 0

# Control
player_move_down = (0, 4)
player_move_up = (0, -4)
player_move_right = (4, 0)
player_move_left = (-4, 0)


# Functions
# Set up enemy
def create_cloud():
    cloud_size = [100, 72]
    cloud_position = (WIDTH + cloud_size[0],
                      random.randint(0, int(HEIGHT/8) - cloud_size[1]))
    cloud = pygame.image.load(CLOUD_IMAGE)
    cloud_rect = pygame.Rect(*cloud_position, *cloud_size)
    cloud_speed = [random.randint(-7, -2), 0]
    return [cloud, cloud_rect, cloud_speed]


def create_enemy():
    enemy_size = [205, 72]
    enemy_position = (WIDTH + enemy_size[0],
                      random.randint(int(HEIGHT/8), HEIGHT - int(HEIGHT/5) - enemy_size[1]))
    enemy = pygame.image.load(ENEMY_IMAGE)
    enemy_rect = pygame.Rect(*enemy_position, *enemy_size)
    enemy_speed = [random.choice([-6, -5, -4, -2, -1]), 0]
    return [enemy, enemy_rect, enemy_speed]


# Set up bonus
def create_bonus():
    bonus_size = [179, 298]
    bonus_position = (random.randint(
        int(WIDTH/8) + player_size[0], WIDTH - bonus_size[0]), -bonus_size[1])
    bonus = pygame.image.load(BONUS_IMAGE)
    bonus_rect = pygame.Rect(*bonus_position, *bonus_size)
    bonus_speed = [random.randint(-1, 0), random.randint(1, 2)]
    return [bonus, bonus_rect, bonus_speed]


while True:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CREATE_CLOUD:
            clouds.append(create_cloud())
        if event.type == CHANGE_PLAYER_IMAGE:
            player = pygame.image.load(os.path.join(
                PLAYER_IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= (len(PLAYER_IMAGES) - 1):
                image_index = 0
    print(len(PLAYER_IMAGES))
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()
    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_dysplay.blit(bg, (bg_X1, 0))
    main_dysplay.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    # Player control
    if (keys[K_DOWN] or keys[K_s]) and player_rect.bottom < (HEIGHT - HEIGHT/5 - player_size[1]):
        player_rect = player_rect.move(player_move_down)

    if (keys[K_UP] or keys[K_w]) and player_rect.top > (HEIGHT/8):
        player_rect = player_rect.move(player_move_up)

    if (keys[K_RIGHT] or keys[K_d]) and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if (keys[K_LEFT] or keys[K_a]) and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    main_dysplay.blit(player, player_rect)
    player_rect = player_rect.move(player_speed)

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_dysplay.blit(bonus[0], bonus[1])
        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1

    for cloud in clouds:
        cloud[1] = cloud[1].move(cloud[2])
        main_dysplay.blit(cloud[0], cloud[1])

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_dysplay.blit(enemy[0], enemy[1])
        if player_rect.colliderect(enemy[1]):
            enemies.pop(enemies.index(enemy))
            score -= 10
            if score < 0:
                score = 0

    main_dysplay.blit(FONT.render(str(score), True,
                      COLOR_GOLD), (WIDTH - 50, 40))

    pygame.display.flip()

    for cloud in clouds:
        if cloud[1].right < 0:
            clouds.pop(clouds.index(cloud))

    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
