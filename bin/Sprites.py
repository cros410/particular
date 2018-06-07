import pygame as pg
from config import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, stage):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(YELLOW)
        self.stage = stage
        self.rect = self.image.get_rect()
        self.rect.center = (25, 300)
        self.pos = vec(25, 300) #POSITION IN ALL STAGE 
        self.pos_screen = vec(25, 300) #POSITION IN SCREEN
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def move(self, side):
        #DEF GRAVITY
        self.acc = vec(0,PLAYER_GRAV)
        #DEF ACELE
        self.acc.x = PLAYER_ACC * side
        #DEF FRICC
        self.acc.x += self.vel.x * PLAYER_FRIC
        # ECU OF MOVE
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        WP = self.image.get_width()
        WHP = self.image.get_width() / 2
        # NO OUT OF STAGE
        if self.pos.x >= self.stage.stageWidth - WHP:
            self.pos.x = self.stage.stageWidth - WHP
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
        # MOVE THE SCREEN
        rel_x = self.stage.stagePosX % self.stage.bgWidth
        self.stage.win.blit(self.stage.bg.currentImage,
                            (rel_x - self.stage.bgWidth, 0))
        if rel_x < WIDTH:
            self.stage.win.blit(self.stage.bg.currentImage, (rel_x, 0))

        self.rect.center = (self.pos_screen.x, self.pos.y-WHP)

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self,self.stage.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -10

class Platform(pg.sprite.Sprite):

    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
