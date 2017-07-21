#! /usr/bin/python

import pygame, sys, os, random
from pygame import *

WIN_WIDTH = 1020
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 120
MAX_LEVEL = 4

 
def main():
    global screen, player, total_level_height
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Use arrows to move!")
    timer = pygame.time.Clock()
               
    opening_screen(screen)
    
    cue_music()
   
    start_level = True

    myfont = pygame.font.SysFont("sans serif", 35)
    
    content = read_lvls_file('lvls.txt')
    
    lvlnum = 4
    
    while True:

        if start_level == True:

            bg = Surface((DEPTH, DEPTH))
            bg.convert()
            bg.fill(Color("#000000"))
   
            entities = pygame.sprite.Group()
            player = Player(DEPTH, DEPTH)
            movingPlatforms = []
            platforms = []
            enemies = []
            
            lvlnum += 1
            if lvlnum > MAX_LEVEL:
                lvlnum = 1
        
            level = get_level(content, str(lvlnum))
            build_level(level, platforms, movingPlatforms, enemies, entities)

            total_level_width  = len(level[0])*DEPTH
            total_level_height = len(level)*DEPTH
            
            camera = Camera(complex_camera, total_level_width, total_level_height)
            entities.add(player)
            time = 0
            
        for y in range(DEPTH):
            for x in range(DEPTH):
                screen.blit(bg, (x * DEPTH, y * DEPTH))
                
        start_level = player.lvlDone
        
        player.handle_event()
       
        camera.update(player)
        
        time += 1

        player.update(platforms, movingPlatforms, time)
         
        for e in enemies:
            e.update(platforms, movingPlatforms, player, time)

        for m in movingPlatforms:
            m.update(platforms, movingPlatforms)

        for e in entities:
            screen.blit(e.image, camera.apply(e))
        
 #       lvlstr = "Level:" + str(lvlnum)
#        label = myfont.render(lvlstr, 5, (255, 0, 0))
#        screen.blit(label, (15, 15))
        
        game_over()
            
        pygame.display.update()
        
        timer.tick(60)

        
def opening_screen(screen):
    start_game = False
    gradient = 'up'
    gval = 0
    image = pygame.image.load('3force.bmp')
    
    while start_game == False:
        
       
        if gval == 250:
            gradient = 'down'
        if gval == 0:
            gradient = 'up'

        if gradient == 'up':
            gval += 10
        if gradient == 'down':
            gval -= 10

        screen.fill(Color("#FFFFFF"))
        screen.blit(image, (HALF_WIDTH - 640/ 2, HALF_HEIGHT - 400/2, WIN_WIDTH, WIN_HEIGHT))
        #make fonts
        myfont0 = pygame.font.SysFont("sans serif", 60) 
        myfont = pygame.font.SysFont("monospace", 68)
        myfont2 = pygame.font.SysFont("monospace", 35)
        myfont3 = pygame.font.SysFont("monospace", 10)
        
        #render text
        label0 = myfont0.render("Press Any Key to Start", 5, (gval, gval, gval))
        label = myfont.render("ZELDA", 5, (0, 0, 0))
        label2 = myfont2.render("Legends Untold", 5, (0, 0, 0))
        label3 = myfont3.render("by Riley Bird", 5, (0, 0, 0))
        screen.blit(label0, (280, 50))
        screen.blit(label, (HALF_WIDTH - 100, HALF_HEIGHT + 200))
        screen.blit(label2, (HALF_WIDTH - 150, HALF_HEIGHT + 260))
        screen.blit(label3, (HALF_WIDTH - 40, HALF_HEIGHT + 300))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN:
                start_game = True
            
def reset():
        global bg, camera, time, player, lvlnum, enemies, platforms, movingPlatforms, entities, total_level_height
        bg = set_background()
        
        entities = pygame.sprite.Group()

        player = Player(DEPTH, DEPTH)
        movingPlatforms = []
        platforms = []
        enemies = []
        
        lvlnum += 1
        if lvlnum > MAX_LEVEL:
            lvlnum = 1
    
        content = read_lvls_file('lvls.txt')
        level = get_level(content, str(lvlnum))
        build_level(level, platforms, enemies, entities)

        total_level_width  = len(level[0])*DEPTH
        total_level_height = len(level)*DEPTH
        
        camera = Camera(complex_camera, total_level_width, total_level_height)
        entities.add(player)
        time = 0
        
    

def build_level(level, platforms, movingPlatforms, enemies, entities):
#    global player
    x = y = 0
    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "M":
                m = MovingPlatform(x, y)
                movingPlatforms.append(m)
                entities.add(m)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            if col == "G":
                g = Enemy(x, y)
                enemies.append(g)
                entities.add(g)
            if col == "S":
                s = Spikes(x, y)
                platforms.append(s)
                entities.add(s)
            if col == "K":
                k = Koopa(x, y)
                enemies.append(k)
                entities.add(k)
            if col == "@":
                player.rect.x = x
                player.rect.y = y
            x += DEPTH
        y += DEPTH
        x = 0

        
def read_lvls_file(filename):
    lvlsfile = open(filename, 'r')
    content = lvlsfile.readlines()
    lvlsfile.close()
    return content

def get_level(content, lvlnum):
    Level = []
    lineNum = 0
    for lineNum in range(len(content)):
        #process each line
        line = content[lineNum]

        #this is the level we want
        if lvlnum in line:
            lineNum += 1
            while ';' not in line: #; indicates the end of the level
                line = content[lineNum].strip('\n')
                Level.append(line)
                lineNum += 1
    return Level

#def draw_entites(entities, camera, screen):
#    for e in entities:
#        screen.blit(e.image, camera.apply(e))
    
def cue_music():
    pygame.mixer.init()
    pygame.mixer.music.load('243-stone-tower-temple.ogg')
    pygame.mixer.music.play(-1)

#def set_background():
#    bg = Surface((DEPTH, DEPTH))
#    bg.convert()
#    bg.fill(Color("#000000"))
#    return bg

#def draw_background(screen, bg):
#    for y in range(DEPTH):
#        for x in range(DEPTH):
#            screen.blit(bg, (x * DEPTH, y * DEPTH))
   
def game_over():
        #load gameover pic
        if player.alive == False:
            image = pygame.image.load('gameover.bmp')
            screen.blit(image, (190, 0))

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)
    
    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h
     #camera moves down
    if player.down == True:
        t -= HALF_HEIGHT
        
    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        #set up sprite animation
        self.sheet = pygame.image.load('_linkEdit.bmp')
        self.sheet.set_colorkey((0, 0, 0)) #make background transparent
        self.sheet.set_clip(pygame.Rect(5, 5, 107, 120))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.frame = 0
        
        self.right_states = { 0: (5, 917, 107, 120), 1: (132, 917, 107, 120), 2: (242, 917, 107, 120), 3: (364, 917, 107, 120), 4: (480, 917, 107, 120), 5: (604, 917, 107, 120), 6: (725, 917, 107, 120),
        7: (851, 917, 107, 120), 8: (970, 917, 107, 120), 9: (1077, 917, 107, 120)}

        self.left_states = { 0: (5, 658, 107, 120), 1: (132, 658, 107, 120), 2: (242, 658, 107, 120), 3: (364, 658, 107, 120), 4: (480, 658, 107, 120), 5: (604, 658, 107, 120), 6: (725, 658, 107, 120),
        7: (851, 658, 107, 120), 8: (970, 658, 107, 120), 9: (1077, 658, 107, 120)}

        self.standing_states = { 0: (12, 5, 107, 120), 1: (132, 5, 107, 120), 2:(252, 5, 107, 120)}

        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.alive = True
        self.lvlDone = False
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.running = False
        self.onMovingPlatform = False

    def handle_event(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if e.type == KEYDOWN:
                
                if e.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if e.key == K_UP:
                    self.up = True
                if e.key == K_DOWN:
                    self.down = True
                if e.key == K_LEFT:
                    self.left = True
                if e.key == K_RIGHT:
                    self.right = True
                if e.key == K_SPACE:
                    self.running = True

            
            if e.type == KEYUP:
                self.clip(self.standing_states[0])
                if e.key == K_UP:
                    self.up = False
                if e.key == K_DOWN:
                    self.down = False
                if e.key == K_RIGHT:
                    self.right = False
                if e.key == K_LEFT:
                    self.left = False
                if e.key == K_SPACE:
                    self.running = False 
          
                    
    def update(self, platforms, movingPlatforms, time):
        #only move if player is alive
        if self.alive == True:
            if self.up:
                # only jump if on the ground
                if self.onGround:
                    self.yvel -= 60
                    effect =  pygame.mixer.Sound('jump.ogg')
                    effect.play()
            if self.down:
                pass
            if self.left:
                self.xvel = -15
                self.clip(self.left_states)
                time = 0
            if self.right:
                self.xvel = 15
                self.clip(self.right_states)
                time = 0
            if self.running and self.right:
                self.xvel = 28
            if self.running and self.left:
                self.xvel -= 28
                
            self.blink(time)
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 5
            # max falling speed
            if self.yvel > 100: self.yvel = 100
            
        if not (self.left or self.right) and self.onMovingPlatform == False:
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        self.collide(self.xvel, 0, movingPlatforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False
        # do y-axis collisions if player is still alive (want to see him fall)
        if self.alive == True:
            self.collide(0, self.yvel, platforms)
            self.collide(0, self.yvel, movingPlatforms)
        #player falls to his death
        if self.rect.y > total_level_height:
            self.yvel = 0
            if self.alive == True:
                effect =  pygame.mixer.Sound('WW_Link_Die1.ogg')
                effect.play()
                self.alive = False

        self.image = self.sheet.subsurface(self.sheet.get_clip())
  
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    self.lvlDone = True    
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                    #follow moving platform
                    if isinstance(p, MovingPlatform):
                        self.xvel = p.xvel
                        self.onMovingPlatform = True
                    else:
                        self.onMovingPlatform = False
                    #dying from spikes
                    if isinstance(p, Spikes):
                        effect =  pygame.mixer.Sound('WW_Link_Die1.ogg')
                        effect.play()
                        self.alive = False
                        self.yvel = -20
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                

    def blink(self, time):
        if time%129 == 4:
            self.clip(self.standing_states[0])
        if time%129 == 5:
            self.clip(self.standing_states[1])
        if time%129 == 6:
            self.clip(self.standing_states[2])
        if time%129 == 7:
            self.clip(self.standing_states[1])
        if time%129 == 8:
            self.clip(self.standing_states[0])

class Enemy(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
  
        #displaying gumba image
        self.sheet = pygame.image.load('mariospritesheet.bmp')
        self.sheet.set_colorkey((0,0,0)) #make background transparent
        self.sheet.set_clip(pygame.Rect(515, 400, 120, 120))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.movements = { 0: (512, 400, 120, 120), 1: (671, 400, 120, 120) }
       
        self.frame = 0
        self.movement = 'left'
        self.xvel = 0
        self.yvel = 0
        self.onGround = False

    def update(self, platforms, movingPlatforms, player, time):

        #goomba image updates
        if time%20 == 0:
            self.clip(self.movements)                  
        if self.movement == 'left' and self.rect.x < player.rect.x + HALF_WIDTH:
            self.xvel = -4
        if self.movement == 'right':
            self.xvel = 4
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 2
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if self.movement == 'none':
            self.displaysmashedgumba()
        else:    
            # increment in x direction
            self.rect.left += self.xvel
            # do x-axis collisions
            self.collide(self.xvel, 0, platforms, player)
            self.collide(self.xvel, 0, movingPlatforms, player)
            # increment in y direction
            self.rect.top += self.yvel
            # assuming we're in the air
            self.onGround = False;
            # do y-axis collisions
            self.collide(0, self.yvel, platforms, player)
            self.collide(0, self.yvel, movingPlatforms, player)
            self.image = self.sheet.subsurface(self.sheet.get_clip())

    def displaysmashedgumba(self):
        self.sheet = pygame.image.load('smashedgumba.bmp')
        self.sheet.set_colorkey((0, 0, 0)) #make background transparent
        self.sheet.set_clip(pygame.Rect(0, 0, 120, 120))
        self.image = self.sheet.subsurface(self.sheet.get_clip())         
        self.clip((0,0,120, 120))
        

    def collide(self, xvel, yvel, platforms, player):
        
        self.killedByPlayer(player)

        self.playerKilled(player)
        
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.movement = 'left'
                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.movement = 'right'
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom

    def killedByPlayer(self, player):
         if pygame.sprite.collide_rect(self, player) and player.yvel > 0 and self.movement != 'None' and player.alive == True:
            effect =  pygame.mixer.Sound('BSZ_Kill.ogg')
            effect.play()
            player.yvel = -20
            self.xvel = 0
            self.yvel = 0
            self.movement = 'none'

    def playerKilled(self, player):
        if pygame.sprite.collide_rect(self, player) and self.xvel != 0 and player.rect.right - 40 > self.rect.left and player.alive == True:
            effect =  pygame.mixer.Sound('WW_Link_Die1.ogg')
            effect.play()
            player.alive = False
            player.yvel = -20


class Koopa(Enemy):
     def __init__(self, x, y):
        Enemy.__init__(self, x, y)
  
        #displaying gumba image
        self.sheet = pygame.image.load('enemy.bmp')
        self.sheet.set_colorkey((0,0,0)) #make background transparent
        self.sheet.set_clip(pygame.Rect(435, 200, 120, 120))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.movements = { 0: (435, 195, 120, 120), 1: (580, 195, 120, 120)  }
       
        self.frame = 0
        self.movement = 'left'
        self.xvel = 0
        self.yvel = 0
        self.onGround = False

     def update(self, platforms, movingPlatforms, player, time):
        ran = random.randint(0, 2)
        if self.movement != 'none':
            if ran == 1:
                self.movement = 'left'
            else:
                self.movement = 'right'
       #Koopa image updates
        if time%20 == 0:
            self.clip(self.movements)
        if self.movement == 'left' and self.rect.x < player.rect.x + HALF_WIDTH:
            if self.onGround:
                self.xvel = -4
                self.yvel -= 20
        elif self.movement == 'right':
            if self.onGround:
                self.xvel = 4
                self.yvel -= 20
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 2
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if self.movement == 'none':
            self.displaydeadkoopa()
        else:
            # increment in x direction
            self.rect.left += self.xvel
            # do x-axis collisions
            self.collide(self.xvel, 0, platforms, player)
            self.collide(self.xvel, 0, movingPlatforms, player)
            # increment in y direction
            self.rect.top += self.yvel
            # assuming we're in the air
            self.onGround = False;
            # do y-axis collisions
            self.collide(0, self.yvel, platforms, player)
            self.collide(0, self.yvel, movingPlatforms, player)
            self.image = self.sheet.subsurface(self.sheet.get_clip())

     def displaydeadkoopa(self):
        self.sheet = pygame.image.load('dk.bmp')
        self.sheet.set_colorkey((0, 0, 0)) #make background transparent
        self.sheet.set_clip(pygame.Rect(0, 0, 120, 120))
        self.image = self.sheet.subsurface(self.sheet.get_clip())         
        self.clip((0,0,120, 120))





    

class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.sheet = pygame.image.load('brick-2.bmp').convert()
        self.sheet.set_colorkey((0, 0, 0))#make background transparent
        self.sheet.set_clip(pygame.Rect(0, 0, 120, 120))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        pass

class MovingPlatform(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.xvel = 0
        self.direction = 'right'

    def update(self, platforms, movingPlatforms):
        if self.direction == 'left':
            self.xvel = 3
        if self.direction == 'right':
            self.xvel = -3
        self.rect.x += self.xvel
        self.collide(platforms)
        self.collide(movingPlatforms)

    def collide(self, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p) and p != self:
                if self.xvel > 0:
                    self.rect.right = p.rect.left
                    self.direction = 'right'
                    self.xvel = 0
                if self.xvel < 0:
                    self.rect.left = p.rect.right
                    self.direction = 'left'
                    self.xvel = 0

class Spikes(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.sheet = pygame.image.load('Spikes.bmp').convert()
        self.sheet.set_colorkey() #make background transparent
        self.sheet.set_clip(pygame.Rect(0, 0, 110, 120))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.sheet = pygame.image.load('Door2.bmp')
        self.sheet.set_colorkey((0,0,0)) #make background transparent
        self.sheet.set_clip(pygame.Rect(0, 0, 120, 120))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
       

if __name__ == "__main__":
    main()
