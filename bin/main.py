import pygame as pg
import sys
from random import randint
from db.database import Database
from Stage import MenuStage
from config import *

class Game():

    def __init__(self):
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(TITLE)
        self.win = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        params = self.__load()
        self.difficulty = params[2]
        self.suit = params[1]
        self.sound = params[3]
        self.music = params[4]
        self.stage = MenuStage(self, self.win)
        self.sound_click = pg.mixer.Sound("../assets/sound/click.wav")
        self.sound_coin = pg.mixer.Sound("../assets/sound/coin.wav")
        self.sound_life = pg.mixer.Sound("../assets/sound/life.wav")
        self.sound_food = pg.mixer.Sound("../assets/sound/food.wav")
        self.sound_lose = pg.mixer.Sound("../assets/sound/lose.wav")
        pg.mixer.music.load("../assets/sound/game.wav")
        if self.music == 1:
            pg.mixer.music.play()
    
    def new(self):
        self.run()
    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        self.stage.update()
    
    def events(self):
        self.stage.events()
    
    def draw(self):
        self.stage.draw()
        pg.display.flip()
    
    def changeState(self, state):
        self.stage = state
    
    def click_sound(self):
        if self.sound == 1 :
            pg.mixer.Sound.play(self.sound_click)
    
    def coin_sound(self):
        if self.sound == 1 :
            pg.mixer.Sound.play(self.sound_coin)
    
    def life_sound(self):
        if self.sound == 1 :
            pg.mixer.Sound.play(self.sound_life)
    
    def food_sound(self):
        if self.sound == 1 :
            pg.mixer.Sound.play(self.sound_food)
    
    def lose_sound(self):
        if self.sound == 1 :
            pg.mixer.Sound.play(self.sound_lose)

    def __load(self):
        database = Database()
        res = database.get_all()
        return res
    
    
g = Game()
while g.running:
    g.new()

pg.quit()