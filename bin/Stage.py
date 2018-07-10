import sys
import pygame as pg
from Component import Component
from config import *
from db.database import Database
from Sprites import *
import requests as requests
import json


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
        self.ranking = Component(win, pg.image.load(
            "../assets/menu/ranking.png"), None, 860, 540, 0)

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
                    self.goSelect()
                if self.ranking.inside(mouse[0], mouse[1]):
                    self.goRanking()

    def update(self):
        pass

    def goOptions(self):
        self.game.changeState(OptionStage(self.game, self.win))

    def goMenu(self):
        pass

    def goSelect(self):
        self.game.changeState(SelectLevel(self.game, self.win))
    
    def goRanking(self):
        self.game.changeState(Ranking(self.game, self.win))

    def __loadComponents(self, win):
        self.arrayComponente.append(
            Component(win, pg.image.load("../assets/menu/bg.jpg"), None, 0, 0, 0))
        self.arrayComponente.append(Component(win, pg.image.load(
            "../assets/menu/logo.png"), None, 240, 40, 0))
        self.arrayComponente.append(self.play)
        self.arrayComponente.append(self.options)
        self.arrayComponente.append(self.exit)
        self.arrayComponente.append(self.ranking)

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
            "../assets/one/f.png"), None, 0, 0, 0)
        self.floor = Component(win, pg.image.load(
            "../assets/one/floor.png"), None, 0, FLOOR, 0)    
        self.win.blit(self.bg.currentImage, (0, 0))
        self.bgWidth, self.bgHeight = self.bg.currentImage.get_rect().size
        self.stageWidth = self.bgWidth * 4
        self.startScrollingPosX = HW
        self.stagePosX = 0
        self.pauseState = False
        self.loseState = False
        self.winState = False
        self.name = ""
        # CONJUNTO DE IMAGENES
        self.players = pg.sprite.Group()
        self.enemys = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.flags = pg.sprite.Group()
        self.bases = pg.sprite.Group()
        self.lifes = pg.sprite.Group()
        self.tumis = pg.sprite.Group()
        self.foods = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.spritesheet = Spritesheet("../assets/one/player{}.png".format(self.game.suit))
        self.spritesheet_enemy = Spritesheet("../assets/one/enemy.png")
        #ADD PLAYER
        self.player = Player(self)
        self.players.add(self.player)
        #ADD ENEMY
        self.enemy1 = Enemy(self, 600, FLOOR-65,1)
        self.enemy2 = Enemy(self, 1000, FLOOR-65,1)
        self.enemys.add(self.enemy1)
        self.enemys.add(self.enemy2)
        #ADD PLATFORMS
        base = Platform(0, FLOOR , 3*WIDTH, HEIGHT - FLOOR,"")
        base.image.set_alpha(0) 
        pt = Platform(200 , FLOOR - 25 , 100 , 20,"1")
        p1 = Platform(750 , FLOOR - 100 , 100 , 20,"1")
        p2 = Platform(1135.5 , FLOOR - 100 , 100 , 20,"1")
        p3 = Platform(1411 , FLOOR - 200 , 50 , 20,"2")
        p4 = Platform(1636.5 , FLOOR - 100 , 100 , 20,"1")
        p5 = Platform(2350 , FLOOR - 100 , 100 , 20,"1")
        p6 = Platform(3055.5 , FLOOR - 100 , 100 , 20,"1")
        p7 = Platform(3331 , FLOOR - 200 , 50 , 20,"2")
        p8 = Platform(3556.5 , FLOOR - 100 , 100 , 20,"1")
        self.bases.add(base)
        self.platforms.add(pt)
        self.platforms.add(p1)
        self.platforms.add(p2)
        self.platforms.add(p3)
        self.platforms.add(p4)
        self.platforms.add(p5)
        self.platforms.add(p6)
        self.platforms.add(p7)
        self.platforms.add(p8)
        #ADD LIFE
        l1 = Life(1423.5 , FLOOR - 225)
        l2 = Life(3343.5 , FLOOR - 225)
        self.lifes.add(l1)
        self.lifes.add(l2)
        #ADD TUMIS
        t1 = Tumi(1674 ,FLOOR - 150)
        t2 = Tumi(3093 ,FLOOR - 150)
        self.tumis.add(t1)
        self.tumis.add(t2)
        #ADD FOOD
        f1 = Food(1160 , FLOOR - 125)
        self.foods.add(f1)
        #ADD FLAG
        flag  = Flag(self.stageWidth-30,FLOOR-100)
        self.flags.add(flag)
        #LETRA
        self.myfont = pg.font.SysFont("monospace", 20, True)
        self.myfontNumber = pg.font.SysFont("monospace", 30, True)
        #PUNTAJE
        self.poits = 0
        #LIFES
        self.lifes_points = 1
        #FOOD
        self.nfoods = 0
        #LOAD IMAGES
        self.image_life = pg.image.load('../assets/one/life.png')
        #LOAD COMPONENTS
        self.arrayComponents = []
        self.arrayPause = []
        self.arrayLose = []
        self.arrayWin = []
        self.pause = Component(win , pg.image.load(
            "../assets/one/pause.png") , None , 905 , 5 , 0)
        #LOAD COMPONENTS PAUSE
        self.marco_pause = Component(win , pg.image.load(
            "../assets/pause/pause_marco.png") , None ,280 , 160 , 0)
        self.play = Component(win, pg.image.load("../assets/pause/btn_play.png"),
                              pg.image.load("../assets/pause/btn_alt_play.png"), 325.3, 250, 1)
        self.exit = Component(win, pg.image.load("../assets/pause/btn_exit.png"),
                              pg.image.load("../assets/pause/btn_alt_exit.png"), 502.6, 250, 1)
        
        #LOAD COMPONENTS LOSE / WIN
        self.marco = Component(win , pg.image.load(
            "../assets/lose/tabla.png") , None ,230 , 70 , 0)
        self.marco_win = Component(win , pg.image.load(
            "../assets/lose/tabla_win.png") , None ,230 , 70 , 0)
        self.game_over_title = Component(win , pg.image.load(
            "../assets/lose/game_over_title.png") , None ,262 , 127 , 0)
        self.win_title = Component(win , pg.image.load(
            "../assets/lose/win_title.png") , None ,262 , 127 , 0)
        self.save = Component(win, pg.image.load("../assets/lose/btn_guardar.png"),
                              pg.image.load("../assets/lose/btn_alt_guardar.png"), 325.3, 453, 1)
        self.exit_lose = Component(win, pg.image.load("../assets/lose/btn_exit.png"),
                              pg.image.load("../assets/lose/btn_alt_exit.png"), 502.6, 453, 1)
        self.continue_win = Component(win, pg.image.load("../assets/lose/btn_exit.png"),
                              pg.image.load("../assets/lose/btn_alt_exit.png"), 414, 368, 1)
        self.player_dead = Component(win, pg.image.load(
            "../assets/lose/player_{}_dead.png".format(self.game.suit)), None, 415, 250, 1)
        self.player_win = Component(win, pg.image.load(
            "../assets/lose/player_{}_win.png".format(self.game.suit)), None, 415, 250, 1)
        self.lose_tumi = Component(win, pg.image.load(
            "../assets/lose/tumi.png"), None, 310, 250, 1)
        self.lose_food = Component(win, pg.image.load(
            "../assets/lose/food.png"), None, 600, 270, 1)
        
        self.__loadComponents()
        
    def draw(self):
        self.bases.draw(self.win)
        self.players.draw(self.win)
        self.enemys.draw(self.win)
        self.platforms.draw(self.win)
        self.lifes.draw(self.win)
        self.tumis.draw(self.win)
        self.foods.draw(self.win)
        self.bullets.draw(self.win)
        self.flags.draw(self.win)
        #RENDER POINTS
        label = self.myfont.render("PUNTAJE : {}".format(self.poits), 1, BLACK)
        self.win.blit(label, (5, 0))
        #RENDER LIFE
        lifes = self.myfont.render("VIDAS : ", 1, BLACK)
        place  = HW +  100
        self.win.blit(lifes, (HW, 0))
        for l in range(self.lifes_points):
            self.win.blit(self.image_life , (place, 0))
            place += 30
        for component in self.arrayComponents:
            component.draw()
        if  self.pauseState:
            for component in self.arrayPause:
                component.draw()
                component.hover()
        if self.loseState:
            for component in self.arrayLose:
                component.draw()
                component.hover()
            #RENDER NAME
            pg.draw.rect(self.win,(255,255,255),(330,400,300,40))
            n = self.myfont.render(self.name, 1, BLACK)
            self.win.blit(n, (350,410))
            s_tumis = self.myfontNumber.render(str(self.poits), 1, BLACK)
            s_food = self.myfontNumber.render(str(self.nfoods), 1, BLACK)
            self.win.blit(s_tumis, (320, 355))
            self.win.blit(s_food, (620, 330))
        if self.winState:
            for component in self.arrayWin:
                component.draw()
                component.hover()
            s_tumis = self.myfontNumber.render(str(self.poits), 1, BLACK)
            s_food = self.myfontNumber.render(str(self.nfoods), 1, BLACK)
            self.win.blit(s_tumis, (320, 355))
            self.win.blit(s_food, (620, 330))

    def events(self):
        mouse = pg.mouse.get_pos()
        move = 0
        k = pg.key.get_pressed()
        if k[pg.K_RIGHT]:
            move  = 1
            self.player.side = 1
        elif k[pg.K_LEFT]:
            move = -1
            self.player.side = -1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if not self.pauseState and  not self.loseState and not self.winState:
                if event.type == pg.KEYDOWN:
                    if  event.key == pg.K_UP:
                        self.player.jump(1)
                    if event.key == pg.K_SPACE:
                        self.player.shoot()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.pause.inside(mouse[0], mouse[1]):
                        self.goPause(True)
            if self.pauseState:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.play.inside(mouse[0], mouse[1]):
                        self.goPause(False)
                    if self.exit.inside(mouse[0], mouse[1]):
                        self.goMenu()
            if self.loseState:
                if event.type == pg.KEYDOWN:
                    if event.unicode.isalpha():
                        self.name += event.unicode
                    elif event.key == pg.K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif event.key == pg.K_RETURN:
                        self.name = ""
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.save.inside(mouse[0], mouse[1]):
                        self.save_score()
                    if self.exit_lose.inside(mouse[0], mouse[1]):
                        self.goMenu()
            if self.winState:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.exit_lose.inside(mouse[0], mouse[1]):
                        self.goMenu()
                        

        if not self.pauseState and not self.loseState and not self.winState:
            self.player.move(move)
            self.move_screen(move)

    def update(self):
        self.bullets.update()
        for enemy in self.enemys:
            enemy.animate()
        self.player.jumping = True
        #CHECK IF PLAYER HIT THE FLOOR
        hit_floor = pg.sprite.spritecollide(self.player , self.bases , False)
        if hit_floor:
                self.player.jumping = False
                self.player.pos.y = hit_floor[0].rect.top - 2
                self.player.vel.y = 0

        #CHECK IF PLAYER HIT A PLATFOR
        if  self.player.vel.y > 0:
            hits_platfroms = pg.sprite.spritecollide(self.player , self.platforms , False)
            if hits_platfroms:
                self.player.jumping = False
                self.player.pos.y = hits_platfroms[0].rect.top - 2
                self.player.vel.y = 0

        #CHECK HIT A LIFE
        hits_lifes = pg.sprite.spritecollide(self.player, self.lifes , False)
        if hits_lifes:
            self.game.life_sound()
            self.lifes.remove(hits_lifes[0])
            self.lifes_points += 1
        #CHECK HIT A TUMI
        hits_tumis = pg.sprite.spritecollide(self.player, self.tumis , False)
        if hits_tumis:
            self.game.coin_sound()
            self.tumis.remove(hits_tumis[0])
            self.poits += 10
        #CHECK HIT A FOOD
        hits_food = pg.sprite.spritecollide(self.player, self.foods , False)
        if hits_food:
            self.game.food_sound()
            self.foods.remove(hits_food[0])
            self.nfoods += 5
        
        #CHECK HIT TO ENMY
        hits_enemy = pg.sprite.spritecollide(self.player, self.enemys , False)
        if hits_enemy:
            self.loseState = True
        
        #CHECK IF BULLET TO ENEMY
        for bullet in self.bullets:
            hits_bullet =  pg.sprite.spritecollide(bullet, self.enemys , True)
            if hits_bullet:
                self.poits += 20
                bullet.kill()
        #CHECK IF WIIN
        hits_flag = pg.sprite.spritecollide(self.player, self.flags , False)
        if hits_flag:
            self.winState = True

    def __loadComponents(self):
        self.arrayComponents.append(self.pause)
        self.arrayPause.append(self.marco_pause)
        self.arrayPause.append(self.play)
        self.arrayPause.append(self.exit)
        self.arrayLose.append(self.marco)
        self.arrayLose.append(self.exit_lose)
        self.arrayLose.append(self.save)
        self.arrayLose.append(self.game_over_title)
        self.arrayLose.append(self.player_dead)
        self.arrayLose.append(self.lose_tumi)
        self.arrayLose.append(self.lose_food)
        self.arrayWin.append(self.marco_win)
        self.arrayWin.append(self.continue_win)
        self.arrayWin.append(self.win_title)
        self.arrayWin.append(self.player_win)
        self.arrayWin.append(self.lose_tumi)
        self.arrayWin.append(self.lose_food)

    def goPause(self, state):
        self.pauseState = state

    def goMenu(self):
        self.game.changeState(MenuStage(self.game, self.win))

    def move_screen(self, dir):
        rel_x = round(self.stagePosX % self.bgWidth,0)
        self.win.blit(self.bg.currentImage,
                            (rel_x - self.bgWidth, 0))
        self.win.blit(self.floor.currentImage,
                            (rel_x - self.bgWidth, FLOOR))
        
        if rel_x < WIDTH:
            self.win.blit(self.bg.currentImage, (rel_x, 0))
            self.win.blit(self.floor.currentImage, (rel_x, FLOOR))
        if self.player.rect.center[0] == self.startScrollingPosX:
            self.platforms.update(self.player.des)
            self.lifes.update(self.player.des)
            self.tumis.update(self.player.des)
            self.foods.update(self.player.des)
            self.enemys.update(self.player.des)
            self.flags.update(self.player.des)
    
    def save_score(self):
        payload = {"nombre" : self.name , "puntaje" : self.poits}
        r = requests.post(URL_API + "/ranking", data=payload)
        print("Status : {}".format(r.status_code))
        self.goMenu()

class Ranking():

    def __init__(self, game, win):
        self.game = game
        self.win = win
        self.arrayComponente = []
        #LETRA
        self.myfont = pg.font.SysFont("monospace", 40, True)
        self.back = Component(win, pg.image.load(
            "../assets/ranking/back.png"), None, 20, 20, 0)
        self.rankings = self.getRanking()
        self.__loadComponents()
    
    def draw(self):
        for component in self.arrayComponente:
            component.draw()
            component.hover()
        #RENDER POINTS
        inicio =  130
        for ranking in self.rankings:
            label = self.myfont.render("{}:  {}".format(ranking.get("nombre").upper(),ranking.get("puntaje")), 1, BLACK)
            self.win.blit(label, (280, inicio))
            inicio += 80

    def update(self):
        pass

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

    def __loadComponents(self):
        self.arrayComponente.append(
            Component(self.win, pg.image.load("../assets/ranking/bg.jpg"), None, 0, 0, 0))
        self.arrayComponente.append(
            Component(self.win, pg.image.load("../assets/ranking/tabla.png"), None, 230, 70, 0))
        self.arrayComponente.append(self.back)
    
    def goMenu(self):
        self.game.changeState(MenuStage(self.game, self.win))

    def getRanking(self):
        r = requests.get(URL_API + "/ranking")
        return r.json()

class SelectLevel():

    def __init__(self, game, win):
        self.game = game
        self.win = win
        self.arrayComponente = []
        self.back = Component(win, pg.image.load(
            "../assets/select/back.png"), None, 20, 20, 0)
        self.One = Component(self.win, pg.image.load("../assets/select/one.png"), None, 99, 130, 0)
        self.Two = Component(self.win, pg.image.load("../assets/select/two.png"), None, 414, 130, 0)
        self.create = Component(self.win, pg.image.load("../assets/select/create.png"), None, 729, 130, 0)
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
                    self.goMenu()
                if self.One.inside(mouse[0], mouse[1]):
                    self.game.click_sound()
                    self.goNivelOne()
                if self.Two.inside(mouse[0], mouse[1]):
                    self.game.click_sound()
                    self.goNivelTwo()
                if self.create.inside(mouse[0], mouse[1]):
                    self.game.click_sound()
                    self.goNivelCreate()
                   

    def update(self):
        pass

    def goOptions(self):
        pass

    def goMenu(self):
        self.game.changeState(MenuStage(self.game, self.win))

    def goNivelOne(self):
        self.game.changeState(NivelOne(self.game, self.win))
    
    def goNivelTwo(self):
        self.game.changeState(NivelTwo(self.game, self.win))

    def goNivelCreate(self):
        self.game.changeState(NivelCreate(self.game, self.win))

    def __loadComponents(self):
        self.arrayComponente.append(
            Component(self.win, pg.image.load("../assets/select/bg.jpg"), None, 0, 0, 0))
        self.arrayComponente.append(
            Component(self.win, pg.image.load("../assets/select/tabla.png"), None, 15, 200, 0))
        self.arrayComponente.append(
            Component(self.win, pg.image.load("../assets/select/tabla.png"), None, 330, 200, 0))
        self.arrayComponente.append(
            Component(self.win, pg.image.load("../assets/select/tabla.png"), None, 645, 200, 0))

        self.arrayComponente.append(
            Component(self.win, pg.image.load("../assets/select/level_one.png"), None, 40, 225, 0))
        self.arrayComponente.append(
            Component(self.win, pg.image.load("../assets/select/level_two.png"), None, 355, 215, 0))
        self.arrayComponente.append(
            Component(self.win, pg.image.load("../assets/select/level_create.png"), None, 670, 215, 0))

        self.arrayComponente.append(self.One)
        self.arrayComponente.append(self.Two)
        self.arrayComponente.append(self.create)
        

        self.arrayComponente.append(self.back)

class NivelTwo():
    def __init__(self, game, win):
        self.game = game
        self.win = win
        self.arrayComponente = []
        self.bg = Component(win, pg.image.load(
            "../assets/two/f.png"), None, 0, 0, 0)
        self.floor = Component(win, pg.image.load(
            "../assets/two/floor.png"), None, 0, FLOOR, 0)    
        self.win.blit(self.bg.currentImage, (0, 0))
        self.bgWidth, self.bgHeight = self.bg.currentImage.get_rect().size
        self.stageWidth = self.bgWidth * 4
        self.startScrollingPosX = HW
        self.stagePosX = 0
        self.pauseState = False
        self.loseState = False
        self.winState = False
        self.name = ""
        # CONJUNTO DE IMAGENES
        self.players = pg.sprite.Group()
        self.enemys = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.flags = pg.sprite.Group()
        self.bases = pg.sprite.Group()
        self.lifes = pg.sprite.Group()
        self.tumis = pg.sprite.Group()
        self.foods = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.spritesheet = Spritesheet("../assets/two/player{}.png".format(self.game.suit))
        self.spritesheet_enemy = Spritesheet("../assets/two/enemy2.png")
        #ADD PLAYER
        self.player = Player(self)
        self.players.add(self.player)
        #ADD ENEMY
        self.enemy1 = Enemy(self, 600, FLOOR-65,2)
        self.enemy2 = Enemy(self, 1000, FLOOR-65,2)
        self.enemys.add(self.enemy1)
        self.enemys.add(self.enemy2)
        #ADD PLATFORMS
        base = Platform(0, FLOOR , 3*WIDTH, HEIGHT - FLOOR,"")
        base.image.set_alpha(0) 
        pt = Platform(200 , FLOOR - 25 , 100 , 20,"1")
        p1 = Platform(750 , FLOOR - 100 , 100 , 20,"1")
        p2 = Platform(1135.5 , FLOOR - 100 , 100 , 20,"1")
        p3 = Platform(1411 , FLOOR - 200 , 50 , 20,"2")
        p4 = Platform(1636.5 , FLOOR - 100 , 100 , 20,"1")
        p5 = Platform(2350 , FLOOR - 100 , 100 , 20,"1")
        p6 = Platform(3055.5 , FLOOR - 100 , 100 , 20,"1")
        p7 = Platform(3331 , FLOOR - 200 , 50 , 20,"2")
        p8 = Platform(3556.5 , FLOOR - 100 , 100 , 20,"1")
        self.bases.add(base)
        self.platforms.add(pt)
        self.platforms.add(p1)
        self.platforms.add(p2)
        self.platforms.add(p3)
        self.platforms.add(p4)
        self.platforms.add(p5)
        self.platforms.add(p6)
        self.platforms.add(p7)
        self.platforms.add(p8)
        #ADD LIFE
        l1 = Life(1423.5 , FLOOR - 225)
        l2 = Life(3343.5 , FLOOR - 225)
        self.lifes.add(l1)
        self.lifes.add(l2)
        #ADD TUMIS
        t1 = Tumi(1674 ,FLOOR - 150)
        t2 = Tumi(3093 ,FLOOR - 150)
        self.tumis.add(t1)
        self.tumis.add(t2)
        #ADD FOOD
        f1 = Food(1160 , FLOOR - 125)
        self.foods.add(f1)
        #ADD FLAG
        flag  = Flag(self.stageWidth-30,FLOOR-100)
        self.flags.add(flag)
        #LETRA
        self.myfont = pg.font.SysFont("monospace", 20, True)
        self.myfontNumber = pg.font.SysFont("monospace", 30, True)
        #PUNTAJE
        self.poits = 0
        #LIFES
        self.lifes_points = 1
        #FOOD
        self.nfoods = 0
        #LOAD IMAGES
        self.image_life = pg.image.load('../assets/two/life.png')
        #LOAD COMPONENTS
        self.arrayComponents = []
        self.arrayPause = []
        self.arrayLose = []
        self.arrayWin = []
        self.pause = Component(win , pg.image.load(
            "../assets/two/pause.png") , None , 905 , 5 , 0)
        #LOAD COMPONENTS PAUSE
        self.marco_pause = Component(win , pg.image.load(
            "../assets/pause/pause_marco.png") , None ,280 , 160 , 0)
        self.play = Component(win, pg.image.load("../assets/pause/btn_play.png"),
                              pg.image.load("../assets/pause/btn_alt_play.png"), 325.3, 250, 1)
        self.exit = Component(win, pg.image.load("../assets/pause/btn_exit.png"),
                              pg.image.load("../assets/pause/btn_alt_exit.png"), 502.6, 250, 1)
        
        #LOAD COMPONENTS LOSE / WIN
        self.marco = Component(win , pg.image.load(
            "../assets/lose/tabla.png") , None ,230 , 70 , 0)
        self.marco_win = Component(win , pg.image.load(
            "../assets/lose/tabla_win.png") , None ,230 , 70 , 0)
        self.game_over_title = Component(win , pg.image.load(
            "../assets/lose/game_over_title.png") , None ,262 , 127 , 0)
        self.win_title = Component(win , pg.image.load(
            "../assets/lose/win_title.png") , None ,262 , 127 , 0)
        self.save = Component(win, pg.image.load("../assets/lose/btn_guardar.png"),
                              pg.image.load("../assets/lose/btn_alt_guardar.png"), 325.3, 453, 1)
        self.exit_lose = Component(win, pg.image.load("../assets/lose/btn_exit.png"),
                              pg.image.load("../assets/lose/btn_alt_exit.png"), 502.6, 453, 1)
        self.continue_win = Component(win, pg.image.load("../assets/lose/btn_exit.png"),
                              pg.image.load("../assets/lose/btn_alt_exit.png"), 414, 368, 1)
        self.player_dead = Component(win, pg.image.load(
            "../assets/lose/player_{}_dead.png".format(self.game.suit)), None, 415, 250, 1)
        self.player_win = Component(win, pg.image.load(
            "../assets/lose/player_{}_win.png".format(self.game.suit)), None, 415, 250, 1)
        self.lose_tumi = Component(win, pg.image.load(
            "../assets/lose/tumi.png"), None, 310, 250, 1)
        self.lose_food = Component(win, pg.image.load(
            "../assets/lose/food.png"), None, 600, 270, 1)
        
        self.__loadComponents()
        
    def draw(self):
        self.bases.draw(self.win)
        self.players.draw(self.win)
        self.enemys.draw(self.win)
        self.platforms.draw(self.win)
        self.lifes.draw(self.win)
        self.tumis.draw(self.win)
        self.foods.draw(self.win)
        self.bullets.draw(self.win)
        self.flags.draw(self.win)
        #RENDER POINTS
        label = self.myfont.render("PUNTAJE : {}".format(self.poits), 1, BLACK)
        self.win.blit(label, (5, 0))
        #RENDER LIFE
        lifes = self.myfont.render("VIDAS : ", 1, BLACK)
        place  = HW +  100
        self.win.blit(lifes, (HW, 0))
        for l in range(self.lifes_points):
            self.win.blit(self.image_life , (place, 0))
            place += 30
        for component in self.arrayComponents:
            component.draw()
        if  self.pauseState:
            for component in self.arrayPause:
                component.draw()
                component.hover()
        if self.loseState:
            for component in self.arrayLose:
                component.draw()
                component.hover()
            #RENDER NAME
            pg.draw.rect(self.win,(255,255,255),(330,400,300,40))
            n = self.myfont.render(self.name, 1, BLACK)
            self.win.blit(n, (350,410))
            s_tumis = self.myfontNumber.render(str(self.poits), 1, BLACK)
            s_food = self.myfontNumber.render(str(self.nfoods), 1, BLACK)
            self.win.blit(s_tumis, (320, 355))
            self.win.blit(s_food, (620, 330))
        if self.winState:
            for component in self.arrayWin:
                component.draw()
                component.hover()
            s_tumis = self.myfontNumber.render(str(self.poits), 1, BLACK)
            s_food = self.myfontNumber.render(str(self.nfoods), 1, BLACK)
            self.win.blit(s_tumis, (320, 355))
            self.win.blit(s_food, (620, 330))

    def events(self):
        mouse = pg.mouse.get_pos()
        move = 0
        k = pg.key.get_pressed()
        if k[pg.K_RIGHT]:
            move  = 1
            self.player.side = 1
        elif k[pg.K_LEFT]:
            move = -1
            self.player.side = -1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if not self.pauseState and  not self.loseState and not self.winState:
                if event.type == pg.KEYDOWN:
                    if  event.key == pg.K_UP:
                        self.player.jump(2)
                    if event.key == pg.K_SPACE:
                        self.player.shoot()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.pause.inside(mouse[0], mouse[1]):
                        self.goPause(True)
            if self.pauseState:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.play.inside(mouse[0], mouse[1]):
                        self.goPause(False)
                    if self.exit.inside(mouse[0], mouse[1]):
                        self.goMenu()
            if self.loseState:
                if event.type == pg.KEYDOWN:
                    if event.unicode.isalpha():
                        self.name += event.unicode
                    elif event.key == pg.K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif event.key == pg.K_RETURN:
                        self.name = ""
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.save.inside(mouse[0], mouse[1]):
                        self.save_score()
                    if self.exit_lose.inside(mouse[0], mouse[1]):
                        self.goMenu()
            if self.winState:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.exit_lose.inside(mouse[0], mouse[1]):
                        self.goMenu()
                        

        if not self.pauseState and not self.loseState and not self.winState:
            self.player.move(move)
            self.move_screen(move)

    def update(self):
        self.bullets.update()
        for enemy in self.enemys:
            enemy.animate()
        self.player.jumping = True
        #CHECK IF PLAYER HIT THE FLOOR
        hit_floor = pg.sprite.spritecollide(self.player , self.bases , False)
        if hit_floor:
                self.player.jumping = False
                self.player.pos.y = hit_floor[0].rect.top - 2
                self.player.vel.y = 0

        #CHECK IF PLAYER HIT A PLATFOR
        if  self.player.vel.y > 0:
            hits_platfroms = pg.sprite.spritecollide(self.player , self.platforms , False)
            if hits_platfroms:
                self.player.jumping = False
                self.player.pos.y = hits_platfroms[0].rect.top - 2
                self.player.vel.y = 0

        #CHECK HIT A LIFE
        hits_lifes = pg.sprite.spritecollide(self.player, self.lifes , False)
        if hits_lifes:
            self.game.life_sound()
            self.lifes.remove(hits_lifes[0])
            self.lifes_points += 1
        #CHECK HIT A TUMI
        hits_tumis = pg.sprite.spritecollide(self.player, self.tumis , False)
        if hits_tumis:
            self.game.coin_sound()
            self.tumis.remove(hits_tumis[0])
            self.poits += 10
        #CHECK HIT A FOOD
        hits_food = pg.sprite.spritecollide(self.player, self.foods , False)
        if hits_food:
            self.game.food_sound()
            self.foods.remove(hits_food[0])
            self.nfoods += 5
        
        #CHECK HIT TO ENMY
        hits_enemy = pg.sprite.spritecollide(self.player, self.enemys , False)
        if hits_enemy:
            self.loseState = True
        
        #CHECK IF BULLET TO ENEMY
        for bullet in self.bullets:
            hits_bullet =  pg.sprite.spritecollide(bullet, self.enemys , True)
            if hits_bullet:
                self.poits += 20
                bullet.kill()
        #CHECK IF WIIN
        hits_flag = pg.sprite.spritecollide(self.player, self.flags , False)
        if hits_flag:
            self.winState = True

    def __loadComponents(self):
        self.arrayComponents.append(self.pause)
        self.arrayPause.append(self.marco_pause)
        self.arrayPause.append(self.play)
        self.arrayPause.append(self.exit)
        self.arrayLose.append(self.marco)
        self.arrayLose.append(self.exit_lose)
        self.arrayLose.append(self.save)
        self.arrayLose.append(self.game_over_title)
        self.arrayLose.append(self.player_dead)
        self.arrayLose.append(self.lose_tumi)
        self.arrayLose.append(self.lose_food)
        self.arrayWin.append(self.marco_win)
        self.arrayWin.append(self.continue_win)
        self.arrayWin.append(self.win_title)
        self.arrayWin.append(self.player_win)
        self.arrayWin.append(self.lose_tumi)
        self.arrayWin.append(self.lose_food)

    def goPause(self, state):
        self.pauseState = state

    def goMenu(self):
        self.game.changeState(MenuStage(self.game, self.win))

    def move_screen(self, dir):
        rel_x = round(self.stagePosX % self.bgWidth,0)
        self.win.blit(self.bg.currentImage,
                            (rel_x - self.bgWidth, 0))
        self.win.blit(self.floor.currentImage,
                            (rel_x - self.bgWidth, FLOOR))
        
        if rel_x < WIDTH:
            self.win.blit(self.bg.currentImage, (rel_x, 0))
            self.win.blit(self.floor.currentImage, (rel_x, FLOOR))
        if self.player.rect.center[0] == self.startScrollingPosX:
            self.platforms.update(self.player.des)
            self.lifes.update(self.player.des)
            self.tumis.update(self.player.des)
            self.foods.update(self.player.des)
            self.enemys.update(self.player.des)
            self.flags.update(self.player.des)
    
    def save_score(self):
        payload = {"nombre" : self.name , "puntaje" : self.poits}
        r = requests.post(URL_API + "/ranking", data=payload)
        print("Status : {}".format(r.status_code))
        self.goMenu()

class NivelCreate():
    def __init__(self, game, win):
        self.database = Database()
        self.game = game
        self.win = win
        self.arrayComponente = []
        self.arrayBackground = []
        self.arrayEnemy = []
        self.arrayWeapon = []
        self.background = 1
        self.enemy = 1
        self.weapon = 1
        self.f_1 = Component(win, pg.image.load("../assets/create/f_1.png"),
                                pg.image.load("../assets/create/f_s_1.png"), 330, 10, 1)
        self.f_2 = Component(win, pg.image.load("../assets/create/f_2.png"),
                                pg.image.load("../assets/create/f_s_2.png"), 540, 10, 1)
        self.f_3 = Component(win, pg.image.load("../assets/create/f_3.png"),
                                pg.image.load("../assets/create/f_s_3.png"), 750, 10, 1)
        self.e_1 = Component(win, pg.image.load("../assets/create/e_1.png"),
                                      pg.image.load("../assets/create/e_s_1.png"), 400, 220, 1)
        self.e_2 = Component(win, pg.image.load("../assets/create/e_2.png"),
                                      pg.image.load("../assets/create/e_s_2.png"), 680, 220, 1)
        self.w_1 = Component(win, pg.image.load("../assets/create/p_1.png"),
                                pg.image.load("../assets/create/p_s_1.png"), 410, 430, 1)
        self.w_2 = Component(win, pg.image.load("../assets/create/p_2.png"),
                                pg.image.load("../assets/create/p_s_2.png"), 620, 430, 1)
        self.w_3 = Component(win, pg.image.load("../assets/create/p_3.png"),
                                pg.image.load("../assets/create/p_s_3.png"), 830, 430, 1)
        self.back = Component(win, pg.image.load(
            "../assets/options/back.png"), None, 10, 10, 0)

        self.run = Component(win, pg.image.load(
            "../assets/create/run.png"), None, 880, 540, 0)

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
                    self.goSelect()
                if self.run.inside(mouse[0], mouse[1]):
                    self.game.click_sound()
                    self.goNivelThree()
                for b in self.arrayBackground:
                    if b.inside(mouse[0], mouse[1]):
                        self.game.click_sound()
                        self.__active_group(self.arrayBackground, b, "BG")
                for e in self.arrayEnemy:
                    if e.inside(mouse[0], mouse[1]):
                        self.game.click_sound()
                        self.__active_group(self.arrayEnemy, e, "ENEMY")
                for w in self.arrayWeapon:
                    if w.inside(mouse[0], mouse[1]):
                        self.game.click_sound()
                        self.__active_group(self.arrayWeapon, w, "WEAPON")

    def update(self):
        pass

    def goOptions(self):
        pass

    def goSelect(self):
        self.game.changeState(SelectLevel(self.game, self.win))

    def goNivelThree(self):
        self.game.changeState(NivelThree(self.game, self.win, self.background, self.enemy, self.weapon))

    def __loadComponents(self, win):
        self.arrayComponente.append(
            Component(win, pg.image.load("../assets/options/bg.jpg"), None, 0, 0, 0))
        self.arrayComponente.append(Component(win, pg.image.load(
            "../assets/create/fondo.png"), None, 25, 82.5, 0))
        self.arrayBackground.append(self.f_1)
        self.arrayBackground.append(self.f_2)
        self.arrayBackground.append(self.f_3)
        self.arrayComponente = self.arrayComponente + self.arrayBackground
        self.arrayComponente.append(Component(win, pg.image.load(
            "../assets/create/enemigo.png"), None,25 , 292.5, 0))
        self.arrayEnemy.append(self.e_1)
        self.arrayEnemy.append(self.e_2)
        self.arrayComponente = self.arrayComponente + self.arrayEnemy
        self.arrayWeapon.append(self.w_1)
        self.arrayWeapon.append(self.w_2)
        self.arrayWeapon.append(self.w_3)
        self.arrayComponente = self.arrayComponente + self.arrayWeapon
        self.arrayComponente.append(self.back)
        self.arrayComponente.append(self.run)

    def __init_componets(self):
        self.arrayBackground[0].active(True)
        self.arrayEnemy[0].active(True)
        self.arrayWeapon[0].active(True)

    def __active_group(self, group, element, type):
        element.active(True)
        index = group.index(element)
        if type == "BG":
            self.background = index + 1
        if type == "ENEMY":
            self.enemy = index + 1
        if type == "WEAPON":
            self.weapon = index + 1
        for component in group:
            if group.index(component) != index:
                component.active(False)

class NivelThree():
    def __init__(self, game, win, background, enemy , weapon):
        self.game = game
        self.win = win
        self.arrayComponente = []
        self.bg = Component(win, pg.image.load(
            "../assets/three/f{}.png".format(background)), None, 0, 0, 0)
        self.win.blit(self.bg.currentImage, (0, 0))
        self.bgWidth, self.bgHeight = self.bg.currentImage.get_rect().size
        self.stageWidth = self.bgWidth
        self.startScrollingPosX = HW
        self.stagePosX = 0
        self.pauseState = False
        self.loseState = False
        self.winState = False
        self.name = ""
        # CONJUNTO DE IMAGENES
        self.players = pg.sprite.Group()
        self.monsters = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.spritesheet = Spritesheet("../assets/one/player{}.png".format(self.game.suit))
        self.spritesheet_enemy = Spritesheet("../assets/three/enemy{}.png".format(enemy))
        #ADD PLAYER
        self.player = Player(self,weapon)
        self.players.add(self.player)
        #ADD MONSTERS
        self.monster1 = Monster(self,100,100,enemy,1)
        self.monsters.add(self.monster1)
        #LETRA
        self.myfont = pg.font.SysFont("monospace", 20, True)
        #LOAD COMPONENTS
        self.arrayComponents = []
        self.arrayPause = []
        self.arrayLose = []
        self.arrayWin = []
        self.pause = Component(win , pg.image.load(
            "../assets/one/pause.png") , None , 905 , 5 , 0)
        #LOAD COMPONENTS PAUSE
        self.marco_pause = Component(win , pg.image.load(
            "../assets/pause/pause_marco.png") , None ,280 , 160 , 0)
        self.play = Component(win, pg.image.load("../assets/pause/btn_play.png"),
                              pg.image.load("../assets/pause/btn_alt_play.png"), 325.3, 250, 1)
        self.exit = Component(win, pg.image.load("../assets/pause/btn_exit.png"),
                              pg.image.load("../assets/pause/btn_alt_exit.png"), 502.6, 250, 1)
        
        #LOAD COMPONENTS LOSE / WIN
        self.marco = Component(win , pg.image.load(
            "../assets/lose/tabla.png") , None ,230 , 70 , 0)
        self.marco_win = Component(win , pg.image.load(
            "../assets/lose/tabla_win.png") , None ,230 , 70 , 0)
        self.game_over_title = Component(win , pg.image.load(
            "../assets/lose/game_over_title.png") , None ,262 , 127 , 0)
        self.win_title = Component(win , pg.image.load(
            "../assets/lose/win_title.png") , None ,262 , 127 , 0)
        self.save = Component(win, pg.image.load("../assets/lose/btn_guardar.png"),
                              pg.image.load("../assets/lose/btn_alt_guardar.png"), 325.3, 453, 1)
        self.exit_lose = Component(win, pg.image.load("../assets/lose/btn_exit.png"),
                              pg.image.load("../assets/lose/btn_alt_exit.png"), 502.6, 453, 1)
        self.continue_win = Component(win, pg.image.load("../assets/lose/btn_exit.png"),
                              pg.image.load("../assets/lose/btn_alt_exit.png"), 414, 368, 1)
        self.player_dead = Component(win, pg.image.load(
            "../assets/lose/player_{}_dead.png".format(self.game.suit)), None, 415, 250, 1)
        self.player_win = Component(win, pg.image.load(
            "../assets/lose/player_{}_win.png".format(self.game.suit)), None, 415, 250, 1)
        self.lose_tumi = Component(win, pg.image.load(
            "../assets/lose/tumi.png"), None, 310, 250, 1)
        self.lose_food = Component(win, pg.image.load(
            "../assets/lose/food.png"), None, 600, 270, 1)
        
        self.__loadComponents()
        
    def draw(self):
        self.players.draw(self.win)
        self.monsters.draw(self.win)
        self.bullets.draw(self.win)
        for component in self.arrayComponents:
            component.draw()
        if  self.pauseState:
            for component in self.arrayPause:
                component.draw()
                component.hover()
        if self.loseState:
            for component in self.arrayLose:
                component.draw()
                component.hover()
            #RENDER NAME
            pg.draw.rect(self.win,(255,255,255),(330,400,300,40))
            n = self.myfont.render(self.name, 1, BLACK)
            self.win.blit(n, (350,410))
        if self.winState:
            for component in self.arrayWin:
                component.draw()
                component.hover()

    def events(self):
        mouse = pg.mouse.get_pos()
        move = 0
        k = pg.key.get_pressed()
        if k[pg.K_RIGHT]:
            move  = 1
            self.player.side = 1
        elif k[pg.K_LEFT]:
            move = -1
            self.player.side = -1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if not self.pauseState and  not self.loseState and not self.winState:
                if event.type == pg.KEYDOWN:
                    if  event.key == pg.K_SPACE:
                        self.player.jump(3)
                    if event.key == pg.K_TAB:
                        self.player.shoot()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.pause.inside(mouse[0], mouse[1]):
                        self.goPause(True)
            if self.pauseState:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.play.inside(mouse[0], mouse[1]):
                        self.goPause(False)
                    if self.exit.inside(mouse[0], mouse[1]):
                        self.goMenu()
            if self.loseState:
                if event.type == pg.KEYDOWN:
                    if event.unicode.isalpha():
                        self.name += event.unicode
                    elif event.key == pg.K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif event.key == pg.K_RETURN:
                        self.name = ""
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.save.inside(mouse[0], mouse[1]):
                        pass
                    if self.exit_lose.inside(mouse[0], mouse[1]):
                        self.goMenu()
            if self.winState:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.exit_lose.inside(mouse[0], mouse[1]):
                        self.goMenu()
                        

        if not self.pauseState and not self.loseState and not self.winState:
            self.player.move(move)
            self.move_screen(move)

    def update(self):
        self.bullets.update()
        if not self.pauseState and not self.loseState and not self.winState:
            self.monsters.update()

    def __loadComponents(self):
        self.arrayComponents.append(self.pause)
        self.arrayPause.append(self.marco_pause)
        self.arrayPause.append(self.play)
        self.arrayPause.append(self.exit)
        self.arrayLose.append(self.marco)
        self.arrayLose.append(self.exit_lose)
        self.arrayLose.append(self.save)
        self.arrayLose.append(self.game_over_title)
        self.arrayLose.append(self.player_dead)
        self.arrayWin.append(self.marco_win)
        self.arrayWin.append(self.continue_win)
        self.arrayWin.append(self.win_title)
        self.arrayWin.append(self.player_win)

    def goPause(self, state):
        self.pauseState = state

    def goMenu(self):
        self.game.changeState(MenuStage(self.game, self.win))

    def move_screen(self, dir):
        rel_x = round(self.stagePosX % self.bgWidth,0)
        self.win.blit(self.bg.currentImage,
                            (rel_x - self.bgWidth, 0))
        
        if rel_x < WIDTH:
            self.win.blit(self.bg.currentImage, (rel_x, 0))

    