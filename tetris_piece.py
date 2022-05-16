# Créé par mchedor, le 25/04/2022 en Python 3.7
import pygame
from pygame.locals import *
import time

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
    def get_coord(self):
        return (self.x,self.y)
    def get_coordp(self):
        return (self.xp,self.yp)
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
    def destroy(self,r=False):
        self.draw(color=(0,0,0),r=r)

    def __repr__(self):
        return "x "+str(self.xp)+"  y "+str(self.yp)

    def __str__(self):
        return self.name
    def __int__(self):
        return self.id
    def __(self):
        return (self.xp,self.yp,self.id)


class Piece(Pixel):
    def __init__(self,surface,id,name,color=(1,1,1),x=0,y=0,debug=2):
        super().__init__(surface,id,name,color,x,y,debug)
        self.shape=[[10, 1,20],
                    [-1,00,-1]]
        self.Repere00Table=(0,0)
        # -1 = hors de porter
        # _0 = a checker:
                        #00 =  bas(s)
                        #10 = gauche(q)
                        #20 = droite(d)
        # _1 = hitbox de la piece

    def movetesting(self,table):
        print("\n\nmovetseting_debut")
        direction="sqd"#fleme de modifier donc c'est un copier coller
        coordss=self.coordsIdShape(10,20,00)
        gauches,droites,bas=coordss[10],coordss[20],coordss[00]
        print(coordss)
        if "s" in direction:
            s=[]
            for i in bas:
                print("table",table[i[1]][i[0]],"xy",repr(table[i[1]][i[0]]))
                if table[i[1]][i[0]]:
                    #print("probleme?",table[i[0]][i[1]])
                    s.append(False)
                else:
                    s.append(True)
            if True in s:
                s=True
            else:
                s=False


        if "q" in direction:
            q=[]
            for i in gauches:
                if table[i[1]][i[0]]:
                    q.append(False)
                else:
                    q.append(True)
            if True in q:
                q=True
            else:
                q=False


        if "d" in direction:
            d=[]
            for i in droites:
                if table[i[1]][i[0]]:
                    d.append(False)
                else:
                    d.append(True)
            if True in d:
                d=True
            else:
                d=False
        print({"s":s,"q":q,"d":d})
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
            self.draw(r=True)

    def draw(self,color=(),r=False):
        if not color:
            color=self.color
        #pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(self.x, self.y, 32, 32))
        coords=self.coordsIdShape(1,11)
        print(coords)
        for i in coords:
            if coords[i]:
                x,y=coords[i][0]

            pygame.draw.rect(self.surface, color, pygame.Rect(x*32+2+32, y*32+32+2, 32-2, 32-2))
            if self.debug==2:
                print(self.x/32,self.y/32)
            if r:
                print("R",x,y)

    def coordsIdShape(self,*ids):
        PixelPieceRepere=[(j,i) for i,x in enumerate(self.shape) for j,x2 in enumerate(x) if x2==1]#le point repere(1) qui corespond au coordone x et y
        PixelPieceRepere=PixelPieceRepere[0]
        coordss={}
        for k in ids:
            coordss[k]=[(j-PixelPieceRepere[0]+self.xp-self.Repere00Table[0],i-PixelPieceRepere[1]+self.yp-self.Repere00Table[1]) for i,x in enumerate(self.shape) for j,x2 in enumerate(x) if x2==k]
        return coordss
        #coordonerMONDE=(coordonerLIEU-coordonerRepereLIEUX+coordonerRepereMONDE)=>
        #=> cM=(cLx-crLx+crMx,cLy-crLy+crMy)




class Carre(Piece):
    def __init__(self,surface,id,name,color=(1,1,1),x=0,y=0,debug=0):
        super().__init__(surface,id,name,color,x,y,debug)
        forme= [[10,11,1,20],
                [10,11,11,20],
                [0,00,00,0],]











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
    piece=Piece(fenetre,8,"piece",color=(0,255,0),x=4,y=1)
    piece.draw()
    pygame.display.flip()
    cuvette=[[0,0,0,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1]]
    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0
        time.sleep(1)
        if piece.movetesting(cuvette)["s"]:
            piece.move("s")
            print("move", piece.get_coordp())
        else:
            pxpyp=piece.get_coordp()
            cuvette[pxpyp[0]][pxpyp[1]]=piece
            piece=Piece(fenetre,8,"piece",color=(0,255,0),x=3,y=2)
            piece.draw()
        pygame.display.flip()
    pygame.quit()
