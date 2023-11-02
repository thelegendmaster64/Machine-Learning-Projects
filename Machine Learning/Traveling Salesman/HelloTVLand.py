import random
import math

Sold = "qwPdaw dLSkfe"

temp = 100.0
time = 0.01

def perturb(S):
    #Getting the random character from the old solution
    index = random.randint(0, len(S)-1)

    #Generating a new character
    newChar = chr(random.randint(0, 127)) #not only the alphabet characters - ASCII table characters
    
    #Inserting the new char where the old one was thus replacing it
    Snew = S[:index] + newChar + S[index + 1:]
    
    return Snew

def calcScore(S):
    score = 0
    
    for i in range(len(S)):
        #calculating the score based on how far the new string is away from the target string
        score += abs(ord(S[i]) - ord("Hello TV Land"[i]))
        
    return score

def main(Sold, temp, time):
    oldScore = 0
    newScore = 0
    i = 0

    while 1:
        Snew = perturb(Sold)
        
        oldScore = calcScore(Sold)
        newScore = calcScore(Snew)
        
        if newScore < oldScore:
            Sold = Snew
            print(f"Solution: {Sold}, nEpoch {i+1}, temperature: {temp}")
        else:
            dE = newScore - oldScore
            
            #negative sign should be in the formula instead but this makes it look nicer
            k = -10 #contant that can be anything else
            #the formula
            pofAcc = math.exp((k*dE)/temp)
            
            nRand = random.randint(0, 100)
            
            if nRand < pofAcc:
                Sold = Snew
                print(f"Solution: {Sold}, nEpoch {i+1}, temperature: {temp}")
                
        temp = temp - temp*time

        if Sold == "Hello TV Land":
            print(f"Solution found after {i+1} epochs: {Sold}")
            break
        i += 1
        #print(f"Solution: {Sold}, nEpoch {i+1}, temperature: {temp}")
    
    print("Final solution: ", Sold)
    
main(Sold, temp, time)