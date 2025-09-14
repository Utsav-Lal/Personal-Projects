from tkinter import *
import math
from rule import *

tk = Tk()
w = 400
h = 400
canvas = Canvas(tk, width=w, height=h)
canvas.pack()

state = firststate()[:]

def draw():
    global state
    pos, state = rule(state)
    if len(pos) == 1:
        x, y = linscale(pos[0], h/2)
    else:
        x, y = linscale(pos[0], pos[1])
    canvas.create_rectangle(x, y, x, y, outline="black")
    canvas.after(1, draw)

    

draw()

tk.mainloop()
