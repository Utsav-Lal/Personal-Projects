#Use arrow keys to scroll

import time

import random
from tkinter import *
tk = Tk()
canvas = Canvas(tk, width=1000, height=1000)
canvas.pack()
xoffSet = 0
yoffSet = 0
scrollx = 0
scrolly = 0
objects = []
#list of all objects

class Object:
    def __init__(self, canvas, x, y, xVel, yVel, radius, focus=False):
        self.canvas = canvas
        self.x = x-xoffSet
        self.y = y-yoffSet
        self.xVel = xVel
        self.yVel = yVel
        self.radius = radius
        self.size = radius**2 * 3.14
        objects.append(self)
        self.id = self.canvas.create_oval(self.x + \
self.radius, self.y + self.radius, self.x - self.radius, self.y - self.radius, \
tags="Bob", fill='#000000')
        self.canvas.coords(self.id, self.x-self.radius+xoffSet, self.y-self.radius+yoffSet, self.x+self.radius+xoffSet, self.y+self.radius+yoffSet)

        self.time = 0
        self.focus = focus



    def update(self):
        #sets up movement
        

        #updates x and y positions
        
        
        for i in objects:
            #tells object where to go and what to do by checking
            #all other object positions
            xDistance = i.x - self.x
            yDistance = i.y - self.y

            if i != self:
                distance = (xDistance**2 + yDistance**2)**(1/2)
                if distance != 0 and self.size != 0:
                    xUnit = xDistance/distance
                    yUnit = yDistance/distance
                    gConstant = 1
                    self.force = gConstant * self.size * i.size / (distance ** 2)


                    if distance <= self.radius + i.radius:
                        #collision detection


                        if self.size >= i.size:

                            self.size += i.size
                            
                            self.radius = ((self.size)  / 3.14)**(1/2)
                            self.canvas.coords(self.id, self.x-self.radius+xoffSet, self.y-self.radius+yoffSet, self.x+self.radius+xoffSet, self.y+self.radius+yoffSet)

                            self.xVel += (i.size/self.size)*i.xVel
                            self.yVel += (i.size/self.size)*i.yVel

                            i.delete()
                            #when objects collide they combine
                        
                    
                    if self.size != 0:
                        moved = self.force / self.size
                        self.xVel += moved * xUnit
                        self.yVel += moved * yUnit

                
            
                



                        

                
                        
 
    def mov(self):
        global xoffSet
        global yoffSet
        #actually moves the object
        self.x += self.xVel
        self.y += self.yVel
        if self.focus == True:
            xoffSet -= self.xVel
            yoffSet -= self.yVel
        self.canvas.coords(self.id, self.x-self.radius+xoffSet, self.y-self.radius+yoffSet, self.x+self.radius+xoffSet, self.y+self.radius+yoffSet)

        self.time += 1

    
           

        

    def delete(self):
        #used for self destruct
        self.size = 0
        self.radius = 0
        self.canvas.coords(self.id, -1000000, -1000000, -1000000, -1000000)
        
        for i in range(0, len(objects)-1):
            if objects[i] == self:
                del(objects[i])
        del self

    


planet3 = Object(canvas, 500, 900, 3, 0, 10)
planet4 = Object(canvas, 500, 850, 0.2, 0.2, 0.1)
planet5 = Object(canvas, 500, 500, 0, 0, 30)
#create planets by typing in: [name of planet] = Object(canvas, x, y, xspeed,\
#yspeed, size)


def run():
    #tells all objects to move

    for x in objects:
        x.update()
    for x in objects:
        x.mov()
        


    canvas.after(10, run)
def srun():
    #tells all objects to check for scrolling
    scrolldraw()
    canvas.after(10, srun)
spawnTimer = 20
def spawn():
    global spawnTimer
#auto spawns objects(insert code in if you want to to do this)
#create planets by typing in: [name of planet] = Object(canvas, x, y, xspeed,\
#yspeed, size)
    
    Object(canvas, random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 3),\
random.randint(0, 3), random.randint(0, 10))
    if (spawnTimer > 0):
        spawnTimer -= 1
        canvas.after(0, spawn)

def scrollext(event):
    #checks for scrolling
    scroll(event)
def antiscrollext(event):
    #checks for stopping scrolling
    antiscroll(event)
def scroll(event):
        global scrolly
        global scrollx
        #sets the scrolling movement
        x = 2
        if event.keysym == 'Up':
            scrolly = x
        if event.keysym == 'Down':
            scrolly = -x
        if event.keysym == 'Left':
            scrollx = x
        if event.keysym == 'Right':
            scrollx = -x
def antiscroll(event):
        global scrolly
        global scrollx
        #stops scrolling movement
        if event.keysym == 'Up':
            scrolly = 0
        if event.keysym == 'Down':
            scrolly = 0
        if event.keysym == 'Left':
            scrollx = 0
        if event.keysym == 'Right':
            scrollx = 0

def scrolldraw():
        global scrolly
        global scrollx
        global xoffSet
        global yoffSet
        #moves object for scrolling
        if scrollx != 0 or scrolly != 0:

            xoffSet += scrollx;
            yoffSet += scrolly;
            
canvas.bind_all("<KeyPress>", scrollext)
canvas.bind_all("<KeyRelease>", antiscrollext)
#checks for keybinds

run()
spawn()
srun()
tk.mainloop()
