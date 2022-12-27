import pygame
import sys
import random as rnd


#? Inicializacia
pygame.init()
clock = pygame.time.Clock()
fps = 120
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_font = pygame.font.Font('fonts/VCR_OSD_MONO_1.001.ttf', 32)
DEFAULT_BUMPER_SPEED = 7

#? Trieda pre objekt hraca (narazniky)
class BumperObject():
    # Inicializacia / Nastavenie parametrov
    def __init__(self, size_x: int, size_y: int, pos_x, pos_y, color: tuple):
        self.w = size_x
        self.h = size_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.bumper = pygame.Rect(self.pos_x, self.pos_y, self.w, self.h)
        self.score = 0
        self.bumper_speed = 0
        self.default_ai_speed = 7

    # Vykreslenie
    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.bumper)

    # Animacia naraznika (ako sa ma spravat, co sa ma vykonat ked nastane to a to...)
    # Zvlast pre hraca, zvlast pre pocitac
    def player_animation(self):
        self.bumper.y += self.bumper_speed
        if self.bumper.top <= 0:
            self.bumper.top = 0
        if self.bumper.bottom >= SCREEN_HEIGHT:
            self.bumper.bottom = SCREEN_HEIGHT
    def autonomous_animation(self, ball):
        if self.bumper.top < ball.y:
            self.bumper.top += self.default_ai_speed
        if self.bumper.bottom > ball.y:
            self.bumper.bottom -= self.default_ai_speed
        if self.bumper.top <= 0:
            self.bumper.top = 0
        if self.bumper.bottom >= SCREEN_HEIGHT:
            self.bumper.bottom = SCREEN_HEIGHT

    # Vrati aktualne skore hraca
    def getScore(self):
        return self.score
    
    # Restartovanie naraznikov na zakladnu poziciu
    def restart(self, pos_x, pos_y):
        self.bumper.x = pos_x
        self.bumper.y = pos_y
        self.score = 0
        

        


#? Trieda pre objekt lopty
class BallObject():
    # Inicializacia / Nastavenie parametrov
    def __init__(self, size: int, default_speed: int, color: tuple, score_time):
        self.size = size
        self.default_speed = default_speed
        self.color = color
        self.score_time = score_time
        self.speed_x = (self.default_speed * rnd.choice((-1, 1)))
        self.speed_y = (self.default_speed * rnd.choice((-1, 1)))
        self.ball = pygame.Rect(SCREEN_WIDTH / 2  - int(self.size / 2),
                                SCREEN_HEIGHT / 2 - int(self.size / 2),
                                self.size, self.size)
    
    # Vykreslenie
    def render(self, screen):
        pygame.draw.ellipse(screen, self.color, self.ball)

    # Animacia lopty (ako sa ma spravat, co sa ma vykonat ked nastane to a to...)
    def animate(self, bumper1: BumperObject, bumper2: BumperObject):
        self.ball.x += self.speed_x
        self.ball.y += self.speed_y
        
        # Ak sa dotyka spodnej / vrchnej hranici okna -> odraz
        if self.ball.top <= 0 or self.ball.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1
        
        # Ak sa dotyka lavej / pravej hranice hracieho okna -> priratanie skore
        if self.ball.left <= 0:
            bumper1.score += 1
            self.score_time = pygame.time.get_ticks()
        if self.ball.right >= SCREEN_WIDTH:
            bumper2.score += 1
            self.score_time = pygame.time.get_ticks()
        
        # Ak loptu odrazi jeden z hracov -> odraz
        if self.ball.colliderect(bumper1.bumper) or self.ball.colliderect(bumper2.bumper):
            self.speed_x *= -1

    
    # Restartovanie lopty (ak jeden z hracov zaboduje)
    def restart(self):
        self.ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        # Zistujem kolko casu ubehlo current_time, podla toho vypisem cifru
        current_time = pygame.time.get_ticks()
        if current_time - self.score_time < 700: # 0.7s
            text = game_font.render("3", False, (0, 200, 200))
            screen.blit(text, (SCREEN_WIDTH / 2 - 10, SCREEN_HEIGHT / 2 + 20))
        if 700 < current_time - self.score_time < 1400: #1.4s
            text = game_font.render("2", False, (0, 150, 150))
            screen.blit(text, (SCREEN_WIDTH / 2 - 10, SCREEN_HEIGHT / 2 + 20))
        if 1400 < current_time - self.score_time < 2100: #2.1s
            text = game_font.render("1", False, (0, 100, 100))
            screen.blit(text, (SCREEN_WIDTH / 2 - 10, SCREEN_HEIGHT / 2 + 20))
        if current_time - self.score_time < 2100:
            self.speed_x = self.speed_y = 0
        
        # Ak nic, tak pokracuj bez zmeny
        else:
            self.speed_x = self.default_speed * rnd.choice((-1, 1))
            self.speed_y = self.default_speed * rnd.choice((-1, 1))
            self.score_time = None # Reset

            


#? Vytvorenie objektov hry, nastavenie ostatnych vlastnosti
background_color = (0, 0, 0)
# Deliaca ciara
separator = (screen, (200, 200, 200), (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))
score_time = True
ball = BallObject(20, 5, (255, 0 ,0), score_time)
bumper_player = BumperObject(20, 160, SCREEN_WIDTH - (int(20 /  2) + 20), SCREEN_HEIGHT / 2 - (int(160 / 2)), (255, 255, 255))
bumper_opponent = BumperObject(20, 160, int(20 / 2), SCREEN_HEIGHT / 2 - int(160 / 2), (255, 255, 255))

#? Event Loop
Running = True
Started = False
Paused = False
while Running:
    # Event Listeners
    for e in pygame.event.get():
        # Zatvorenie okna
        if e.type == pygame.QUIT:
            Running = False
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:            
            # Pozastavenie hry
            if e.key == pygame.K_p and Paused is False:
                print('Game paused -> True')
                pause_text = game_font.render("Pozastavené", False, (255, 0, 0))
                screen.blit(pause_text, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 60))
                Paused = True
                break
            if e.key == pygame.K_p and Paused is True:
                print('Game paused -> False')
                Paused = False
                break
            # Restartovanie hry (reset skore a lopty)
            if e.key == pygame.K_r:
                ball.score_time = pygame.time.get_ticks()
                bumper_player.restart(SCREEN_WIDTH - (int(20 / 2) + 20), SCREEN_HEIGHT / 2 - (int(160 / 2)))
                bumper_opponent.restart(int(20 / 2), SCREEN_HEIGHT / 2 - int(160 / 2))
                break
            
                
        # Pohyb hraca 1 (napravo)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_DOWN:
                bumper_player.bumper_speed += DEFAULT_BUMPER_SPEED
            if e.key == pygame.K_UP:
                bumper_player.bumper_speed -= DEFAULT_BUMPER_SPEED
        # Naopak pri uvolneni klavesy
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_DOWN:
                bumper_player.bumper_speed -= DEFAULT_BUMPER_SPEED
            if e.key == pygame.K_UP:
                bumper_player.bumper_speed += DEFAULT_BUMPER_SPEED
        
    if Paused is False:
        # Vykreslenie objektov
        screen.fill(background_color)
        pygame.draw.aaline(*separator)
        ball.render(screen)
        bumper_player.render(screen)
        bumper_opponent.render(screen)
        
        # Vykreslenie textu (skore)
        player_score = game_font.render(f"{bumper_player.getScore()}", False, (200, 200, 0))   # Vykreslenie skore hraca 1
        opponent_score = game_font.render(f"{bumper_opponent.getScore()}", False, (200, 200, 0)) # Vykreslenie skore hraca 1
        screen.blit(player_score, (600, 470))
        screen.blit(opponent_score, (200, 470))
    
        # Animacia jednotlivych objektov
        ball.animate(bumper_player, bumper_opponent)
        bumper_player.player_animation()
        bumper_opponent.autonomous_animation(ball.ball)

        # Restarttovanie lopty
        if ball.score_time:
            ball.restart()
    else:
        pass
    
    
    # Aktualizacia okna
    pygame.display.flip()
    clock.tick(fps)
