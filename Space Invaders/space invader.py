import pygame
import random
import math
from pygame import mixer

# Reduce latency of audio
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

# Initialize the pygame
pygame.init()

# colour
black = (0,0,0)
white = (255,255,255)

# Background
background = pygame.image.load("background.jpeg")

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# create screen
window_width = 1024
window_height = 720
gameDisplay  = pygame.display.set_mode((window_width,window_height))

# Player
player_img = pygame.image.load("space-invaders.png")
player_x = 490
player_y = 640
player_x_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 6
for i in range(number_of_enemies):
    if i%2 == 0 :
        enemy_img.append(pygame.image.load("enemy_1.png"))
    elif i%3 == 0 :
        enemy_img.append(pygame.image.load("enemy_2.png"))
    else :
        enemy_img.append(pygame.image.load("enemy_3.png"))
    enemy_x.append(random.randint(0,960)) 
    enemy_y.append(random.randint(0,150)) 
    enemy_x_change.append(3)
    enemy_y_change.append(40)

# Bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 640
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('America.ttf',32)
text_x = 5
text_y = 5

# Game over text
game_over_text = pygame.font.Font("America.ttf",64)

def game_over():
    game_over_txt = game_over_text.render("GAME OVER",True,white)
    gameDisplay.blit(game_over_txt,(400,350))

def show_Score(x,y):
    score = font.render("Score : " + str(score_value),True,white)
    gameDisplay.blit(score,(x,y))

def player(x,y):
    gameDisplay.blit(player_img,(x,y)) 

def enemy(x,y,i):
    gameDisplay.blit(enemy_img[i],(x,y)) 

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    gameDisplay.blit(bullet_img,(x + 16 ,y + 10)) # x + 16 so that bullet gets fired from centre of the spaceship and y + 10 so that bullet gets fired from above spaceship 

def isCollision(enemy_x,enemy_y,bullet_x,bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x,2) + math.pow(bullet_y - enemy_y,2))
    if distance < 27:
        return True
    else :
        return False



# game loop
running = True
while running:
    gameDisplay.fill(black)
    gameDisplay.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -7
            if event.key == pygame.K_RIGHT:
                player_x_change = 7
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    mixer.Sound('laser.wav').play()
                    bullet_x = player_x
                    fire_bullet(bullet_x,bullet_y)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
                
    player_x += player_x_change

    # checking boundaries for spaceship so that it doesn't go out of the screen
    if player_x <= 0 :
        player_x = 0
    
    if player_x >= 960 :
        player_x = 960
    
    player(player_x,player_y)

    # Enemy movement 
    for i in range(number_of_enemies):  
        
        # Game Over
        if enemy_y[i] > 550:
            for j in range(number_of_enemies):
                enemy_y[j] = 10000
            game_over()
            break 

        if enemy_x[i] <= 0 :
            enemy_x_change[i] = 3
            enemy_y[i] += enemy_y_change[i]
        
        if enemy_x[i] >= 960 :
            enemy_x_change[i] = -3
            enemy_y[i] += enemy_y_change[i]
        
        enemy_x[i] += enemy_x_change[i]
        
        # Collision
        collision = isCollision(enemy_x[i],enemy_y[i],bullet_x,bullet_y)
        if collision :
            mixer.Sound('explosion.wav').play()
            bullet_state = "ready"
            bullet_y = 640
            if i == 3:
                score_value += 2
            else:
                score_value += 1

            enemy_x[i] = random.randint(0,960)
            enemy_y[i] = random.randint(0,150)
        
        enemy(enemy_x[i],enemy_y[i],i)

    # Bullet movement
    if bullet_y <= 0:
        bullet_state = "ready"
        bullet_y = 640
        
    if bullet_state is "fire":
        fire_bullet(bullet_x,bullet_y)
        bullet_y -= bullet_y_change

    show_Score(text_x,text_y)
    
    pygame.display.update()
