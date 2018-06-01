import pygame as pg
from config import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0)
        k = pg.key.get_pressed()
        if k[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        elif k[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        #RESTRINGIR EL MOVIMIENTO DE JUGADOR 
        #SI PASA EL INICIO O FIN DEL STAGE

        self.acc += self.vel * PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
