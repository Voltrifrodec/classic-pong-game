# Original code: https://www.youtube.com/watch?v=Qf3-aDXG8q4

import sys, pygame
import random

#* 0 - Inicializacia
pygame.init()
clock = pygame.time.Clock()

# Window settings
(scr_w,scr_h) = 800,600
screen = pygame.display.set_mode((scr_w,scr_h))
pygame.display.set_caption('Pong Game - v0.0.0a')
fps = 60


def ball_anim():
    global ball_speed_x,ball_speed_y # Oprava chyby s globálnými premennými
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.top <= 0 or ball.bottom >= scr_h:
        ball_speed_y *= -1  # obrati rychlost lopty
    if ball.left <= 0 or ball.right >= scr_w:
        # ball_speed_x *= -1
        ball_restart()

    # Ak narazí na bumper hráča / protivníka
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1
        
      
def player_anim():
    player.y += player_speed
    if player.top <= 0:  # Oprava aby hrac nemohol vybehnut z hracieho okna
        player.top = 0
    if player.bottom >= scr_h:
        player.bottom = scr_h
      

def opponent_anim():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:  # Oprava aby hrac nemohol vybehnut z hracieho okna
        opponent.top = 0
    if opponent.bottom >= scr_h:
        opponent.bottom = scr_h

def ball_restart():
    global ball_speed_x,ball_speed_y
    ball.center = (scr_w/2,scr_h/2)
    ball_speed_y *= random.choice((1,-1))
    ball_speed_x *= random.choice((1,-1))

# Ball
ball = pygame.Rect(scr_w/2 - 15, scr_h/2 - 15,30,30)
player = pygame.Rect(scr_w - 20, scr_h/2 - 70, 10,140)
opponent = pygame.Rect(10,scr_h/2 - 70, 10, 140)

bg_color = pygame.Color('grey12')
light_gray = pygame.Color(200,200,200)

ball_speed_x, ball_speed_y = 7 * random.choice((1, -1)), 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
                # Ak by som len pripočítaval k y += hodnotu, tak by som musel spamovať tú klávesu, inak 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        # Naopak pri uvolneni klavesy
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7
        
                
                
            
        # TODO: Prvý krok je mať to čo je vo funkcii tu, potom to nahradiť funkciou
    ball_anim()
    player_anim()
    opponent_anim()
    
    # Vykreslenie objektov
    # Moznosti pre farbu: tuple s (r,g,b) s hodnotami 0 .. 255 alebo Color Object (pygame.color('color_name'))
    screen.fill(bg_color) #prefarbenie starej obrazovky, aby nedoslo k prekryvaniu
    pygame.draw.rect(screen,light_gray,player)
    pygame.draw.rect(screen,light_gray,opponent)
    pygame.draw.ellipse(screen,light_gray,ball)
    pygame.draw.aaline(screen, light_gray, (scr_w/2, 0), (scr_w/2,scr_h)) # anti alias line
    
    # Window update
    pygame.display.flip() # Vytvorenie obrazku zo vsetkeho co sa da vykreslit z loop
    delta = clock.tick(fps) * 0.001
    clock.tick(180) # 60 times per second

# Na obrazovku mozeme pridavat objekty troma sposobmi na Display Surface: kreslenie cez pygame.draw, (regular) Surface a pridavanie objektov, rectangles
