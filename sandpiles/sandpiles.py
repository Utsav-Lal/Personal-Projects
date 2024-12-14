from graph import Graph
from termcolor import colored
import time



sandgraph = Graph([("P", "A"), ("P", "E"), ("P", "C"), ("A", "D"), ("C", "F"), ("D", "E"), ("E", "F"), ("D", "G"), ("E", "H"), ("F", "S"), ("G", "H"), ("H", "S")])

graphlist = []
side = 20
inlist = list(range(side))
inlist = [side*side//2]
outlist = [0, side-1, side*(side-1), side*side-1]


donedict = {}
for x in range(side):
    for y in range(side):

        if y < side-1:
            graphlist.append((str(x*side+y), str(x*side+y+1)))
        elif True and y == side-1:
            graphlist.append((str(x*side+y), str(x*side)))
        if x < side-1:
            graphlist.append((str(x*side+y),str(x*side+side+y)))
        elif x == side-1:
            graphlist.append((str(x*side+y),str(y)))
sandgraph = Graph(graphlist)


amountdict = {}
for i in sandgraph.get_vertices():
    amountdict[i]=0

often = 2*len(inlist)
poslist = []
for x in range(100000):
    brokedict = {}
    placedict = {}
    currpos = []
    for i in range(side*side):
        currpos.append(amountdict[str(i)])
        placedict[str(i)] = 0
    currpos = tuple(currpos)
    

    if (x % often ==0):
        
        if currpos in poslist:
            print(currpos, x)
        poslist.append(currpos)
        for i in range(side*side):
            if i in inlist:
                amountdict[str(i)] += 1
    
    
    
    for i in sandgraph.get_vertices():
        a = sandgraph.get_neighbors(i)
        
        if amountdict[i] >= len(a):
            brokedict[i] = len(a)
            amountdict[i] -= len(a)
            for j in a:
                if int(j) not in outlist:
                    placedict[j] += 1
        else:
            brokedict[i] = 0
    for i in placedict:
        amountdict[i] += placedict[i]

    if x > 10000:
        total = ""
        for y in range(side):
            line = ""
            for z in range(side):
                name = ""
                if True:
                    k = amountdict[str(y*side+z)]
                    n = ""
                    char = "██"
                    char2 = "  "
                    if k == 0:
                        n = "  "
                    elif k == 1:
                        n = colored(char, "blue")
                    elif k == 2:
                        n = colored(char, "cyan")
                    elif k == 3:
                        n = colored(char, "green")
                    elif k == 4:
                        n = colored(char, "yellow")
                    elif k == 5:
                        n = colored(char, "red")
                    else:
                        n = colored(char, "white")
                        
                    line += n
                elif False:
                    if amountdict[str(y*side+z)] == 0:
                        line += "  "
                    else:
                        line += str(amountdict[str(y*side+z)])+" "
                elif False:
                    if placedict[str(y*side+z)]-brokedict[str(y*side+z)] < 1:
                        line += " "+" "
                    elif placedict[str(y*side+z)]-brokedict[str(y*side+z)] >=1:
                        line += "• "
                    elif placedict[str(y*side+z)] == 2:
                        line += "x "
                    else:
                        line += str(amountdict[str(y*side+z)])+" "
                elif False:
                    if brokedict[str(y*side+z)] > 0:
                        line += "• "
                    else:
                        line += "  "
                elif True:
                    if amountdict[str(y*side+z)] >= 4:
                        line += str(amountdict[str(y*side+z)])+" "
                    else:
                        line += "  "
                
                else:
                    if brokedict[str(y*side+z)] != 0:
                        nexto = False
                        for i in sandgraph.get_neighbors(str(y*side+z)):
                            if brokedict[i] == 0:
                                nexto = True
                        if nexto:
                            line += "• "
                        else:
                            line += "  "
                    else:
                        line += "  "
            total += line+"\n"

        total += str(x//often)
        print(total)
        time.sleep(0.1)
    else:
        pass
        #print(x)