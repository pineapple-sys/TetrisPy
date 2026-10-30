import numpy as np ,sys
sys.path.append('../Conway_Game/src')
from src.config import *

tetromino = {
    0:((0,0),(1,0),(-1,0),(-2,0),(0,255,255)),
    1:((0,0),(-1,0),(0,1),(-1,1),(255,255,0)),
    2:((0,0),(1,0),(-1,0),(0,1),(255,0,255)),
    3:((0,0),(-1,0),(1,0),(-1,1),(255, 165, 0)),
    4:((0,0),(1,0),(-1,0),(1,1),(0, 0, 255)),
    5:((0,0),(-1,0),(0,1),(1,1),(255, 0, 0)),
    6:((0,0),(1,0),(-1,1),(0,1),(0, 255, 0))

}

def nparg(fix):
    return np.argwhere(fix==1)
def npall(fix,n):
    return np.all(fix ==n)
def clear(fix):
    car = np.zeros((HEIGHT//RECT_SIZE,WIDTH//RECT_SIZE),dtype="int64")
    for obj in fix:
        for i in obj[:-1]:
            if i[0]<=len(car)-1:
                car[i[0],i[1]]=1
    
    for i in range(len(car)):
        if np.all(car[i]==1):
            for j in range(len(car[i])):
                car[i, j] = 0
                for obj in fix[:]:
                    if [i, j] in obj:
                        obj.remove([i,j])
    
    z = []
    for obj in fix:
        for i in obj[:-1]:
            z.append(i)
    
    for i in range(len(fix)):
        for j in range(len(fix[i])-1):
            y = fix[i][j][0]+1
            x = fix[i][j][1]
            for b in range(len(fix[i])-1):
                print([fix[i][b][0]+1,fix[i][b][1]])
            if any([fix[i][b][0]+1,fix[i][b][1]] in z for b in range(len(fix[i])-1)):
                while [y,x] not in z and y<= len(car)-1:
                    for b in range(len(fix[i])-1):
                        fix[i][b][0]+=1
                    y +=1
    
    """
    if not np.all(car==0) and np.all(car[-1]==0):
        while np.all(car[-1]==0):
            ones = np.argwhere(car==1)
            new = [[i[0]+1,i[1]] for i in ones]
            car = np.zeros((HEIGHT//RECT_SIZE,WIDTH//RECT_SIZE),dtype="int64")
            for i in new:
                car[i[0],i[1]] = 1

            for i in range(len(fix)):
                for j in range(len(fix[i])-1):
                    fix[i][j][0]+=1

    
    """
    return fix


def start(n):
    if n!= None:

        
        y =0
        x = WIDTH//(RECT_SIZE*2)
        actif = []
        for i in tetromino[n][:-1]:
            actif.append([y+i[1],x+i[0]]) 
        actif.append(tetromino[n][-1])
        
        
        return actif
    else:
        fix = np.zeros((HEIGHT//RECT_SIZE,WIDTH//RECT_SIZE),dtype="int64")
        return fix

    
