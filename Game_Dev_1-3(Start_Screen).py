import pygame
import random
import os

#CONSTANTS - GAME
WIDTH = 1400
HEIGHT = 700
FPS = 30
GROUND = HEIGHT - 30
SLOW = 3
FAST = 8

#CONSTANTS - PHYSICS
PLAYER_ACC  =  0.9
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.9
vec = pygame.math.Vector2

#DEFINE COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PASTEL_BLUE = (212, 255, 252)
PASTEL_YELLOW = (255, 204, 107)

#DRAW TEXT FUNTION
font_name = pygame.font.match_font ('arial')
def draw_text (surf, text, size, x, y):
        font = pygame.font.Font (font_name, size)
        text_surface = font.render (text, True, BLACK)
        text_rect = text_surface.get_rect ()
        text_rect.midtop = (x, y)
        surf.blit (text_surface, text_rect)
        
#SHOW START SCREEN FUNCTION
def show_start_screen():
        screen.fill (PASTEL_YELLOW)
        draw_text (screen, "SHOOTER", 64, WIDTH / 2, HEIGHT / 4)
        draw_text (screen, "Arrow keys to move, Space to jump, 'S' to fire", 22, WIDTH / 2, HEIGHT / 2)
        draw_text (screen, "Press a key to begin. . .", 18, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick (FPS)
            for event in pygame.event.get ():
                    if event.type == pygame.QUIT:
                        pygame.quit ()
                    if event.type == pygame.KEYUP:
                        print ("Key pressed to start game!")
                        waiting = False
                        
#ASSET FOLDERS
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "Sprite")
snd_folder = os.path.join (game_folder, "Noise")

#PLAYER CLASS
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load(os.path.join(img_folder, "Mica.png")).convert()
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0  #user-built  speed  var
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

        self.pos = vec(0, GROUND - 60)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        #self.speedx = 0  #always stationary unless

        '''
        keystate = pygame.key.get_pressed() 

        if keystate [pygame.K_LEFT]:
             self.speedx = -5
        if keystate [pygame.K_RIGHT]:
            self.speedx = 5
        if keystate [pygame.K_SPACE]:
            self.shoot()
        '''
        #self.rect.x += self.speedx
                
         #CHECKS TO SEE WHICH KEYES WERE IN THE LIST (A.K.A PRESSED)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.acc.x += PLAYER_ACC
        if keystate[pygame.K_LEFT]:
            self.acc.x += -PLAYER_ACC
        if self.vel.y == 0 and keystate[pygame.K_SPACE]:
            self.vel.y = -20

        #APPLY FRICTION IN THE X DIRECTION
        self.acc.x += self.vel.x * PLAYER_FRICTION

        #EQUATIONS OF MOTION
        self.vel += self.acc                                         #v = v0 + at
        self.pos += self.vel + 0.5 * self.acc              #s = s + v0t + 1/2at

        #WRAP AROUND THE SIDES OF THE SCREEN
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        #SIMULATE THE GROUND
        if self.pos.y > GROUND:
            self.pos.y = GROUND + 1
            self.vel.y = 0

        #SET THE NEW PLAYER POSITION BASED ON ABOVE
        self.rect.midbottom = self.pos
            
    def shoot(self):
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
               #shoot_sound.play()
                
#PLATFORM CLASS
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((200, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 4, HEIGHT - 200)

    def update(self):
        self.rect.x += -5
        if self.rect.right < 0:
            self.rect.left = WIDTH
            
#BULLET CLASS
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        bullet_img = pygame.image.load(os.path.join(img_folder, "Lazer_0.png")).convert()
        self.image = bullet_img
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += se;f.speedy
        if self.rect.bottom < 0:
            self.kill()

#INITS
pygame.init()
pygame.mixer.init()

#LOAD SOUNDS
pygame.mixer.music.load (os.path.join (snd_folder, "SongTryOut1.mp3"))
pygame.mixer.music.set_volume (0.4)

#INITIALIZE VARIABLES
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot")

clock = pygame.time.Clock()
pygame.mixer.music.play(loops = -1) #continuous looping

#SPRITE GROUPS
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
platform = Platform()
all_sprites.add(player)
all_sprites.add(platform)

#GAME LOOP:
#   Process Events
#   Update
#   Draw
start = True
running = True
while running:

    #SHOW START SCREEN ONCE
    if start:
            show_start_screen()
            start = False
            
    clock.tick(FPS)

    #PROCESS EVENTS
    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            running = False

    #UPDATE
    all_sprites.update()

    #DRAW
    screen.fill(PASTEL_BLUE)
    all_sprites.draw(screen)

    #FLIP AFTER DRAWING
    pygame.display.flip()

pygame.quit()
