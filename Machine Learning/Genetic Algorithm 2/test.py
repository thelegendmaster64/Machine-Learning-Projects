mom = [['11'], ['11'], ['11']]
dad = [['00'], ['00'], ['00']]

for i in range(len(mom)):
    move = ""
    move = mom[i][0]
    move2 = dad[i][0]
    ch1 = move[:1]
    ch2 = move2[1:]
    

    final = ch1 + ch2

    print(final)