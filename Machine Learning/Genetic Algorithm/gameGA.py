import string
import random

pop = []
popSize = len(pop)
#each memeber of population is 13 character string
percent2keep = 0.2

class popMember:
    def __init__(self, string, score=0, bulletHits=0, bombsKilled=0):
        self.string = string
        self.score = score
        self.bulletHits = bulletHits
        self.bombsKilled = bombsKilled
        #self.damage = damage
    def fitness(self):
        self.score = self.bulletHits + self.bombsKilled # - self.damage
    
def breed(mom, dad):
    #crossover
    crossPoint = random.randint(0,12)
    
    return mom[:crossPoint] + dad[crossPoint:]

def mutate(kid, prob):
    for i in range(len(kid)):
        #mutate the character at random
        if random.random() < prob:
            kid = kid[:i] + random.choice("udlrs") + kid[i+1:]
    return kid
    
nGnrts = 10
for j in range(nGnrts):
    if j == 0:
        for i in range (10):
            #up down left right shoot
            pop.append(popMember(''.join(random.choices("udlrs", k=200))))
        popSize = len(pop)
        #create random population
        
    #fitness test
    for k in range(popSize):
        pop[k].fitness()

    #rank the population from best to worst - lowest to highest score
    pop.sort(key=lambda x: x.score) #this sorts by the .score attribute from the class
    
    #breed new population members
    d = int(percent2keep * popSize) #kepping 20% of the population and replacing the rest
    
    newPop = [] #making the new population
    for k in range(d):
        newPop.append(pop[k])
        
    #Elite selection of parents
    for k in range(d, popSize):
        mom = random.randint(0, d-1)
        dad = random.randint(0, d-1)
        
        kid = breed(pop[mom].string, pop[dad].string)
        kid = mutate(kid, 0.1)
        newPop.append(popMember(kid))
        
    pop = newPop
    print(pop[0].string)
    nGnrts += 1
    
    