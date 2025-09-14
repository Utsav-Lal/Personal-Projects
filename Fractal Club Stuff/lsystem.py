import turtle

from turtle import *



class L_system:
    def __init__(self, variables, constants, axiom, rules, moverules):
        self.variables = variables
        self.constants = constants
        self.axiom = axiom
        self.rules = rules
        self.state = self.axiom
        self.moverules = moverules
        self.lifo = []

    def step(self):
        newstate = ""
        for i in self.state:
            if i in self.variables:
                newstate += self.rules[i]
            else:
                newstate += i
        self.state = newstate
        return self.state
    
    def stepitr(self, itr):
        for i in range(itr):
            self.step()
        return self.state
    
    def draw(self):
        for i in self.state:
            self.moverules(i, self.lifo)


penup()
turtle.speed(200)
turtle.setpos((0, 0)) # set original position
pendown()
turtle.tracer(0, 0)
pensize(0.1)


# set movement rules
def movefn(inp, lifo):
    if inp == "0":
        forward(10)
    elif inp == "+":
        left(7)
    elif inp == "-":
        right(7)
    elif inp == "[":
        lifo.append((pos(), heading()))
    elif inp == "]":
        ps, hding = lifo.pop()
        penup()
        setpos(ps)
        setheading(hding)
        pendown()
        

# create Lsystem
ourl = L_system("0", "[]+-", "0", {"0":"0[--------0]+0[++++++++0]+0"}, movefn)


print(ourl.stepitr(7))  # set iterations
ourl.draw()

turtle.update()
input("Done:")
