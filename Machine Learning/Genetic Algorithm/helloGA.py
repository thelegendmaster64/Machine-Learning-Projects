import string
import random

nGnrts = 0
pop = []
popSize = len(pop)
#each memeber of population is 13 character string
percent2keep = 0.2

#this is our population member
class popMember:
    #score is automatically declared at 1000 (bad)
    def __init__(self, string, score=1000):
        self.string = string
        self.score = score

def fitness(member):
    score = 0
    
    for i in range(len(member)):
        #calculating the score based on how far the new string is away from the target string
        score += abs(ord(member[i]) - ord("Hello TV Land"[i]))
        
    return score
    
def breed(mom, dad):
    #crossover
    crossPoint = random.randint(0,12)
    
    return mom[:crossPoint] + dad[crossPoint:]

def mutate(kid, prob):
    for i in range(len(kid)):
        #mutate the character at random
        if random.random() < prob:
            #if kid mutates we mutate one of it's characters
            kid = kid[:i] + random.choice(string.ascii_letters + string.digits + " ") + kid[i+1:]
    return kid
    
looping = True
while looping:
    if nGnrts == 0:
        #initialize random population
        for i in range (100):
            pop.append(popMember(''.join(random.choices(string.ascii_letters + string.digits + " ", k=13))))
        popSize = len(pop)
        #create random population
        
    #fitness test
    for k in range(popSize):
        pop[k].score = fitness(pop[k].string)

    #rank the population from best to worst - lowest to highest score
    pop.sort(key=lambda x: x.score) #this sorts by the .score attribute from the class
    
    #breed new population members
    d = int(percent2keep * popSize) #keeping 20% of the population and replacing the rest
    
    newPop = [] #making the new population
    for k in range(d):
        newPop.append(pop[k])
        
    #elite selection of parents
    for k in range(d, popSize):
        mom = random.randint(0, d-1)
        dad = random.randint(0, d-1)
        
        kid = breed(pop[mom].string, pop[dad].string)
        kid = mutate(kid, 0.1)
        newPop.append(popMember(kid))
        
    #replace the old population with the newly bred population     
    pop = newPop
    print(pop[0].string + f" --- Gen: {nGnrts}")
    nGnrts += 1
    
    #we stop when top 20% of the pop members are fit enough
    #this is a for loop that goes over the top 20% members and checks if every single
    #one of them has score==0
    #all function returns if the whole for loop returned true for every score
    if all(pop[i].score == 0 for i in range(d)) == True:
        looping = False
    