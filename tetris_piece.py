# Créé par mchedor, le 25/04/2022 en Python 3.7
import pygame
from pygame.locals import *
import time

COLOR_BARRE=(0, 255, 255)#blue sky
COLOR_CARRE=(255, 255, 0)#yellow
COLOR_S=(255, 0, 0)#red
COLOR_Z=(0, 255, 0)#green
COLOR_L=(255, 127, 0)#orange
COLOR_J=(0, 0, 255)#blue
COLOR_T=(128, 0, 128)#purple


class Pixel:
    def __init__(self,surface,id,name,color=(1,1,1),x=0,y=0,debug=0):
        self.debug=debug

        self.name=name
        self.id=int(id)
        self.xp=x
        self.yp=y
        self.x=x*32+32
        self.y=y*32+32
        self.color=color
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
            #print(self.x,self.y)
            pass
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
    def direction_coords(self):
        coordss=self.coordsIdShape(10,20,00)
        gauches,droites,bas=coordss[10],coordss[20],coordss[00]
        return (gauches,droites,bas)

    def movetesting(self,table):
        try:
            #print("\n\nmovetseting_debut")
            direction="sqd"#fleme de modifier donc c'est un copier coller
            coordss=self.coordsIdShape(10,20,00)
            gauches,droites,bas=self.direction_coords()
            #print(coordss)
            if "s" in direction:
                s=[]
                #print("bas  bas",bas)
                for i in bas:
                    #print("table",table[i[1]][i[0]],"xy",repr(table[i[1]][i[0]]))
                    if table[i[1]][i[0]]:
                        #print("probleme?",table[i[0]][i[1]])
                        s.append(False)
                    else:
                        s.append(True)
                if False in s:
                    s=False
                else:
                    s=True


            if "q" in direction:
                q=[]
                for i in gauches:
                    if table[i[1]][i[0]]:
                        q.append(False)
                    else:
                        q.append(True)
                if False in q:
                    q=False
                else:
                    q=True


            if "d" in direction:
                d=[]
                for i in droites:
                    if table[i[1]][i[0]]:
                        d.append(False)
                    else:
                        d.append(True)
                if False in d:
                    d=False
                else:
                    d=True

        except IndexError as err:
            #print("IndexError: {0}".format(err))
            #print("ERROR : ")
            return {"s":False,"q":False,"d":False,"o":self.rotation_testing(table)}
        #print({"s":s,"q":q,"d":d,"o":self.rotation_testing(table)})
        return {"s":s,"q":q,"d":d,"o":self.rotation_testing(table)}


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
        if "o" in direction:
            self.rotation()
        if draw:
            self.draw(r=True)
        #print("\t\t   movemove xy",self.xp,self.yp)
    def draw(self,color=(),r=False):
        if not color:
            color=self.color
        #pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(self.x, self.y, 32, 32))
        coords=self.coordsIdShape(1,11)
        #print(coords)
        coord=[j for i in coords for j in coords[i]]
        for i in range(len(coord)):
            if coord[i]:
                x,y=coord[i]

            pygame.draw.rect(self.surface, color, pygame.Rect(x*32+2+32, y*32+32+2, 32-2, 32-2))
            if self.debug==2:
                #print(self.x/32,self.y/32)
                pass
            if r:
                #print("R",x,y)
                pass

    def coordsIdShape(self,*ids,table=False,xt=0,yt=0):
        if not yt and not xt:
            xt,yt=self.xp,self.yp
        if not table:
            table=self.shape
        PixelPieceRepere=[(j,i) for i,x in enumerate(table) for j,x2 in enumerate(x) if x2==1]#le point repere(1) qui corespond au coordone x et y
        PixelPieceRepere=PixelPieceRepere[0]
        coordss={}
        for k in ids:
            coordss[k]=[(j-PixelPieceRepere[0]+xt-self.Repere00Table[0],i-PixelPieceRepere[1]+yt-self.Repere00Table[1]) for i,x in enumerate(table) for j,x2 in enumerate(x) if x2==k]
        return coordss
        #coordonerMONDE=(coordonerLIEU-coordonerRepereLIEUX+coordonerRepereMONDE)=>
        #=> cM=(cLx-crLx+crMx,cLy-crLy+crMy)
    def rotation(self):
        pass
    def rotation_testing(self,table,x=0,y=0):
        return True



class Carre(Piece):
    def __init__(self,surface,id,name,color=COLOR_CARRE,x=0,y=0,debug=0):
        super().__init__(surface,id,name,color,x,y,debug)
        self.shape= [[10,11,1,20],
                [10,11,11,20],
                [-1,00,00,-1],]

class Barre(Piece):
    def __init__(self,surface,id,name,color=COLOR_BARRE,x=0,y=0,debug=0):
        super().__init__(surface,id,name,color,x,y,debug)

        self.shape= [[10,11,20],
                     [10,11,20],
                     [10, 1,20],
                     [10,11,20],
                     [-1,00,-1],]
        self.shapes=[[[10,11,11,1,11,20],
                     [-1,00,00,00,00,-1]],

                     [[10,11,20],
                     [10,11,20],
                     [10, 1,20],
                     [10,11,20],
                     [-1,00,-1],],

                     [[10,11,1,11,11,20],
                     [-1,00,00,00,00,-1]],

                     [[10,11,20],
                     [10,1,20],
                     [10,11,20],
                     [10,11,20],
                     [-1,00,-1],]]
        self.shapes_alternative=[[[[10,11,11,1,11,20],
                     [-1,00,00,00,00,-1]],

                     [[10,11,11,11,1,20],
                     [-1,00,00,00,00,-1]],

                     [[10,11,1,11,11,20],
                     [-1,00,00,00,00,-1]],

                     [[10,1,11,11,11,20],
                     [-1,00,00,00,00,-1]]],

                     [[[10,11,20],
                     [10,11,20],
                     [10, 1,20],
                     [10,11,20],
                     [-1,00,-1]],

                     [[10,11,20],
                     [10,11,20],
                     [10,11,20],
                     [10,1,20],
                     [-1,00,-1]],

                     [[10,11,20],
                     [10,1,20],
                     [10, 11,20],
                     [10,11,20],
                     [-1,00,-1]],

                     [[10,1,20],
                     [10,11,20],
                     [10,11,20],
                     [10,11,20],
                     [-1,00,-1]]],

                     [[[10,11,11,1,11,20],
                     [-1,00,00,00,00,-1]],

                     [[10,11,11,11,1,20],
                     [-1,00,00,00,00,-1]],

                     [[10,1,11,11,11,20],
                     [-1,00,00,00,00,-1]],

                     [[10,11,1,11,11,20],
                     [-1,00,00,00,00,-1]]],

                     [[[10,11,20],
                     [10,11,20],
                     [10, 1,20],
                     [10,11,20],
                     [-1,00,-1]],

                     [[10,11,20],
                     [10,11,20],
                     [10,11,20],
                     [10,1,20],
                     [-1,00,-1]],

                     [[10,11,20],
                     [10,1,20],
                     [10, 11,20],
                     [10,11,20],
                     [-1,00,-1]],

                     [[10,1,20],
                     [10,11,20],
                     [10,11,20],
                     [10,11,20],
                     [-1,00,-1]]]]
        self.shapeNumber=1
        self.shape_result=self.shape
    def rotation_testing(self,table):
        #print("shape actual",self.shape)
        xt,yt=self.xp,self.yp
        o=False
        finich=False
        self.shapeNumber_increment(1)
        STOP=0
        alt=0
        while ((not o and (alt<4)) and ((finich==False) and (STOP<10))):
            #print("coord centre xy",self.xp,self.yp)
            #print("           while",STOP)
            rotation_testing_shape=self.shapes_alternative[self.shapeNumber][alt]
            #print("rotation_testing_shape /_\\",rotation_testing_shape)
            o=[]
            STOP+=1
            coordsst=self.coordsIdShape(11,1,table=rotation_testing_shape)
            forme_plus_milieu=coordsst[11]+coordsst[1]
            problem=[]
            for i in forme_plus_milieu:
                try:

                    if table[i[1]][i[0]] or i[1]<=0 or i[0]<=0:
                        #print("table rotation_testing",table[i[1]][i[0]],"xy",repr(table[i[1]][i[0]]))
                        o.append(False)
                        problem.append(i)
                    else:
                        #print("table rotation_testing",table[i[1]][i[0]],"xy",repr(table[i[1]][i[0]]))
                        o.append(True)
                except IndexError:
                    o.append(False)
                    problem.append(i)
            #print("oo",o)
            if False in o:
                o=False
                #print("rotation_testing FALSE alt",alt)
                #print(self.shapes_alternative[self.shapeNumber][alt])
                alt+=1

            elif True in o:
                o=True
                self.shape_result=rotation_testing_shape
                #print("problem ??",coordsst)
        #print("'-'",self.shapeNumber)
        #print("nn",self.shapes_alternative[self.shapeNumber])
        self.shapeNumber_increment(-1)

        #print("FIN rotation_testing : ",alt,"\n\t\t       ",self.shape_result,"\n\t\t       ",self.coordsIdShape(11,1,table=self.shape_result))
        return o

    def rotation(self):

        #print("o  o o o o o o o o o o o o o o o o o o o o o o o o")
        self.shapeNumber_increment(1)
        self.shape=self.shape_result

    def shapeNumber_increment(self,num):
        #print(self.shape)
        #print("shapeNumber_1",self.shapeNumber)
        self.shapeNumber+=num
        if self.shapeNumber==len(self.shapes):
            self.shapeNumber=0
        if self.shapeNumber<0:
            self.shapeNumber=len(self.shapes)-1
        #print("shapeNumber_2",self.shapeNumber)

class Piece_S(Barre):
    def __init__(self,surface,id,name,color=COLOR_S,x=0,y=0,debug=0):
        super().__init__(surface,id,name,color,x,y,debug)

        self.shape= [[-1,10, 1,11,20],
                     [10,11,11,22,-1],
                     [-1,00,00,-1,-1],]
        self.shapes=[[[10,11,20,-1],
                      [10,11, 1,20],
                      [-1,12,11,20],
                      [-1,-1,00,-1],],

                     [[-1,10, 1,11,20],
                      [10,11,11,22,-1],
                      [-1,00,00,-1,-1],],

                     [[10,11,20,-1],
                      [10,11, 1,20],
                      [-1,12,11,20],
                      [-1,-1,00,-1],],

                     [[-1,10, 1,11,20],
                      [10,11,11,22,-1],
                      [-1,00,00,-1,-1],],]
        self.shapes_alternative=[[[[10,11,20,-1],
                      [10,11, 1,20],
                      [-1,12,11,20],
                      [-1,-1,00,-1],],

                     [[10,11,20,-1],
                      [10,1, 11,20],
                      [-1,12,11,20],
                      [-1,-1,00,-1],],

                     [[10,1,20,-1],
                      [10,11, 11,20],
                      [-1,12,11,20],
                      [-1,-1,00,-1],],

                     [[10,11,20,-1],
                      [10,11,11,20],
                      [-1,12, 1,20],
                      [-1,-1,00,-1],]],

                     [[[-1,10, 1,11,20],
                      [10,11,11,22,-1],
                      [-1,00,00,-1,-1]],

                     [[-1,10, 11, 1,20],
                      [10,11,11,22,-1],
                      [-1,00,00,-1,-1]],

                     [[-1,10, 11,11,20],
                      [10,11, 1,22,-1],
                      [-1,00,00,-1,-1]],

                     [[-1,10, 11,11,20],
                      [10, 1,11,22,-1],
                      [-1,00,00,-1,-1],]],

                     [[[10,11,20,-1],
                      [10,11, 1,20],
                      [-1,12,11,20],
                      [-1,-1,00,-1],],

                     [[10,11,20,-1],
                      [10,1, 11,20],
                      [-1,12,11,20],
                      [-1,-1,00,-1],],

                     [[10,1,20,-1],
                      [10,11, 11,20],
                      [-1,12,11,20],
                      [-1,-1,00,-1],],

                     [[10,11,20,-1],
                      [10,11,11,20],
                      [-1,12, 1,20],
                      [-1,-1,00,-1],]],

                     [[[-1,10, 1,11,20],
                      [10,11,11,22,-1],
                      [-1,00,00,-1,-1],],

                     [[-1,10, 11, 1,20],
                      [10,11,11,22,-1],
                      [-1,00,00,-1,-1],],

                     [[-1,10, 11,11,20],
                      [10,11, 1,22,-1],
                      [-1,00,00,-1,-1],],

                     [[-1,10, 11,11,20],
                      [10, 1,11,22,-1],
                      [-1,00,00,-1,-1],]],]
        self.shapeNumber=1
        self.shape_result=self.shape

    def direction_coords(self):
        coordss=self.coordsIdShape(10,20,00,22,12)
        gauches,droites,bas=coordss[10]+coordss[12],coordss[20]+coordss[22],coordss[00]+coordss[22]+coordss[12]
        return (gauches,droites,bas)

class Piece_Z(Piece_S):
    def __init__(self,surface,id,name,color=COLOR_Z,x=0,y=0,debug=0):
        super().__init__(surface,id,name,color,x,y,debug)

        self.shape= [[10,11, 1,20,-1],
                     [10,12,11,11,20],
                     [-1,-1,00,00,-1],]
        self.shapes=[[[-1,10,11,20],
                      [10,1, 11,20],
                      [10,11,22,-1],
                      [-1,00,-1,-1],],

                     [[10,11, 1,20,-1],
                     [10,12,11,11,20],
                     [-1,-1,00,00,-1],],

                     [[-1,10,11,20],
                      [10,1, 11,20],
                      [10,11,22,-1],
                      [-1,00,-1,-1],],

                     [[10,11, 1,20,-1],
                     [10,12,11,11,20],
                     [-1,-1,00,00,-1],]]
        self.shapes_alternative=[[[[-1,10,11,20],
                      [10,1, 11,20],
                      [10,11,22,-1],
                      [-1,00,-1,-1],],

                     [[-1,10,1,20],
                      [10,11,11,20],
                      [10,11,22,-1],
                      [-1,00,-1,-1],],

                     [[-1,10,11,20],
                      [10,11,1,20],
                      [10,11,22,-1],
                      [-1,00,-1,-1],],

                     [[-1,10,11,20],
                      [10,11,11,20],
                      [10,1,22,-1],
                      [-1,00,-1,-1],],],

                    [[[10,11, 1,20,-1],
                     [10,12,11,11,20],
                     [-1,-1,00,00,-1],],

                    [[10,1, 11,20,-1],
                     [10,12,11,11,20],
                     [-1,-1,00,00,-1],],

                    [[10,11, 11,20,-1],
                     [10,12,1,11,20],
                     [-1,-1,00,00,-1],],

                    [[10,11,11,20,-1],
                     [10,12,11, 1,20],
                     [-1,-1,00,00,-1]]],

                    [[[-1,10,11,20],
                      [10,1, 11,20],
                      [10,11,22,-1],
                      [-1,00,-1,-1],],

                     [[-1,10,1,20],
                      [10,11,11,20],
                      [10,11,22,-1],
                      [-1,00,-1,-1],],

                     [[-1,10,11,20],
                      [10,11,1,20],
                      [10,11,22,-1],
                      [-1,00,-1,-1],],

                     [[-1,10,11,20],
                      [10,11,11,20],
                      [10,1,22,-1],
                      [-1,00,-1,-1],],],

                    [[[10,11, 1,20,-1],
                     [10,12,11,11,20],
                     [-1,-1,00,00,-1],],

                    [[10,1, 11,20,-1],
                     [10,12,11,11,20],
                     [-1,-1,00,00,-1],],

                    [[10,11, 11,20,-1],
                     [10,12,1,11,20],
                     [-1,-1,00,00,-1],],

                    [[10,11, 11,20,-1],
                     [10,12,11,1,20],
                     [-1,-1,00,00,-1],],]]
        self.shapeNumber=1
        self.shape_result=self.shape



class Piece_L(Piece_Z):
    def __init__(self,surface,id,name,color=COLOR_L,x=0,y=0,debug=0):
        super().__init__(surface,id,name,color,x,y,debug)

        self.shape= [[10,11,20,-1],
                     [10, 1,20,-1],
                     [10,11,11,20],
                     [-1,00,00,-1],]
        self.shapes=[[[-1,-1,10,11,20],
                      [10,11, 1,11,20],
                      [-1,00,00,00,-1]],

                     [[10,11,20,-1],
                     [10, 1,20,-1],
                     [10,11,11,20],
                     [-1,00,00,-1],],

                     [[10,11, 1,11,20],
                      [10,11,22,00,-1],
                      [-1,00,-1,-1,-1]],

                     [[10,11,11,20],
                     [-1,12, 1,20],
                     [-1,10,11,20],
                     [-1,-1,00,-1],],]
        self.shapes_alternative=[[[[-1,-1,10,11,20],
                      [10, 1,11,11,20],
                      [-1,00,00,00,-1]],

                     [[-1,-1,10,11,20],
                      [10,11, 1,11,20],
                      [-1,00,00,00,-1]],

                    [[-1,-1,10,11,20],
                      [10,11,11, 1,20],
                      [-1,00,00,00,-1]],

                     [[-1,-1,10, 1,20],
                      [10,11,11,11,20],
                      [-1,00,00,00,-1]],],

                    [[[10, 1,20,-1],
                     [10,11,20,-1],
                     [10,11,11,20],
                     [-1,00,00,-1],],

                    [[10,11,20,-1],
                     [10, 1,20,-1],
                     [10,11,11,20],
                     [-1,00,00,-1],],

                    [[10,11,20,-1],
                     [10,11,20,-1],
                     [10, 1,11,20],
                     [-1,00,00,-1],],

                    [[10,11,20,-1],
                     [10,11,20,-1],
                     [10,11, 1,20],
                     [-1,00,00,-1],],],

                    [[[10,11,11, 1,20],
                      [10,11,22,00,-1],
                      [-1,00,-1,-1,-1]],

                     [[10,11, 1,11,20],
                      [10,11,22,00,-1],
                      [-1,00,-1,-1,-1]],

                     [[10, 1,11,11,20],
                      [10,11,22,00,-1],
                      [-1,00,-1,-1,-1]],

                     [[10,11,11,11,20],
                      [10, 1,22,00,-1],
                      [-1,00,-1,-1,-1]],],

                    [[[10,11,11,20],
                     [-1,12,11,20],
                     [-1,10, 1,20],
                     [-1,-1,00,-1],],

                    [[10,11,11,20],
                     [-1,12, 1,20],
                     [-1,10,11,20],
                     [-1,-1,00,-1],],

                    [[10,11, 1,20],
                     [-1,12,11,20],
                     [-1,10,11,20],
                     [-1,-1,00,-1],],

                    [[10, 1,11,20],
                     [-1,12,11,20],
                     [-1,10,11,20],
                     [-1,-1,00,-1],],]]
        self.shapeNumber=1
        self.shape_result=self.shape


class Piece_J(Piece_Z):
    def __init__(self,surface,id,name,color=COLOR_L,x=0,y=0,debug=0):
        super().__init__(surface,id,name,color,x,y,debug)

        self.shape= [[-1,10,11,20],
                     [-1,10, 1,20],
                     [10,11,11,20],
                     [-1,00,00,-1],]
        self.shapes=[[[10,11,11,20],
                      [10, 1,22,-1],
                      [10,11,20,-1],
                      [-1,00,-1,-1],],

                     [[10,11, 1,11,20],
                      [-1,00,12,11,20],
                      [-1,-1,-1,00,-1],],

                     [[-1,10,11,20],
                      [-1,10, 1,20],
                      [10,11,11,20],
                      [-1,00,00,-1],],

                     [[10,11,20,-1,-1],
                      [10,11, 1,11,20],
                      [-1,00,00,00,-1],],]
        self.shapes_alternative=[[[[10,11,11,20],
                      [10,11,22,-1],
                      [10, 1,20,-1],
                      [-1,00,-1,-1],],

                     [[10,11,11,20],
                      [10, 1,22,-1],
                      [10,11,20,-1],
                      [-1,00,-1,-1],],

                     [[10, 1,11,20],
                      [10,11,22,-1],
                      [10,11,20,-1],
                      [-1,00,-1,-1],],

                     [[10,11, 1,20],
                      [10,11,22,-1],
                      [10,11,20,-1],
                      [-1,00,-1,-1],],],

                    [[[10, 1,11,11,20],
                      [-1,00,12,11,20],
                      [-1,-1,-1,00,-1],],

                    [[10,11, 1,11,20],
                      [-1,00,12,11,20],
                      [-1,-1,-1,00,-1],],

                    [[10,11,11, 1,20],
                      [-1,00,12,11,20],
                      [-1,-1,-1,00,-1],],

                    [[10,11,11,11,20],
                      [-1,00,12, 1,20],
                      [-1,-1,-1,00,-1],],],

                    [[[-1,10, 1,20],
                      [-1,10,11,20],
                      [10,11,11,20],
                      [-1,00,00,-1],],

                     [[-1,10,11,20],
                      [-1,10, 1,20],
                      [10,11,11,20],
                      [-1,00,00,-1],],

                     [[-1,10,11,20],
                      [-1,10,11,20],
                      [10,11, 1,20],
                      [-1,00,00,-1],],

                     [[-1,10,11,20],
                      [-1,10,11,20],
                      [10, 1,11,20],
                      [-1,00,00,-1],],],

                    [[[10,11,20,-1,-1],
                      [10,11,11, 1,20],
                      [-1,00,00,00,-1],],

                    [[10,11,20,-1,-1],
                      [10,11, 1,11,20],
                      [-1,00,00,00,-1],],

                    [[10,11,20,-1,-1],
                      [10, 1,11,11,20],
                      [-1,00,00,00,-1],],

                    [[10, 1,20,-1,-1],
                      [10,11,11,11,20],
                      [-1,00,00,00,-1],],]]
        self.shapeNumber=1
        self.shape_result=self.shape

class Piece_T(Piece_Z):
    def __init__(self,surface,id,name,color=COLOR_L,x=0,y=0,debug=0):
        super().__init__(surface,id,name,color,x,y,debug)

        self.shape= [[10,11,20,-1],
                     [10, 1,11,20],
                     [10,11,22,-1],
                     [-1,00,-1,-1],]
        self.shapes=[[[-1,10,11,20,-1],
                      [10,11, 1,11,20],
                      [-1,00,00,00,-1],],

                     [[10,11,20,-1],
                     [10, 1,11,20],
                     [10,11,22,-1],
                     [-1,00,-1,-1],],

                     [[10,11, 1,11,20],
                      [-1,12,11,22,-1],
                      [-1,-1,00,-1,-1],],

                     [[-1,10,11,20],
                      [10,11, 1,20],
                      [-1,12,11,20],
                      [-1,-1,00-1],],]
        self.shapes_alternative=[[[[-1,10,11,20,-1],
                      [10,11, 1,11,20],
                      [-1,00,00,00,-1],],

                     [[-1,10, 1,20,-1],
                      [10,11,11,11,20],
                      [-1,00,00,00,-1],],

                     [[-1,10,11,20,-1],
                      [10,11,11, 1,20],
                      [-1,00,00,00,-1],],

                     [[-1,10,11,20,-1],
                      [10, 1,11,11,20],
                      [-1,00,00,00,-1],],],

                    [[[10,11,20,-1],
                     [10, 1,11,20],
                     [10,11,22,-1],
                     [-1,00,-1,-1],],

                    [[10,11,20,-1],
                     [10,11, 1,20],
                     [10,11,22,-1],
                     [-1,00,-1,-1],],

                    [[10, 1,20,-1],
                     [10,11,11,20],
                     [10,11,22,-1],
                     [-1,00,-1,-1],],

                    [[10,11,20,-1],
                     [10,11,11,20],
                     [10, 1,22,-1],
                     [-1,00,-1,-1],],],

                    [[[10,11, 1,11,20],
                      [-1,12,11,22,-1],
                      [-1,-1,00,-1,-1],],

                     [[10,11,11, 1,20],
                      [-1,12,11,22,-1],
                      [-1,-1,00,-1,-1],],

                     [[10, 1,11,11,20],
                      [-1,12,11,22,-1],
                      [-1,-1,00,-1,-1],],

                    [[10,11,11,11,20],
                      [-1,12, 1,22,-1],
                      [-1,-1,00,-1,-1],],],

                    [[[-1,10,11,20],
                      [10,11, 1,20],
                      [-1,12,11,20],
                      [-1,-1,00-1],],

                    [[-1,10,11,20],
                      [10,1,11,20],
                      [-1,12,11,20],
                      [-1,-1,00-1],],

                    [[-1,10, 1,20],
                      [10,11,11,20],
                      [-1,12,11,20],
                      [-1,-1,00-1],],

                    [[-1,10,11,20],
                      [10,11,11,20],
                      [-1,12, 1,20],
                      [-1,-1,00-1],],]]
        self.shapeNumber=1
        self.shape_result=self.shape

if __name__=="__main__":
    x=8
    y=16
    xp=x*32
    yp=y*32
    pygame.init()
    fenetre = pygame.display.set_mode((xp+32*2, yp+32*2))
    continuer = 1
    red=(255,0,0)
    c1=Barre(fenetre,1,"test",color=red,x=0,y=0)
    c1.draw()
    pygame.display.flip()
    #Boucle infinie
    piece=Carre(fenetre,8,"piece",color=(0,255,0),x=4,y=1)
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
            #print("move", piece.get_coordp())
        else:
            pxpyp=piece.get_coordp()
            cuvette[pxpyp[0]][pxpyp[1]]=piece
            piece=Piece(fenetre,8,"piece",color=(0,255,0),x=3,y=2)
            piece.draw()
        pygame.display.flip()
    pygame.quit()
