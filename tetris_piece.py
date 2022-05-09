# Créé par mchedor, le 25/04/2022 en Python 3.7
import pygame
from pygame.locals import *

class Pixel:
    def __init__(self,surface,id,name,color=(1,1,1),x=0,y=0,debug=0):
        self.debug=debug

        self.name=name
        self.id=int(id)
        self.xp=x
        self.yp=y
        self.color = color
        self.x=x*32+32
        self.y=y*32+32
        self.surface=surface

    def set_color(self,color):
        self.color = (255,0,0)
    def set_coordp(self,x,y):
        self.xp=x
        self.yp=y
        self.x=x*32+32
        self.y=y*32+32
    def get_coordp(self):
        return (self.x,self.y)
    def set_draw(self,x,y):
        self.x=x+32*32
        self.y=y+32*32
        self.draw()
    def draw(self,color=(),r=False):
        if not color:
            color=self.color
        #pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(self.x, self.y, 32, 32))
        pygame.draw.rect(self.surface, color, pygame.Rect(self.x+2, self.y+32+2, 32-2, 32-2))
        if self.debug==2:
            print(self.x,self.y)
        if r:
            print(self.x,self.y)

    def __repr__(self):
        return self.id

    def __str__(self):
        return self.name


class Piece(Pixel):
    def __init__(self,surface,id,name,color=(1,1,1),x=0,y=0,debug=0):
        super().__init__(surface,id,name,color,x,y,debug)

    def movetesting(self,table):
        direction="sqd"#fleme de modifier donc c'est un copier coller
        if "s" in direction:
            if table[self.yp+1][self.xp]:
                s=False
            else:
                s=True
        if "q" in direction:
            if table[self.yp][self.xp-1]:
                q=False
            else:
                q=True
        if "d" in direction:
            if table[self.yp][self.xp+1]:
                d=False
            else:
                d=True
        return {"s":s,"q":q,"d":d}

    def move(self, direction,draw=1):
        if draw:
            self.draw(color=(0,0,0))
        if "s" in direction:
            self.y+=32
            self.yp+=1
        if "q" in direction:
            self.x-=32
            self.xp-=1
        if "d" in direction:
            self.x+=32
            self.xp+=1
        if draw:
            self.draw()








if __name__=="__main__":
    x=8
    y=16
    xp=x*32
    yp=y*32
    pygame.init()
    fenetre = pygame.display.set_mode((xp+32*2, yp+32*2))
    continuer = 1
    red=(255,0,0)
    c1=Piece(fenetre,1,"test",color=red,x=0,y=0)
    c1.draw()
    pygame.display.flip()
    #Boucle infinie
    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0
    pygame.quit()
