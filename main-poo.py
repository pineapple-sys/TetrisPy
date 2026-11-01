import pygame as py
import sys
from src.config import *
import random

class Bloc: #Représente un carré a l'ecran
    def __init__(self, x:int,y:int,color: tuple,size: int):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
    
    def draw(self, screen):
        py.draw.rect(screen,self.color,(self.x,self.y,self.size,self.size))
        py.draw.rect(screen,BACKGROUND_COLOR,(self.x,self.y,self.size+1,self.size+1),4)

class Piece: #Représente un tetromino
    def __init__(self,type:int):
        self.color = tetromino[type][-1]
        self.coord = tetromino[type][:-1]
        self.type = type

        self.blocs = []
        for c in self.coord:
            new_bloc = Bloc(x=POS[0]+c[0]*RECT_SIZE, y=POS[1] + c[1]*RECT_SIZE, color=self.color, size=RECT_SIZE)
            self.blocs.append(new_bloc)
    def deplacer(self, event, grille):
        x,y = 0,0
        if event.key == py.K_LEFT:
            x = -1
        elif event.key == py.K_RIGHT:
            x = 1
        elif event.key == py.K_DOWN:
            y = 1
        else:
            return
        
        liste = [[i.x,i.y] for i in grille.bloc_fixes]
        if all(0<=b.x+x*RECT_SIZE<=WIDTH-RECT_SIZE and [b.x+x*RECT_SIZE, b.y+y*RECT_SIZE] not in liste for b in self.blocs ):
            for b in self.blocs:
                b.x += x*RECT_SIZE
                b.y += y*RECT_SIZE
        
    def descendre(self):
        for b in self.blocs:
            b.y += RECT_SIZE
    def draw(self, screen):
        for b in self.blocs:
            b.draw(screen)
    def colision(self,grille):
        if grille.bloc_fixes:
            pos_grille = [[i.x,i.y] for i in grille.bloc_fixes]
            if any([b.x,b.y+RECT_SIZE] in pos_grille for b in self.blocs):
                for a in self.blocs:
                    grille.bloc_fixes.append(a)
                return Piece(random.randint(1,1))
        if any(b.y+RECT_SIZE>=HEIGHT for b in self.blocs):
            for a in self.blocs:
                grille.bloc_fixes.append(a)
            return Piece(random.randint(1,1))

        return self
    def rotation(self,grille):
        if self.type !=1:
            can_rotate = True
            pivot_x = self.blocs[0].x
            pivot_y = self.blocs[0].y

            liste = [[i.x,i.y] for i in grille.bloc_fixes]
            for i in self.blocs:
                f_x, f_y = i.x - pivot_x, i.y - pivot_y

                oldx = f_x
                oldy = f_y
                f_x = -oldy
                f_y = oldx

                f_x += pivot_x
                f_y += pivot_y
                if [f_x, f_y] in liste or not 0<=f_x<=WIDTH-RECT_SIZE:
                    can_rotate = False
                    break
            if can_rotate:
                for i in self.blocs:
                    f_x, f_y = i.x - pivot_x, i.y - pivot_y

                    oldx = f_x
                    oldy = f_y
                    f_x = -oldy
                    f_y = oldx

                    f_x += pivot_x
                    f_y += pivot_y
                    
                    i.x = f_x
                    i.y = f_y
 

class Grid:#Tous les blocs fixe du jeu
    def __init__(self):
        self.bloc_fixes = []
    
    def draw(self, screen):
        for b in self.bloc_fixes:
            b.draw(screen)
    def clear(self):
        lignes_vides = []
        for i in range(0,HEIGHT,RECT_SIZE):
            count = 0
            for b in self.bloc_fixes:
                if b.y == i:
                    count+=1
            if count==10:
                lignes_vides.append(i)
                for b in self.bloc_fixes[:]:
                    if b.y ==i:
                        self.bloc_fixes.remove(b)
                        
        for i in lignes_vides:
            for b in self.bloc_fixes:
                if b.y < i:
                    b.y += RECT_SIZE

                    

def main():
    py.init()
    screen = py.display.set_mode((WIDTH,HEIGHT))
    running = True
    clock, timer = py.time.Clock(), 0

    actif = Piece(random.randint(1,1))
    grille = Grid()
    while running:
       
        dt = clock.tick(FPS)/1000
        timer += dt
        for event in py.event.get():
            if event.type==py.QUIT:
                running = False
            if event.type ==py.KEYDOWN:
                actif.deplacer(event, grille)

                if event.key == py.K_UP:
                    actif.rotation(grille)
        actif  = actif.colision(grille)

        if timer >= COOLDOWN:
            timer = 0
            actif.descendre()
        grille.clear()
        screen.fill(BACKGROUND_COLOR)
        grille.draw(screen)
        actif.draw(screen)
        py.display.flip()
    py.quit()
    sys.exit()

if __name__== "__main__":
    main()