import math
import pygame
import random
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create The Screen  (width(x),height(y))
screen = pygame.display.set_mode((800, 600))

# Background
backgroundImg = pygame.image.load('background.png')

# background music


mixer.music.load('background.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)


# Player
playerImg = pygame.image.load('player.png')

# Giving the starting coordinates
playerX = 370
playerY = 480
PlayerX_Change = 0

# Enemy
# To Create multiple enemies we are using list

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6


for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))

 # To give random coordinates
    enemyX .append(random.randint(64, 736))
    enemyY .append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(20)


# Bullet
bulletImg = pygame.image.load('bullet.png')

# To give  coordinates
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10

# ready- can't see bullet
#fire- bullet is moving
bullet_state = "ready"
# Function for player and we use blit method to draw
# blit((image,x-cordinate,y-cordinate))


# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10
score_value = 0

# Game Over Text


over_font = pygame.font.Font('freesansbold.ttf', 64)




def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((bulletX-enemyX)**2 + (bulletY-enemyY)**2)
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200,250))


# Game Loop
# To make the screen appear for longer time I created infinite loop
'''Now we are using for loop that is 
checking close key is pressed or not'''
running = True
while running:

    # fill(Red,Blue,Gree)-RGB to set color of screen
    screen.fill((0, 0, 0))

    # background image

    screen.blit(backgroundImg, (0, 0))

    # if running becomes false then it quits games as when it is true while is infinite loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            # print("A KeyStroke is pressed")
            if event.key == pygame.K_LEFT:
                # print("Left Key Pressed")
                PlayerX_Change = -5
            if event.key == pygame.K_RIGHT:
                # print("Right Key Pressed")
                PlayerX_Change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # For the soung of bullet
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

    # This is for event type where we remove hand from the key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("Keystroke has been released")
                PlayerX_Change = 0

    playerX += PlayerX_Change


# To stop the player to go out of the game window
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


# To stop the enemey to move out from the game widnow
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        enemy(enemyX[i], enemyY[i], i)

# Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:

            # for explosion sound
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 10  

            enemyX[i] = random.randint(64, 736)
            enemyY[i] = random.randint(50, 150)


# Bullet movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    show_score(textX, textY)
    

    '''we are putting coordinates in player function so that 
    we can change position of player image'''
    player(playerX, playerY)

    # to update game window
    pygame.display.update()
