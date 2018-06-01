import pygame , sys

class Component():

    def __init__(self, win, image,alternative , x, y, type):
        self.win = win
        self.currentImage = image
        self.imagePrincipal = image
        self.alternative = alternative
        self.x = x
        self.y = y
        self.type = type
        self.pressed = False
        # TYPE
        # 0: Componente flotante 
        # 1 : boton de seleccion
    
    def draw(self):
        self.win.blit(self.currentImage,(self.x, self.y))
        
    def hover(self):
        if self.pressed == False :
            if self.alternative != None:
                mouse = pygame.mouse.get_pos()
                if self.inside(mouse[0], mouse[1]):
                    self.currentImage = self.alternative
                else:
                    self.currentImage = self.imagePrincipal

    def active(self, state):
        if state == True:
            self.pressed = True
            self.currentImage = self.alternative
        else:
            self.pressed = False
            self.currentImage = self.imagePrincipal

    def actions(self,event):
        pass

    def inside(self,pos_x,pos_y):
        if((self.x + 132) > pos_x > self.x and (self.y + 60) > pos_y > self.y):
            return True
        return False
    
