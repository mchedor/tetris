# Créé par mchedor, le 25/04/2022 en Python 3.7
import pygame
from pygame.locals import *
import tetris_piece as tp
import time


x=8
y=16
xp=x*32+32
yp=y*32+32
pygame.init()
fenetre = pygame.display.set_mode((xp+32*2, yp+32*2))
continuer = 1
red=(255,0,0)


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
cuvette_obj_piece=[]
for i in range(len(cuvette)):
    cuvette_obj_piece.append([])
    for j in range(len(cuvette[i])):
        if cuvette[i][j]:
            print("i,j:",i,j,end='__')
            cuvette_obj_piece[i].append(tp.Pixel(fenetre,1,"cuvette",color=red,x=j,y=i))
            cuvette_obj_piece[i][j].draw()
            print("x,y",cuvette_obj_piece[i][j].get_coordp())
        else:
            cuvette_obj_piece[i].append(0)


piece=tp.Piece(fenetre,8,"piece",color=(0,255,0),x=4,y=1)
piece.draw()

pygame.display.flip()
montps=time.time()
ev=[]

touche_enfoncer={"s":False,"q":False,"d":False}
mouvement=""
#Boucle infinie
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0
        #print(event)
        elif event.type == pygame.KEYDOWN:  #une touche a été pressée...laquelle ?
            if event.key == pygame.K_DOWN:
                touche_enfoncer["s"]=True
            if event.key == pygame.K_LEFT:
                touche_enfoncer["q"]=True
            if event.key == pygame.K_RIGHT:
                touche_enfoncer["d"]=True
        elif event.type == pygame.KEYUP:  #une touche a été pressée...laquelle ?
            if event.key == pygame.K_DOWN:
                touche_enfoncer["s"]=False
            if event.key == pygame.K_LEFT:
                touche_enfoncer["q"]=False
            if event.key == pygame.K_RIGHT:
                touche_enfoncer["d"]=False
        if event:
            ev.append(event)

    if touche_enfoncer:
        if touche_enfoncer["s"]:
            mouvement+="s"
        if touche_enfoncer["q"]:
            mouvement+="q"
        if touche_enfoncer["d"]:
           mouvement+="d"


    if mouvement:
        posibilite_move=piece.movetesting(cuvette_obj_piece)
        mouvement2=""
        for i in mouvement:
            if posibilite_move[i]:
                mouvement2+=i

        if mouvement2:
            piece.move(mouvement2)
            pygame.display.flip()
            mouvement=""

    if time.time()-montps>=0.7:
        #on defini un tic
        montps=time.time()
        if piece.movetesting(cuvette_obj_piece)["s"]:
            mouvement+="s"
        else:
            cuvette_obj_piece[piece.yp][piece.xp]=tp.Pixel(fenetre,2,"piecemorte",color=piece.color,x=piece.xp,y=piece.yp)
            cuvette_obj_piece[piece.yp][piece.xp].draw()
            piece.set_coordp(4,1)
        print("\n",ev)
        ev=[]
        for i in cuvette_obj_piece:
            #on draw la cuvette a chaque tique
            for j in i:
                if j:
                    j.draw()
        pygame.display.flip()


    time.sleep(0.1)


pygame.quit()