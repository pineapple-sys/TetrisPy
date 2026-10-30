import pygame as py, sys, random
from src import game
from src.config import *


def mouv(event, actif, fix):
    if event.type == py.KEYDOWN:
        x, y = 0,0
        if event.key == py.K_LEFT:
            x = -1
        elif event.key == py.K_RIGHT:
            x = 1
        elif event.key == py.K_DOWN:
            y = 1
        else:
            return actif

        z = []
        for obj in fix:
            for i in obj[:-1]:
                z.append(i)
       
        if not(any([actif[i][0]+y,actif[i][1]+x] in z or 0>(actif[i][1]+x)*RECT_SIZE or WIDTH < ((actif[i][1]+x+1)*RECT_SIZE) for i in range(len(actif)-1))):
            #test si au moins un bloc est en colision avec un de z ou si les bordures ne pas respectées
            for i in range(len(actif)-1):
                actif[i][1] += x
                actif[i][0] += y
            
        
        return actif
    return actif


def defilement(actif, timer):
    if timer >= COOLDOWN:
        timer = 0
        for i in range(len(actif)-1):
            actif[i][0] += 1
    return timer 

def stop(fix, actif):
    if not fix:
        if any((i[0]+1)*RECT_SIZE==HEIGHT for i in actif):
            liste = []
            for i in actif:
                liste.append(i)
            fix.append(liste)
            
            actif = []
    else:
        z = []
        for obj in fix:
            for i in obj[:-1]:
                z.append(i)
        
        
        if any([i[0]+1,i[1]] in z for i in actif):
            liste = []
            for i in actif:
                liste.append(i)
            fix.append(liste)
            
            actif = []
        else:
            if any((i[0]+1)*RECT_SIZE==HEIGHT for i in actif):
                liste = []
                for i in actif:
                    liste.append(i)
                fix.append(liste)
                
                actif = []

    return actif
        
def showf(screen, fix):
    
    for obj in fix:
        for sq in obj[:-1]:
            py.draw.rect(screen, obj[-1],(sq[1]*RECT_SIZE,sq[0]*RECT_SIZE,RECT_SIZE,RECT_SIZE))
            py.draw.rect(screen, BACKGROUND_COLOR,(sq[1]*RECT_SIZE,sq[0]*RECT_SIZE,RECT_SIZE+1,RECT_SIZE+1), 4)

def show(screen,bloc):
    for i in bloc[:-1]:
        py.draw.rect(screen, bloc[-1],(i[1]*RECT_SIZE,i[0]*RECT_SIZE,RECT_SIZE,RECT_SIZE))
        py.draw.rect(screen, BACKGROUND_COLOR,(i[1]*RECT_SIZE,i[0]*RECT_SIZE,RECT_SIZE+1,RECT_SIZE+1), 4)
def main():
    screen = py.display.set_mode((WIDTH,HEIGHT))
    running = True
    actif = []
    fix = []
    clock = py.time.Clock()
    timer = 0
    while running:
        dt = clock.tick(60)/1000
        timer += dt
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
       
            actif = mouv(event,actif, fix)
        
        actif = stop(fix, actif)
        if not actif:
            actif = game.start(random.randint(0,6))
        timer = defilement(actif, timer)
        fix = game.clear(fix)
        
        screen.fill(BACKGROUND_COLOR)
        show(screen,actif)
        showf(screen, fix)
        py.display.flip()

if __name__ == "__main__":
    main()