import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30

#DEFINE COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#INITIALIZE VARIABLES
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

clock = pygame.time.Clock()

#GAME LOOP:
#		Process Events
#		Update
#		Draw
running = True
while running:

		#PROCESS EVENTS
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		
		#UPDATE


		#DRAW
		screen.fill(BLACK)

		#FLIP AFTER DRAWING
		pygame.display.flip()

pygame.quit()
