import math
import random

towns = [['b', 10, 0],
         ['c', 10, -10],
         ['d', 0, -10],
         ['e', -10, -10],
         ['f', -10, 0],
         ['g', -10, 10],
         ['h', 0, 10],
         ['i', 10, 10]]

start = ['a',0,0]

goalDist = 94.14213562373095
Sold = ['g', 'i', 'f', 'd', 'b', 'e', 'c', 'h'] #random solution

temp = 100.0
time = 0.01

def getX(S):
    x = 0
    for i in range(len(towns)):
        #all coordinates except the start are stored in towns
        if S == towns[i][0]:
            #return the X coodinate 
            x += int(towns[i][1])
            break
    return x
        
def getY(S):
    y = 0
    for i in range(len(towns)):
        #all coordinates except the start are stored in towns
        if S == towns[i][0]:
            #return the Y coodinate 
            y += int(towns[i][2])
            break
    return y

def distance(S):
    dist = 0
    
    for i in range(-1, len(S)):
        if i < 0:
            x = getX(S[0])
            y = getY(S[0])
            #formula for distance between first town and start town (a)
            dist += math.sqrt( (x - start[1])**2 + (y - start[2])**2 )
        elif i == len(S) - 1:
            #formula for distance between last town and start town (a)
            dist += math.sqrt( (getX(S[i]) - start[1])**2 + (getY(S[i]) - start[2])**2 )
        else:
            dist += math.sqrt( (getX(S[i]) - getX(S[i+1]))**2 + (getY(S[i]) - getY(S[i+1]))**2 )
    
    return dist

def perturb(S):
    #0 for b, 7 for i
    n = random.randint(0, 7)
    ch = chr(n + 98) #98 is 'a'
    Snew = S.copy()
    
    #swaping places of the 2 towns that will result in improved distance
    temp = Snew[n]
    Snew[n] = ch
    Snew[Snew.index(ch)] = temp
    
    return Snew

i = 0
#same algorithm as for HelloTVLand
while 1:
    Snew = perturb(Sold)
    
    oldDist = distance(Sold)
    newDist = distance(Snew)
    
    if newDist < oldDist:
        Sold = Snew
        print(f"Current solution: {Sold} epochs: {i+1} dist: {newDist}")
    else:
        dE = newDist - oldDist
        
        k = -1
        pofAcc = math.exp((k*dE)/temp)
        
        nRand = random.randint(0, 100)
            
        if nRand < pofAcc:
            Sold = Snew
            print(f"Current solution: {Sold} epochs: {i+1} dist: {newDist}")
                
    temp = temp - temp*time

    if newDist == goalDist:
        print(f"Solution found after {i+1} epochs: {Sold}")
        break
    i += 1
    
print("Final solution: ", Sold)