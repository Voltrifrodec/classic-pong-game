"""
Pygame - Pong Game
- použité zdroje:
    1.) Clear Code - Learning Pygame by making Pong [https://www.youtube.com/watch?v=Qf3-aDXG8q4]
    2.) Clear Code - Learning Pygame by making Pong Part 2: Adding the score and a countdown timer [https://www.youtube.com/watch?v=E4Ih9mpn5tk]

"""


# TODO: Pridať opisné komentáre pre jednotlivé riadky kódu / funkcie
# TODO: Prepísať opisné komentáre do dokumentu (.docx) ako "dokumentáciu"
# TODO: Pridať počítanie skóre (jednoduché počítanie x:y, highscore)
# TODO: Pridať pozastavenie hry skrz stlačenie klávesy (napr. "P", alebo po stlačení medzerníka)
# TODO: Pridať zrýchlenie loptičky napr. ako ball_speed * (score * 0.1), prípadne nejakú) (lenže kde?)
# TODO: Pridať možnosť hrať proti počítaču alebo s niekým iným (dva tlačidla na spodku / vrchu obrazovky)
import pygame
import sys
import random as rand


# Inicializacia
pygame.init()
clock = pygame.time.Clock()
fps = 120


# Funkcie
# TODO: Prerobiť na triedy
def ball_anim():
    # Základné pohyby
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    # Ak sa dotýka spodnej / vrchnej hranice hracieho okna
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1 # invert

    # Ak sa dotýka ľavej / pravej hranice hracieho okna
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        restart_ball()

    # Ak lopta narazí na jeden z nárazníkov
    if ball.colliderect(bumper1) or ball.colliderect(bumper2):
        ball_speed_x *= -1

def restart_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    ball_speed_x *= rand.choice((-1,1)) 
    ball_speed_y *= rand.choice((-1,1)) 

def player_anim():
    # Zakladne nastavenie pohybu
    bumper1.y += bumper1_speed
    # Ošetrenie ak nárazník narazí na hornú / spodnú hranicu hracieho okna
    if bumper1.top <= 0:
        bumper1.top = 0
    if bumper1.bottom >= SCREEN_HEIGHT:
        bumper1.bottom = SCREEN_HEIGHT


def opponent_anim():
    if bumper2.top < ball.y:
        bumper2.top += bumper2_speed
    if bumper2.bottom > ball.y:
        bumper2.bottom -= bumper2_speed
    if bumper2.top <= 0:  # Oprava aby hrac nemohol vybehnut z hracieho okna
        bumper2.top = 0
    if bumper2.bottom >= SCREEN_HEIGHT:
        bumper2.bottom = SCREEN_HEIGHT





# Nastavenia okna
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 #? V podstate redundant, no musím všade meniť na tuple
SCREEN_RES = (800, 600)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Nastavenie herných objektov
# TODO: Možnosť si pridať textúru na jednotlivé objekty
# TODO: Pretvoriť jednotlivé objekty do tried (obzvlášť nárazníky)
# Nastavenie lopty
ball_size = 20
ball = pygame.Rect(SCREEN_WIDTH / 2 - int(ball_size / 2), SCREEN_HEIGHT / 2 - int(ball_size / 2), ball_size, ball_size)
# Nastavenie hráča
bumper_size = (20, 160)
bumper1 = pygame.Rect(SCREEN_WIDTH - (int(bumper_size[0]/  2) + bumper_size[0]), SCREEN_HEIGHT / 2 - (int(bumper_size[1] / 2)),*bumper_size)
# Nastavenie oponenta ("AI" alebo iný hráč)
bumper2 = pygame.Rect(int(bumper_size[0] / 2), SCREEN_HEIGHT / 2 - int(bumper_size[1] / 2),*bumper_size)


# Nastavenie vlastností herného okna
background_color = (0, 0, 0)
separator = (screen, (200, 200, 200), (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT)) # deliaca čiara (anti alias line??)


# Nastavenie "fyziky" pre hru
DEFAULT_SPEED = 5
ball_speed_x = (DEFAULT_SPEED * rand.choice((-1,1)))
ball_speed_y = (DEFAULT_SPEED * rand.choice((-1,1)))
bumper1_speed = 0
bumper2_speed = DEFAULT_SPEED       # TODO: Ak sa jedná o hráča, tak nastaviť na 0



# Hlavný cyklus hry
Running = True      #? 'Running' je asi redundant, viacej ako estetická vložka
while Running:      #? 'Running' je asi redundant, viacej ako estetická vložka
    # Nastavenie akcií pre dané udalostí
    for e in pygame.event.get():
        # Zatvorenie okna
        if e.type == pygame.QUIT:
            Running = False #? Redundant?
            pygame.quit()
            sys.exit()
        # Pohyb hráča
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_DOWN:
                bumper1_speed += 7
            if e.key == pygame.K_UP:
                bumper1_speed -= 7
        # Naopak pri uvolneni klavesy
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_DOWN:
                bumper1_speed -= 7
            if e.key == pygame.K_UP:
                bumper1_speed += 7
        
    
    # Vykreslenie objektov
    screen.fill(background_color)
    pygame.draw.ellipse(screen,(255,0,0),ball)
    pygame.draw.rect(screen,(255,255,255),bumper1)
    pygame.draw.rect(screen,(255,255,255),bumper2)
    pygame.draw.aaline(*separator)
    
    
    # Animácie jednotlivých objektov
    ball_anim()
    player_anim()
    opponent_anim()
    
    
    # Aktualizácia okna
    pygame.display.flip()
    clock.tick(fps)
