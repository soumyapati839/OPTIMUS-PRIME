import pygame
import random
import math
from pygame import mixer


pygame.init()
# CALLING PYGAME GUI
screen = pygame.display.set_mode((800, 600))

# TITLE AND WINDOW
pygame.display.set_caption("optimus prime")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
# BACKGROUND
background = pygame.image.load("background.png")
#BACKGROUND SOUND
mixer.music.load('bagr_sound.wav')
mixer.music.play(-1)

# PLAYER
playerimg = pygame.image.load("OP.png")
playerX = 370
playerY = 500
playerX_change = 0
playerY_change = 0

# ENEMY
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_enemy = 8
for i in range(no_enemy):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# BULLET
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 8
bulletX_state = "ready"

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textx = 10
texty = 10


def show_score(x, y):
    score = font.render("score :" + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bulletX_state
    bulletX_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# GAME RUNNING LOOP
running = True
while running:
    # RGB COLOR = RED,GREEN,BLUE
    screen.fill((255, 255, 255))
    # BACKGROUND ING
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # key press is working or not
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_a:
                playerX_change = -5

            if event.key == pygame.K_d:
                playerX_change = +5

            if event.key == pygame.K_SPACE:
                if bulletX_state is "ready":
                    bullet_sound=mixer.Sound("shoot.wav")
                    bullet_sound.play()
                    #get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    playerX = playerX + playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(no_enemy):
        enemyX[i] = enemyX[i] + enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3.5
            enemyY[i] += enemyY_change[i]
        # COLLISION
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("kill.wav")
            collision_sound.play()
            bulletY = 480
            bulletX_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # BULLET MOVEMENT
    if bulletY <= 0:
        bulletY = 480
        bulletX_state = "ready"
    if bulletX_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textx, texty)
    pygame.display.update()
