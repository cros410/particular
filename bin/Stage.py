import sys
import pygame as pg
from Component import Component
from config import *
from db.database import Database
from Sprites import *


class MenuStage():

    def __init__(self, game, win):
        self.database = Database()
        self.game = game
        self.win = win
        self.arrayComponente = []
        self.play = Component(win, pg.image.load("../assets/menu/btn_play.png"),
                              pg.image.load("../assets/menu/btn_alt_play.png"), 414, 360, 1)
        self.options = Component(win, pg.image.load("../assets/menu/btn_options.png"),
                                 pg.image.load("../assets/menu/btn_alt_options.png"), 414, 440, 1)
        self.exit = Component(win, pg.image.load("../assets/menu/btn_exit.png"),
                              pg.image.load("../assets/menu/btn_alt_exit.png"), 414, 520, 1)
        self.__loadComponents(win)

    def draw(self):
        for component in self.arrayComponente:
            component.draw()
            component.hover()

    def events(self):
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.exit.inside(mouse[0], mouse[1]):
                    pg.quit()
                    sys.exit()
                if self.options.inside(mouse[0], mouse[1]):
                    self.game.click_sound()
                    self.goOptions()
                if self.play.inside(mouse[0], mouse[1]):
                    self.game.click_sound()
                    self.goNivelOne()

    def update(self):
        pass

    def goOptions(self):
        self.game.changeState(OptionStage(self.game, self.win))

    def goMenu(self):
        pass

    def goNivelOne(self):
        self.game.changeState(NivelOne(self.game, self.win))

    def __loadComponents(self, win):
        self.arrayComponente.append(
            Component(win, pg.image.load("../assets/menu/bg.jpg"), None, 0, 0, 0))
        self.arrayComponente.append(Component(win, pg.image.load(
            "../assets/menu/logo.png"), None, 240, 40, 0))
        self.arrayComponente.append(self.play)
        self.arrayComponente.append(self.options)
        self.arrayComponente.append(self.exit)


class OptionStage():

    def __init__(self, game, win):
        self.database = Database()
        self.game = game
        self.win = win
        self.arrayComponente = []
        self.arraySuit = []
        self.arrayDifficulty = []
        self.suit_a = Component(win, pg.image.load("../assets/options/suit_a.png"),
                                pg.image.load("../assets/options/suit_a_press.png"), 320, 122, 1)
        self.suit_b = Component(win, pg.image.load("../assets/options/suit_b.png"),
                                pg.image.load("../assets/options/suit_b_press.png"), 440, 122, 1)
        self.suit_c = Component(win, pg.image.load("../assets/options/suit_c.png"),
                                pg.image.load("../assets/options/suit_c_press.png"), 560, 122, 1)
        self.difficulty_1 = Component(win, pg.image.load("../assets/options/level_1.png"),
                                      pg.image.load("../assets/options/level_1_press.png"), 320, 321, 1)
        self.difficulty_2 = Component(win, pg.image.load("../assets/options/level_2.png"),
                                      pg.image.load("../assets/options/level_2_press.png"), 440, 321, 1)
        self.difficulty_3 = Component(win, pg.image.load("../assets/options/level_3.png"),
                                      pg.image.load("../assets/options/level_3_press.png"), 560, 321, 1)
        self.music = Component(win, pg.image.load("../assets/options/music_on.png"),
                               pg.image.load("../assets/options/music_off.png"), 380, 522, 1)
        self.sound = Component(win, pg.image.load("../assets/options/sound_on.png"),
                               pg.image.load("../assets/options/sound_off.png"), 500, 522, 1)
        self.back = Component(win, pg.image.load(
            "../assets/options/back.png"), None, 20, 20, 0)

        self.creditos = Component(win, pg.image.load(
            "../assets/options/creditos.png"), None, 860, 540, 0)

        self.__loadComponents(win)
        self.__init_componets()

    def draw(self):
        for component in self.arrayComponente:
            component.draw()
            component.hover()

    def events(self):
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.back.inside(mouse[0], mouse[1]):
                    self.game.click_sound()
                    self.goMenu()
                if self.sound.inside(mouse[0], mouse[1]):
                    self.game.click_sound()
                    self.game.sound = 1 - self.game.sound
                    self.database.update("sound", self.game.sound)
                    self.sound.active(1-self.game.sound)
                if self.music.inside(mouse[0], mouse[1]):
                    self.game.click_sound()
                    self.game.music = 1 - self.game.music
                    self.database.update("music", self.game.music)
                    self.music.active(1-self.game.music)
                    if self.game.music == 1:
                        pg.mixer.music.play()
                    else:
                        pg.mixer.music.pause()
                if self.creditos.inside(mouse[0], mouse[1]):
                    self.game.click_sound()
                    self.goCreditos()
                for suit in self.arraySuit:
                    if suit.inside(mouse[0], mouse[1]):
                        self.game.click_sound()
                        self.__active_group(self.arraySuit, suit, "suit")
                for difficulty in self.arrayDifficulty:
                    if difficulty.inside(mouse[0], mouse[1]):
                        self.game.click_sound()
                        self.__active_group(
                            self.arrayDifficulty, difficulty, "difficulty")

    def update(self):
        pass

    def goOptions(self):
        pass

    def goMenu(self):
        self.game.changeState(MenuStage(self.game, self.win))

    def goCreditos(self):
        self.game.changeState(CreditsStage(self.game, self.win))

    def __loadComponents(self, win):
        self.arrayComponente.append(
            Component(win, pg.image.load("../assets/options/bg.jpg"), None, 0, 0, 0))
        self.arrayComponente.append(Component(win, pg.image.load(
            "../assets/options/select_suit.png"), None, 258, 33, 0))
        self.arraySuit.append(self.suit_a)
        self.arraySuit.append(self.suit_b)
        self.arraySuit.append(self.suit_c)
        self.arrayComponente = self.arrayComponente + self.arraySuit
        self.arrayComponente.append(Component(win, pg.image.load(
            "../assets/options/select_level.png"), None, 257, 233, 0))
        self.arrayDifficulty.append(self.difficulty_1)
        self.arrayDifficulty.append(self.difficulty_2)
        self.arrayDifficulty.append(self.difficulty_3)
        self.arrayComponente = self.arrayComponente + self.arrayDifficulty
        self.arrayComponente.append(Component(win, pg.image.load(
            "../assets/options/select_sound.png"), None, 345, 434, 0))
        self.arrayComponente.append(self.music)
        self.arrayComponente.append(self.sound)

        self.arrayComponente.append(self.back)
        self.arrayComponente.append(self.creditos)

    def __init_componets(self):
        self.arraySuit[self.game.suit-1].active(True)
        self.arrayDifficulty[self.game.difficulty-1].active(True)
        self.sound.active(1-self.game.sound)
        self.music.active(1-self.game.music)

    def __active_group(self, group, element, property):
        element.active(True)
        index = group.index(element)
        setattr(self.game, property, index + 1)
        self.database.update(property, index+1)
        for component in group:
            if group.index(component) != index:
                component.active(False)


class CreditsStage():
    def __init__(self, game, win):
        self.game = game
        self.win = win
        self.arrayComponente = []
        self.back = Component(win, pg.image.load(
            "../assets/options/back.png"), None, 20, 20, 0)
        self.__loadComponents()

    def draw(self):
        for component in self.arrayComponente:
            component.draw()
            component.hover()

    def events(self):
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.back.inside(mouse[0], mouse[1]):
                    self.game.click_sound()
                    self.goOptions()

    def update(self):
        pass

    def goOptions(self):
        self.game.changeState(OptionStage(self.game, self.win))

    def goMenu(self):
        pass

    def __loadComponents(self):
        self.arrayComponente.append(
            Component(self.win, pg.image.load("../assets/options/bg.jpg"), None, 0, 0, 0))
        self.arrayComponente.append(Component(self.win, pg.image.load(
            "../assets/credits/creditos.png"), None, 258, 40, 0))
        self.arrayComponente.append(Component(self.win, pg.image.load(
            "../assets/credits/jason_foto.png"), None, 146, 145, 0))
        self.arrayComponente.append(Component(self.win, pg.image.load(
            "../assets/credits/jason.png"), None, 108, 253, 0))
        self.arrayComponente.append(Component(self.win, pg.image.load(
            "../assets/credits/claudia_foto.png"), None, 146, 442, 0))
        self.arrayComponente.append(Component(self.win, pg.image.load(
            "../assets/credits/claudia.png"), None, 108, 550, 0))
        self.arrayComponente.append(Component(self.win, pg.image.load(
            "../assets/credits/carlos_foto.png"), None, 430, 294, 0))
        self.arrayComponente.append(Component(self.win, pg.image.load(
            "../assets/credits/carlos.png"), None, 392, 401, 0))
        self.arrayComponente.append(Component(self.win, pg.image.load(
            "../assets/credits/cristina_foto.png"), None, 714, 145, 0))
        self.arrayComponente.append(Component(self.win, pg.image.load(
            "../assets/credits/cristina.png"), None, 676, 253, 0))
        self.arrayComponente.append(Component(self.win, pg.image.load(
            "../assets/credits/casanova_foto.png"), None, 714, 442, 0))
        self.arrayComponente.append(Component(self.win, pg.image.load(
            "../assets/credits/casanova.png"), None, 676, 550, 0))
        self.arrayComponente.append(self.back)


class NivelOne():
    def __init__(self, game, win):
        self.game = game
        self.win = win
        self.arrayComponente = []
        self.bg = Component(win, pg.image.load(
            "../assets/f.jpg"), None, 0, 0, 0)
        self.win.blit(self.bg.currentImage, (0, 0))
        self.bgWidth, self.bgHeight = self.bg.currentImage.get_rect().size
        self.stageWidth = self.bgWidth * 2
        self.startScrollingPosX = HW
        self.stagePosX = 0

        # CONJUNTO DE IMAGENES
        self.players = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        #ADD PLAYER
        self.player = Player(self)
        self.players.add(self.player)
        #ADD PLATFORMS
        base = Platform(0, FLOOR , WIDTH, HEIGHT - FLOOR)
        p2 = Platform(100 , FLOOR - 100 , 100 , 20)
        self.platforms.add(base)
        self.platforms.add(p2)
        
        

    def draw(self):
        self.players.draw(self.win)
        self.platforms.draw(self.win)

    def events(self):
        #mouse = pg.mouse.get_pos()
        move = 0
        k = pg.key.get_pressed()
        if k[pg.K_RIGHT]:
            move  = 1
        elif k[pg.K_LEFT]:
           move = -1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if  event.key == pg.K_SPACE:
                    self.player.jump()
        self.player.move(move)
         

    def update(self):
        #CHECK IF PLAYER HIT A PLATFOR 
        if  self.player.vel.y > 0:
            
            hits = pg.sprite.spritecollide(self.player , self.platforms , False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0

    
