# Créé par mchedor, le 25/04/2022 en Python 3.7
import pygame
from pygame.locals import *
from random import *
import tetris_piece as tp
import time

combo=0
point=0
x=10
y=22
xp=x*32+32
yp=y*32+32
HAUT_DE_CUVETTE=2
pygame.init()
fenetre = pygame.display.set_mode((xp+32*2, yp+32*2))
continuer = 1
COLOR_CUVETTE=(127, 127, 127)
pieces=("""tp.Barre(fenetre,8,"piece",x=4,y=1)""","""tp.Carre(fenetre,8,"piece",x=4,y=1)""","""tp.Piece_S(fenetre,8,"piece",x=4,y=1)""","""tp.Piece_Z(fenetre,8,"piece",x=4,y=1)""","""tp.Piece_L(fenetre,8,"piece",x=4,y=1)""","""tp.Piece_J(fenetre,8,"piece",x=4,y=1)""","""tp.Piece_T(fenetre,8,"piece",x=4,y=1)""")

#pieces=("""tp.Piece_L(fenetre,8,"piece",x=4,y=1)""","""tp.Piece_L(fenetre,8,"piece",x=4,y=1)""")
police = pygame.font.SysFont("monospace" ,30)

cuvette=[[0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1]]
cuvette_obj_piece=[]
for i in range(len(cuvette)):
    cuvette_obj_piece.append([])
    for j in range(len(cuvette[i])):
        if cuvette[i][j]:
            #print("i,j:",i,j,end='__')
            cuvette_obj_piece[i].append(tp.Pixel(fenetre,1,"cuvette",color=COLOR_CUVETTE,x=j,y=i))
            cuvette_obj_piece[i][j].draw()
            #print("x,y",cuvette_obj_piece[i][j].get_coordp())
        else:
            cuvette_obj_piece[i].append(0)


def affiche_points():
    image_texte = police.render ( "Points : "+str(point), 1 , (255,0,0) )
    fenetre.blit(image_texte, (xp-150,40))
def choicePiece():
    global piece
    seed()
    piece=eval(pieces[randint(0,len(pieces))-1])

    """
    pieces2=tuple(pieces)
    global piece
    piece=pieces2[randint(0,len(pieces))-1]
    """
    return piece

piece=choicePiece()
piece.draw()
affiche_points()
pygame.display.flip()
montps=time.time()
ev=[]

ligne=False
touche_enfoncer={"s":False,"q":False,"d":False}
mouvement=""
fin=False
#Boucle infinie
while continuer and fin==False:
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
            if event.key == pygame.K_UP:
                mouvement+="o"
            if event.key == pygame.K_SPACE:
                #print("SPACE   SPACE   SPACE   SPACE   SPACE  ")
                pass
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
        #print("      MOUVEMENT",mouvement)
        try:
            posibilite_move=piece.movetesting(cuvette_obj_piece)
        except IndexError:
            #print("ERROR : ")
            posibilite_move={"s":False,"q":False,"d":False,"o":piece.rotation_testing(cuvette_obj_piece)}
        #print("mouv ",mouvement)
        #print("poss ",posibilite_move)
        for i in mouvement:

            if posibilite_move[i]:
                piece.move(i)
                try:
                    posibilite_move=piece.movetesting(cuvette_obj_piece)
                except IndexError:
                    #print("ERROR : ")
                    posibilite_move={"s":False,"q":False,"d":False,"o":piece.rotation_testing(cuvette_obj_piece)}
            #print("poss ",posibilite_move)


        pygame.display.flip()
        mouvement=""

    if time.time()-montps>=0.7:
        #on defini un tic
        combo-=1
        montps=time.time()
        if piece.movetesting(cuvette_obj_piece)["s"]:
            mouvement+="s"
        else:
            #print("I died my piece",piece.xp,piece.yp)
            piece.move("s")
            coords=piece.coordsIdShape(1,11)
            coord=[j for i in coords for j in coords[i]]
            for i in range(len(coord)):
                if coord[i]:
                    x,y=coord[i]
                cuvette_obj_piece[y-1][x]=tp.Pixel(fenetre,2,"piecemorte",color=piece.color,x=x,y=y-1)
                cuvette_obj_piece[y-1][x].draw(r=True)
            piece=choicePiece()
            #piece.draw(color=(0,0,0))
            #piece.set_coordp(4,1)
        #print("\n",ev)
        ev=[]
        for i in cuvette_obj_piece:
            #on draw la cuvette a chaque tique
            for j in i:
                if j:
                    j.draw()
        affiche_points()

        pygame.display.flip()


        for i in range(len(cuvette_obj_piece)-1):
            if not 0 in cuvette_obj_piece[i]:
                ligne=i
                #print(cuvette_obj_piece[i])
        if ligne:
            if combo<0:
                combo=0
            for i in cuvette_obj_piece[ligne]:
                if int(i)==2:
                    i.destroy()
                    point+=1*(combo+1)
                else:
                    #print(int(i))
                    pass
                pygame.display.flip()
                time.sleep(0.04 )
            cuvette_obj_piece.insert(HAUT_DE_CUVETTE,[cuvette_obj_piece[ligne][0]]+[i*0 for i in range(len(cuvette_obj_piece[ligne])-2)]+[cuvette_obj_piece[ligne][-1]])
            cuvette_obj_piecepop=cuvette_obj_piece.pop(ligne+1)
            #print(cuvette_obj_piece.pop)

            #print(cuvette_obj_piece)
            #print()
            #print("c",cuvette_obj_piece[ligne])
            ligne=False
            xh,yh=fenetre.get_size()
            pygame.draw.rect(fenetre, (0,0,0), pygame.Rect(0, 0, xh, yh))#font d'ecran
            for i in range(len(cuvette_obj_piece)):
            #on draw la cuvette a chaque tique
                for j in range(len(cuvette_obj_piece[i])):
                    if cuvette_obj_piece[i][j]:
                        #print("hhh",int(cuvette_obj_piece[i][j]))
                        cuvette_obj_piece[i][j].set_coordp(j,i)
                        cuvette_obj_piece[i][j].draw()
            pygame.display.flip()
            combo+=1
            #print("l",len(cuvette_obj_piece))
    if [True for i,x in enumerate(cuvette_obj_piece[1]) if x]:
        fin=True
    seed()
    time.sleep(0.1)

print("\n".join([str(i) for i in cuvette_obj_piece]))
pygame.quit()
