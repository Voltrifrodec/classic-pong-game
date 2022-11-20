""" Knižnica pygamezero """
import pygame
import random
import time

from PIL import Image

from mapa import suradnice


""" ROZVRH """
""" 

Smer:
	(ako jednotková kružnica)
	vpravo: 0	vľavo: 2
	hore: 1		dole: 3

Na obrazovke:
	1. Mapa
	2. Objekty
	3. Entity
	4. Skóre

Entity:
	Príšera: (3)
		!pri vytvorení sa pridá do listu entity
		pozícia:int
			x, y
		smer:Smer
		farba:tuple
			R, G, B
	Pac-Man:
		!pri vytvorení sa pridá do listu entity
		pozícia:int
			x, y
		posledná pozícia (kvôli prekreslovaniu)
			x[-1], y[-1]
		smer:Smer
		skóre:int
			ak je pac-man na pozícii s XP => skóre+1
		kolízia:metóda
			ak je pac-man na pozícii ako príšera => GameOver
			ak je pac-man a príšera smerujú oproti sebe a blížia sa => GameOver
			ak ide pac-man naraziť do steny, nepokračuj ďalej
Objekty:
	Stena:
		!pri vytvorení sa pridá do listu objekty
		pozícia:dictionary
			x, y => true/false
	Bod:
		pozícia:dictionary
			x, y => true/false
		typ:Bod
			veľký -> 1.5 rýchlosť
			malý -> 1.0 rýchlosť

Mapa:
	Objekty:
		Steny:Stena
		Body: malé, veľké
		Entity:
			Pac-Man
			Príšera

"""




""" Triedy """
""" Základy """
# Smer
class Smer:
	def __init__(self, smer:int=0) -> None:
		self.smer = self.nahodny()
	def nahodny(self):
		self.smer = random.getrandbits(2)
	def getsmer(self):
		return self.smer

""" Entity """
# Pac-Man
class PacMan:
	""" pozícia:int
			x, y
		posledná pozícia (kvôli prekreslovaniu)
			x[-1], y[-1]
		-smer:Smer
		-skóre:int
			ak je pac-man na pozícii s XP => skóre+1
		rýchlosť: int
			1 - bežná
			1.5 - supercharge
		supercharge:bool
			ak pacman zje veľký bod, dostane supercharge, 1.5 rýchlosť..
			..pacman bude meniť farby
		kolízia:metóda
			ak je pac-man na pozícii ako príšera => GameOver
			ak je pac-man a príšera smerujú oproti sebe a blížia sa => GameOver
			ak ide pac-man naraziť do steny, nepokračuj ďalej """
	def __init__(self, x:int, y:int, obr:str, smer:int=0):
		self.x = x	# Pozícia x
		self.y = y	# Pozícia y
		self.poz = (x, y)	# Pozícia v tuple
		self.lastPoz = self.poz # Posledná pozícia
		self.obr = obr # Obrázok entity
		#TODO: Spraviť triedu smer a metódu náhodný
		self.smer = Smer().nahodny()
		self.skore = 0
	
	# TODO: Dorobiť funkciu na kolíziu
	def kolizia(self):
		pass
	def pridajSkore(self):
		self.skore += 1
	
# Príšery
class Prisery():
	def __init__(self, pocet:int=3) -> None:
		self.pocet = pocet
		pass
	def update(self):
		pass

""" Objekty """
# Bod
class Bod:
	def __init__(self, x, y) -> None:
		self.x = x
		self.y = y
		pass
# Stena
class Wall:
	def __init__(self, x, y, obr) -> None:
		self.x = x
		self.y = y
		self.obr = obr
		pass

# Mapa -> je objekt, ktorý drží obrázok mapy, vytvorený zo súradníc a podobrázkov
class Mapa:
	def __init__(self, size:tuple, suradnice:tuple) -> None:
		self.suradnice = suradnice
		self.size = size
		self.hraciaPlocha = self.draw()
	
	def draw(self) -> pygame.Surface:
		obrazok = Image.new('RGB', self.size)
		for i, riadok in enumerate(self.suradnice):
			for j, prvok in enumerate(riadok):
				nazov = ''
				if prvok is 0: nazov = 'wall-cross'
				if prvok is 1: nazov = 'xp1'
				if prvok is 2: nazov = 'xp2'
				if prvok is 8: nazov = 'none'
				if prvok is 9: nazov = f'prisera{random.randrange(1,3)}'
				if nazov == '': continue
				temp = Image.open(f'images/{nazov}.png')
				x = j * temp.width
				y = i * temp.height
				obrazok.paste(temp, box=(x, y))
				# self.hraciaPlocha.append((obrazok, x, y))
				# self.hraciaPlocha.append(Wall(x, y))
		return pygame.image.frombuffer(obrazok.tobytes(), obrazok.size, 'RGB')


# Loop:
def main():
	""" Konštanty """
	# šírka, výška okna
	WIDTH, HEIGHT = 800, 600
	# tuple šírky a výšky okna
	SIZE = WIDTH, HEIGHT
	# Farby
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)

	""" Inicializácia """
	# Inicializácia
	pygame.init()
	# Logo okna
	logo = pygame.image.load('images/pacman_logo.png')
	# Názov, titulok okna
	caption = 'Pac-Man @AdamValašťan, JakubKubaliak'
	# Nastavenie loga okna
	pygame.display.set_icon(logo)
	# Nastavenie názvu okna
	pygame.display.set_caption(caption)
	# Obrazovka s ktorou budeme pracovať, veľkosť musí byť tuple
	screen = pygame.display.set_mode(SIZE)

	# Obrázok Pac-mana
	pacman = pygame.image.load('images/pacman.png')
	hrac = PacMan(32, 32, 'images/pacman.png')
	# Zobrazenie Pac-Mana v double-bufferi, na pozícii (x,y) <- n-tica
	screen.blit(pacman, (0,0))

	# Mapa
	mapa = Mapa(SIZE, suradnice)

	# pygame.display.flip()
	pygame.display.update()
	
	# Premenná na manažovanie event loopu
	running = True

	x = 32

	# Main loop
	#TODO: Rozhýbať pacmana
	while running:
		x += pacman.get_width()
		x %= 600
		screen.fill(BLACK)
		screen.blit(mapa.hraciaPlocha, (0, 0))
		screen.blit(pacman, (x, 32))

		if hrac.kolizia()
			
		# event handling, gets all event from the event queue
		for event in pygame.event.get():
			# only do something if the event is of type QUIT
			if event.type == pygame.QUIT:
				# change the value to False, to exit the main loop
				running = False
		
		# pygame.display.flip()
		pygame.display.update()
		time.sleep(0.5)


if __name__ == '__main__':
	main()