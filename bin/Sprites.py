import pygame as pg
from config import *
vec = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename)

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width, height))
        return image

class Player(pg.sprite.Sprite):

    def __init__(self, stage):
        pg.sprite.Sprite.__init__(self)
        self.stage = stage
        # self.image.fill(self.__getSuit())
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (25, 300)
        self.pos = vec(48.5, 300) #POSITION IN ALL STAGE 
        self.pos_screen = vec(25, 300) #POSITION IN SCREEN
        self.vel = vec(0, 0)
        self.a = self.__getAcceleration()
        self.acc = vec(0, 0)
        self.des = 0

    def load_images(self):
        self.standing_frames = [self.stage.spritesheet.get_image(20, 10, 48 , 56),self.stage.spritesheet.get_image(117, 10, 48 , 56),
                                self.stage.spritesheet.get_image(214, 10, 48 , 56),self.stage.spritesheet.get_image(311, 10, 48 , 56),
                                self.stage.spritesheet.get_image(408, 10, 48 , 56),self.stage.spritesheet.get_image(505, 10, 48 , 56)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        
        self.walk_frames_r = [self.stage.spritesheet.get_image(20, 81, 48 , 56),self.stage.spritesheet.get_image(117, 81, 48 , 56),
                                self.stage.spritesheet.get_image(214, 81, 48 , 56),self.stage.spritesheet.get_image(311, 81, 48 , 56),
                                self.stage.spritesheet.get_image(408, 81, 48 , 56),self.stage.spritesheet.get_image(505, 81, 48 , 56)]
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
        
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame,True, False))
        for frame in self.walk_frames_l:
            frame.set_colorkey(BLACK)
        
        self.jump_frames_r = [self.stage.spritesheet.get_image(214, 152, 48 , 56),self.stage.spritesheet.get_image(311, 152, 48 , 56),
                                self.stage.spritesheet.get_image(408, 152, 48 , 56)]
        for frame in self.jump_frames_r:
            frame.set_colorkey(BLACK)

        self.jump_frames_l = []
        for frame in self.jump_frames_r:
            self.jump_frames_l.append(pg.transform.flip(frame,True, False))
        for frame in self.jump_frames_l:
            frame.set_colorkey(BLACK)

    def move(self, side):
        self.animate(side)
        #DEF GRAVITY
        self.acc = vec(0,PLAYER_GRAV)
        #DEF ACELE
        self.acc.x = self.a * side
        #DEF FRICC
        self.acc.x += self.vel.x * PLAYER_FRIC
        # ECU OF MOVE
        self.vel += self.acc
        m = self.pos.x
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        self.des = round(self.pos.x - m,0)
        
        WHP = self.image.get_width() / 2
        # NO OUT OF STAGE
        if self.pos.x >= self.stage.stageWidth - WHP:
            self.pos.x = self.stage.stageWidth - WHP
            self.stage.loseState = True
            self.stage.game.lose_sound()
        if self.pos.x <= WHP:
            self.pos.x = WHP
        # IN THE MIDDLE OF THE SCREEM
        # CALCULATE HOW MUCH MOVE THE SCREEN
        if self.pos.x < self.stage.startScrollingPosX:
            self.pos_screen.x = self.pos.x
        elif self.pos.x > self.stage.stageWidth - self.stage.startScrollingPosX:
            self.pos_screen.x = self.pos.x - self.stage.stageWidth + WIDTH
        else:
            self.pos_screen.x = self.stage.startScrollingPosX
            self.stage.stagePosX += -self.vel.x
            
        
        self.rect.center = (self.pos_screen.x, self.pos.y-WHP)

    def animate(self,side):
        now = pg.time.get_ticks()
        if side != 0:
            self.walking = True
        else:
            self.walking = False

        #show walk animation
        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                bottom = self.rect.bottom
                if self.vel.x  > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        #show jump animtion
        if self.jumping:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames_r)
                bottom = self.rect.bottom
                if self.vel.x  < 0:
                    self.image = self.jump_frames_l[self.current_frame]
                else:
                    self.image = self.jump_frames_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        #show stopped animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self,self.stage.platforms, False)
        hits_floor = pg.sprite.spritecollide(self,self.stage.bases, False)
        self.rect.x -= 1
        if hits or hits_floor:
            self.vel.y = -10      

    def __getSuit(self):
        switcher = {
            1 : GREEN,
            2 : BLUE,
            3 : ORANGE
        }
        return switcher.get(self.stage.game.suit)

    def __getAcceleration(self):
        switcher = {
            1 : PLAYER_ACC_1,
            2 : PLAYER_ACC_2,
            3 : PLAYER_ACC_3
        }
        return switcher.get(self.stage.game.difficulty)


class Platform(pg.sprite.Sprite):

    def __init__(self, x, y, w, h, type):
        pg.sprite.Sprite.__init__(self)
        if type == "":
            self.image = pg.Surface((w, h))
            self.image.fill(PURPLE)
        else:
            self.image = pg.image.load("../assets/one/platform{}.png".format(type))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self , dis):
        self.rect.x -= dis

class Life(pg.sprite.Sprite):

    def __init__(self , x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("../assets/one/life.png")
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def update(self , dis):
        self.rect.x -= dis

class Tumi(pg.sprite.Sprite):

    def __init__(self , x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("../assets/one/tumi.png")
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def update(self , dis):
        self.rect.x -= dis

class Food(pg.sprite.Sprite):

    def __init__(self , x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("../assets/one/food.png")
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def update(self , dis):
        self.rect.x -= dis
    
