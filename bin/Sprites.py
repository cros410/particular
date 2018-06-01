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
        self.rect.x = 0
        self.rect.bottom = FLOOR - 300
        self.pos = vec(self.rect.x, self.rect.y)
        self.pos_stage = vec(self.rect.x, self.rect.y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0.5)
        k = pg.key.get_pressed()
        if k[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        elif k[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        # FRICTION
        self.acc.x += self.vel.x * PLAYER_FRIC
        # ECU OF MOVE
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        WP = self.image.get_width()
        WHP = self.image.get_width() / 2
        # NO OUT OF STAGE
        if self.pos.x >= self.stage.stageWidth - WP:
            self.pos.x = self.stage.stageWidth - WP
        if self.pos.x <= 0:
            self.pos.x = 0
        # IN THE MIDDLE OF THE SCREEM
        if self.pos.x < (self.stage.startScrollingPosX - WHP):
            self.pos_stage.x = self.pos.x
        elif self.pos.x > self.stage.stageWidth - (self.stage.startScrollingPosX + WHP):
            self.pos_stage.x = self.pos.x - self.stage.stageWidth + WIDTH
        else:
            self.pos_stage.x = (self.stage.startScrollingPosX - WHP)
            self.stage.stagePosX += -self.vel.x

        rel_x = self.stage.stagePosX % self.stage.bgWidth
        self.stage.win.blit(self.stage.bg.currentImage,
                            (rel_x - self.stage.bgWidth, 0))
        if rel_x < WIDTH:
            self.stage.win.blit(self.stage.bg.currentImage, (rel_x, 0))
        
        self.rect.bottomleft = (self.pos_stage.x , self.pos.y)


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y