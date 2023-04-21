import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT
import random

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

# Colors
COLOR_WHITE = ('#ffffff')
COLOR_BLACK = ('#000000')
COLOR_RED = ('#ff0000')
COLOR_GREEN = ('#00ff00')
BLINK = ('#101010')
PLAYER_COLOR_PALETTE = [(255, 0, 0), (255, 165, 0), (255, 255, 0),
                        (0, 128, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]

main_dysplay = pygame.display.set_mode((WIDTH, HEIGHT))

# Get random coordinates
random_x = random.randint(1, WIDTH - 1)
random_y = random.randint(1, HEIGHT - 1)


# Set up player
player_size = (25, 25)
player_position = (1, 1)
player = pygame.Surface(player_size)
player.fill(COLOR_WHITE)
player_rect = pygame.Rect(*player_position, *player_size)
player_speed = (0, 0)


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

enemies = []

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

bonuses = []

# Set initial random speed
random_speed_x = random.choice([-1, 1])
random_speed_y = random.choice([-1, 1])

random_palette_color = 0

# Control
player_move_down = (0, 3)
player_move_up = (0, -3)
player_move_right = (3, 0)
player_move_left = (-3, 0)

# Functions
# Set up enemy
def create_enemy():
    enemy_size = (30, 30)
    enemy_position = (WIDTH, random.randint(40, HEIGHT - 40))
    enemy = pygame.Surface(enemy_size)
    enemy.fill(COLOR_RED)
    enemy_rect = pygame.Rect(*enemy_position, *enemy_size)
    enemy_speed = [random.randint(-6, -2), 0]
    return [enemy, enemy_rect, enemy_speed]

# Set up bonus
def create_bonus():
    bonus_size = (20, 20)
    bonus_position = (random.randint(200, WIDTH - 40), -20)
    bonus = pygame.Surface(bonus_size)
    bonus.fill(COLOR_GREEN)
    bonus_rect = pygame.Rect(*bonus_position, *bonus_size)
    bonus_speed = [0, random.randint(1, 2)]
    return [bonus, bonus_rect, bonus_speed]


while True:
    FPS.tick(90)
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

    main_dysplay.fill(COLOR_BLACK)

    keys = pygame.key.get_pressed()

    # Player control
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    main_dysplay.blit(player, player_rect)
    player_rect = player_rect.move(player_speed)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_dysplay.blit(enemy[0], enemy[1])

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_dysplay.blit(bonus[0], bonus[1])

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
