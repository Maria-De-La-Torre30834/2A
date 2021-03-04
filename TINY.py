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
GREEN_BLUE = (20, 219, 163)

#------------------------------------------------------------------------------------------------------------------

#DRAW TEXT FUNTION
font_name = pygame.font.match_font ('Times New Roman')
def draw_text (surf, text, size, x, y):
        font = pygame.font.Font (font_name, size)
        text_surface = font.render (text, True, BLACK)
        text_rect = text_surface.get_rect ()
        text_rect.midtop = (x, y)
        surf.blit (text_surface, text_rect)
        
#SHOW START SCREEN FUNCTION
def show_start_screen():
        screen.fill (PASTEL_YELLOW)
        draw_text (screen, "TINY", 64, WIDTH / 2, HEIGHT / 4)
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

#SHOW GAME OVER SCREEN
def show_gameover_screen():
        screen.fill (GREEN_BLUE)
        draw_text (screen, "GAME OVER", 64, WIDTH / 2, HEIGHT / 4)
        draw_text (screen, "Press R to return to game or Q to quit.", 22, WIDTH / 2, HEIGHT / 2)
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

#--------------------------------------------------------------------------------------------------

#PLAYER CLASS

#PLAYER HEALTH
class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.healthbars = [
            pygame.image.load(os.path.join(img_folder, "Heart_0.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Heart_1.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Heart_2.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Heart_3.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Heart_4.png")).convert()
            ]
        self.healthbar_count = 0

        self.image = self.healthbars[self.healthbar_count]
        self.image = pygame.transform.scale(self.image, (100, 50))
        self.image.set_colorkey(PASTEL_BLUE)

        #ESTABLISH RECT, STARTING POINT
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    def getHealth(self):
        return self.healthbar_count
    
    #PASS IN +1 OR -1 TO INCREMENT / DECREMENT HEALTH BAR
    def setHealth(self, health):
        if health == 1: #INCREASE HEALTH, UNLESS self.healthbar_count is at 0
            self.healthbar_count -= 1
            if self.healthbar_count < 0:
                self.healthbar_count = 0
        elif health == -1: #DECREASE HEALTH, UNLESS self.healthbar_count is at 5
            self.healthbar_count += 1
            if self.healthbar_count > 5:
                self.healthbar_count = 5

        
    def update(self):
        self.image = self.healthbars[self.healthbar_count]
        self.image = pygame.transform.scale(self.image, (90, 50))
        self.image.set_colorkey(BLACK)

#PLAYER
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load(os.path.join(img_folder, "Maka.png")).convert()
        self.image = pygame.transform.scale(player_img, (50, 60))
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
        if keystate [pygame.K_s]:
            self.shoot()

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

        #HITS LADYBUG
        hits = pygame.sprite.spritecollide (self, ladybugs, False)
        if hits:
                if self.rect.top > hits[0].rect.top: #jumping from underneath
                        self.pos.y = hits[0].rect.bottom + 25 + 1
                        self.vel.y = 0
                else:
                        self.pos.y = hits[0].rect.top + 1 #jumping from above
                        self.vel.y = 0

        #SET THE NEW PLAYER POSITION BASED ON ABOVE
        self.rect.midbottom = self.pos
            
    def shoot(self):
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                magic = Magic(self.rect.centerx, self.rect.top)
                all_sprites.add(magic)
                magics.add(magic)
               #shoot_sound.play()

#----------------------------------------------------------------------------------------------------------------

#MAGIC CLASS
class Magic(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.magic = [
                                    pygame.image.load(os.path.join(img_folder, "Magic_0.png")).convert(),
                                    pygame.image.load(os.path.join(img_folder, "Magic_1.png")).convert(),
                                    pygame.image.load(os.path.join(img_folder, "Magic_2.png")).convert(),
                                    pygame.image.load(os.path.join(img_folder, "Magic_3.png")).convert(),
                                    pygame.image.load(os.path.join(img_folder, "Magic_4.png")).convert(),
                                    pygame.image.load(os.path.join(img_folder, "Magic_5.png")).convert()
                                    ]

                self.magic_count = 0
                
                self.image = self.magic[self.magic_count]
                self.image = pygame.transform.scale(self.image, (100, 15))
                self.image.set_colorkey(BLACK)

                self.rect = self.image.get_rect()
                self.rect.centerx = x
                self.rect.centery = y
                self.speedx = 10
        
        def update(self):
                self.rect.x += self.speedx

                #TRANSITION BTW MAGIC PNGS
                self.image = self.magic[self.magic_count]
                self.image = pygame.transform.scale(self.image, (50, 10))
                self.image.set_colorkey(BLACK)

                self.magic_count += 1
                if self.magic_count > 5:
                        self.magic_count = 0

                #DELETE MAGIC ONCE OFF SCREEN
                if self.rect.left > WIDTH:
                        self.kill()

#-----------------------------------------------------------------------------------------------------------------

#SPIDER CLASS
class Spider(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.spiders = [
                                        pygame.image.load(os.path.join(img_folder, "Spider_0.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Spider_1.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Spider_2.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Spider_3.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Spider_4.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Spider_5.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Spider_6.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Spider_7.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Spider_8.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Spider_9.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Spider_10.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Spider_11.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Spider_12.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Spider_13.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Spider_14.png")).convert()
                                    ]
                
                self.spider_count = 0
                
                self.image = self.spiders[self.spider_count]
                self.image = pygame.transform.scale(self.image, (150, 150))
                self.image.set_colorkey(BLACK)

                self.rect = self.image.get_rect()
                self.rect.centerx = WIDTH
                self.rect.centery = HEIGHT-400
                self.speedx = 10
        
        def update(self):


                #TRANSITION BTW SPIDER PNGS
                self.image = self.spiders[self.spider_count]
                self.image = pygame.transform.scale(self.image, (130, 130))
                self.image.set_colorkey(BLACK)

                self.spider_count += 1
                if self.spider_count > 14:
                        self.spider_count = 0
                        
               #self.rect.right=0
                self.rect.bottom=GROUND
                self.rect.x -=3
                if self.rect.right<0:
                        self.rect.left=WIDTH

#SPIDER HEALTHBAR
class SpiderHealthBar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.healthbars = [
            pygame.image.load(os.path.join(img_folder, "Skull_0.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Skull_1.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Skull_2.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Skull_3.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Skull_4.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "Skull_5.png")).convert()
            ]
        self.healthbar_count = 0

        self.image = self.healthbars[self.healthbar_count]
        self.image = pygame.transform.scale(self.image, (90, 50))
        self.image.set_colorkey(PASTEL_BLUE)

        #ESTABLISH RECT, STARTING POINT
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH-105
        self.rect.y = 10

    def getHealth(self):
        return self.healthbar_count
    
    #PASS IN +1 OR -1 TO INCREMENT / DECREMENT HEALTH BAR
    def setHealth(self, health):
        if health == 1: #INCREASE HEALTH, UNLESS self.healthbar_count is at 0
            self.healthbar_count -= 1
            if self.healthbar_count < 0:
                self.healthbar_count = 0
        elif health == -1: #DECREASE HEALTH, UNLESS self.healthbar_count is at 5
            self.healthbar_count += 1
            if self.healthbar_count > 5:
                self.healthbar_count = 5
                
    def update(self):
        self.image = self.healthbars[self.healthbar_count]
        self.image = pygame.transform.scale(self.image, (100, 50))
        self.image.set_colorkey(BLACK)

#------------------------------------------------------------------------------------------------------------------------------------------

#LADYBUG CLASS
class Ladybug(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.ladybugs = [
                                        pygame.image.load(os.path.join(img_folder, "Ladybug_0.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Ladybug_1.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Ladybug_2.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Ladybug_3.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Ladybug_4.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Ladybug_5.png")).convert(),
                                        pygame.image.load(os.path.join(img_folder, "Ladybug_6.png")).convert()
                                    ]
                
                self.ladybug_count = 0
                
                self.image = self.ladybugs[self.ladybug_count]
                self.image = pygame.transform.scale(self.image, (80, 60))
                self.image.set_colorkey(BLACK)

                self.rect = self.image.get_rect()
                self.rect.centerx = WIDTH
                self.rect.centery = HEIGHT-220
                self.speedx = 10
        
        def update(self):


                #TRANSITION BTW LADYBUG PNGS
                self.image = self.ladybugs[self.ladybug_count]
                self.image = pygame.transform.scale(self.image, (100, 80))
                self.image.set_colorkey(BLACK)

                self.ladybug_count += 1
                if self.ladybug_count > 6:
                        self.ladybug_count = 0
                        
                self.rect.x += -5
                if self.rect.right < 0:
                 self.rect.left = WIDTH

#-------------------------------------------------------------------------------------------------------------

#INITS
pygame.init()
pygame.mixer.init()

#LOAD SOUNDS
pygame.mixer.music.load (os.path.join (snd_folder, "SongTryOut1.mp3"))
pygame.mixer.music.set_volume (0.4)

#INITIALIZE VARIABLES
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TINY")

clock = pygame.time.Clock()
pygame.mixer.music.play(loops = -1) #continuous looping

#SPRITE GROUPS
all_sprites = pygame.sprite.Group()
magics = pygame.sprite.Group()
player = Player()
all_sprites.add(player)


ladybugs = pygame.sprite.Group()
ladybug = Ladybug ()
all_sprites.add (ladybug)
ladybugs.add (ladybug)

healthbar = HealthBar()
all_sprites.add(healthbar)
spider=Spider()
all_sprites.add(spider)
spiderhealthbar=SpiderHealthBar()
all_sprites.add(spiderhealthbar)

#GAME LOOP:
#   Process Events
#   Update
#   Draw
start = True
end = False
running = True
while running:

    #SHOW START SCREEN ONCE
    if start:
            show_start_screen()
            start = False

    if end:
            show_gameover_screen()
            end = False
            
    clock.tick(FPS)

    #PROCESS EVENTS
    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
                print("keyup!")
                if event.key == [pygame.K_q]:
                        print("x pressed")
                        show_gameover_screen()
                        end = True

    #UPDATE
    all_sprites.update()

    #DRAW
    screen.fill(PASTEL_BLUE)
    all_sprites.draw(screen)

    #FLIP AFTER DRAWING
    pygame.display.flip()

pygame.quit()
