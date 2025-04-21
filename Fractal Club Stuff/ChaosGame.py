from tkinter import *
import random

tk = Tk()
w = 400
h = 400
canvas = Canvas(tk, width=w, height=h)
canvas.pack()


# User-provided stuff
vertices = [(100, 100), (300, 100), (100, 300), (300, 300)]  # set of vertices
r = 0.5  # r-value
remember = 1  # n-value
def nextvertex(memory, currpos):  # rule

    # ex. does not choose the same vertex twice in a row
    choicelist = []
    for i in range(len(vertices)):
        if i != memory[0]:
            choicelist.append(i)
    potentialchoice = random.choice(choicelist)

    # ex. avoids choosing the next point to be closer than 65 units to the vertices
    projnewpos = ((1-r)*currpos[0]+r*vertices[potentialchoice][0], (1-r)*currpos[1]+r*vertices[potentialchoice][1])
    for i in vertices:
        if (i[0]-projnewpos[0])**2+(i[1]-projnewpos[1])**2 < 65**2:
            return nextvertex(memory, currpos)

    return potentialchoice


for i in vertices:
    canvas.create_oval(i[0]-5, i[1]-5, i[0]+5, i[1]+5, fill="black")


memory = []
for i in range(remember):
    memory.append(0)

currpos = (0,0)  # position of point generated

def newpos(memory, currpos, vertex):
    a = canvas.create_oval(currpos[0], currpos[1], currpos[0], currpos[1])
    memory.append(vertex)
    memory = memory[len(memory)-remember:]
    return memory, ((1-r)*currpos[0]+r*vertices[vertex][0], (1-r)*currpos[1]+r*vertices[vertex][1])




def draw():
    global memory
    global currpos

    vertex = nextvertex(memory, currpos)
    memory, currpos = newpos(memory, currpos, vertex)
    canvas.after(1, draw)

draw()


tk.mainloop()
