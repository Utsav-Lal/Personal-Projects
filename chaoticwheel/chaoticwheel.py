# Demonstrates the relationship between the chaotic waterwheel and the lorentz attractor
# Water is added to the bucket on top of the wheel - bucket size = fullness
# In graph: x=velocity, y=height of COM, color=horizontal position of COM

import math
from tkinter import *
import random
import time
tk = Tk()
w = 800
h = 800
canvas = Canvas(tk, width=w, height=h)
canvas.pack()

timestep = 0.01
gravstrength = 0.1/timestep*8 # strength of gravity
spokes = 60 # number of spokes
basetilt=0.3 # initial angular offset

pointlist = [] # stores the points that draw out the strange attractor

currpos = canvas.create_oval(0, 0, 2, 2, fill='red', outline='red') # dot that indicates the current position in the attractor

spx=0 # x-position of the wheel
spy=-175 # y-position of the wheel
spy2=90 # y-offset of the attractor drawing

class carrier: # stores information of and helps simulate the water carrier
    mass = 3  # water mass
    maxful = 200
    def __init__(self, dist, rad, invisible=False):
        self.dist = dist
        self.rad = rad
        self.full = 0
        self.invisible = invisible
        if not self.invisible: # draws the carrier and spoke
            self.sphere = canvas.create_oval(math.cos(self.rad)*self.dist+self.full+w/2+spx, math.sin(self.rad)*self.dist+self.full+h/2+spy, math.cos(self.rad)*self.dist-self.full+w/2+spx, math.sin(self.rad)*self.dist-self.full+h/2+spy)
            self.rod = canvas.create_line(w/2+spx, h/2+spy, math.cos(self.rad)*self.dist+w/2+spx, math.sin(self.rad)*self.dist+h/2+spy)

    def rotate(self, speed):  # rotates the carrier by the speed of the rotation
        self.rad += speed*timestep
        if not self.invisible:
            canvas.coords(self.sphere, math.cos(self.rad)*self.dist+self.full+w/2+spx, math.sin(self.rad)*self.dist+self.full+h/2+spy, math.cos(self.rad)*self.dist-self.full+w/2+spx, math.sin(self.rad)*self.dist-self.full+h/2+spy)
            canvas.coords(self.rod, w/2+spx, h/2+spy, math.cos(self.rad)*self.dist+w/2+spx, math.sin(self.rad)*self.dist+h/2+spy)

    def torquemass(self):  # returns the torque applied, inertia of the carrier
        return (carrier.mass*self.full*gravstrength*math.cos(self.rad)*self.dist, carrier.mass*self.full*self.dist**2)

class wheel:  # handles the wheel
    threshold = 1  # indicates how far from the top a carrier can be to get filled
    fillspeed = 5  # controls how fast water flows in
    emptyspeed = 0.25/3  # controls how fast water empties
    basemass = 0.1  # dry mass of the wheel
    time = 0  # counts time - used for drawing the attractor
    friction=15/timestep*75  # friction of the wheel
    def __init__(self, size, spokes, tilt, fillspeed, emptyspeed, invisible=False):
        self.size = size
        self.spokes = spokes
        self.carrierlist = []
        self.tilt = tilt
        self.fillspeed = fillspeed
        self.emptyspeed = emptyspeed

        for i in range(self.spokes):  # creates the carriers
            self.carrierlist.append(carrier(self.size, 2*i*math.pi/self.spokes+self.tilt+math.pi/2, invisible))

        self.vel = 10  # initial velocity
        self.tiltchange = self.tilt
        self.invisible = invisible
        self.threshold=math.pi/self.spokes*wheel.threshold

    @classmethod
    def timeupdate(cls):  # updates time
        wheel.time += 1
        canvas.after(int(timestep*100), wheel.timeupdate)


    def run(self):  # runs the wheel
        spokechange = (self.spokes/10)
        totalamomentum = wheel.basemass*self.vel
        totaltorque = 0
        inertia = wheel.basemass
        totalmass = wheel.basemass
        totaly = 0
        totalx = 0
        for i in self.carrierlist:
            # measures angular momentum
            n = i.torquemass()
            totalamomentum += self.vel*n[1]

            # fills carriers
            if abs(i.rad%(2*math.pi)-(3*math.pi/2)) <= self.threshold:  # fill
                maxamount = carrier.maxful-i.full
                i.full += min(maxamount, self.fillspeed * timestep)

            # empty carriers and measure momentum change
            totalamomentum -= self.vel*(i.full-max(i.full-self.emptyspeed*i.full*timestep, 0))*carrier.mass*self.size**2
            i.full = max(i.full-self.emptyspeed*i.full*timestep, 0)

            # get new inertia and torque
            m = i.torquemass()
            inertia += m[1]
            totaltorque += m[0]*timestep

            # measure mass and COM
            totalmass += carrier.mass*i.full
            totaly += carrier.mass*i.full*i.dist*math.sin(i.rad)
            totalx += carrier.mass*i.full*i.dist*math.cos(i.rad)


        # update velocity
        self.vel = totalamomentum/inertia

        # apply torque
        self.vel += (totaltorque-self.vel*wheel.friction*spokechange*timestep)/inertia

        # rotate wheel
        for i in self.carrierlist:
            i.rotate(self.vel)

        # gets the coordinates of the state in the attractor
        comy = totaly/totalmass
        comx = totalx/totalmass
        comx = comx*5+w/2
        comy=comy*4+h/2
        comvel=self.vel*400+h/2

        # color is used for the third dimension
        colorx = "#"+3*format(math.floor(((totalx/totalmass*0.5+self.size))*128/self.size), '02x')
        colory = "#"+3*format(math.floor(((totaly/totalmass*0.5+self.size))*128/self.size),'02x')
        colorvel = "#"+3*format(math.floor(self.vel*60+120),'02x')
        
        colort = colory  # the y-position is the third dimension

        # draws the attractor
        if wheel.time % 50 == 0:  # only does it every 50 steps to reduce lag
            if len(pointlist) != 0:  # creates line to previous state
                canvas.create_line(pointlist[-1][0], pointlist[-1][1], comvel-spx, h-comy+spy2, fill=colorx)
            pointlist.append((comvel-spx, h-comy+spy2))  # adds new state to path
            canvas.coords(currpos, pointlist[-1][0]-1, pointlist[-1][1]-1, pointlist[-1][0]+1, pointlist[-1][1]+1)  # repositions state marker
            canvas.tag_raise(currpos)

        self.tiltchange += self.vel # records angular position

        if not self.invisible or False:
            canvas.after(int(100*timestep), self.run) 


# creates wheels - only one is created but there is code for more at the same time to show divergence
tiltshift = 0.003
fillshift = 0.0001
times = 1
plots = 5

wheellist = []

for i in range(1, 2):
    for j in range(times-1, 0-1,-1):
        k=wheel(100, spokes, basetilt+j*tiltshift*10/times, wheel.fillspeed+i*fillshift*10/times, wheel.emptyspeed, invisible=False)
        wheellist.append(k)
        k.run()

def runfunc():  # runs wheels
    for i in wheellist:
        i.run()
    canvas.after(1, runfunc)

wheel.timeupdate()
tk.mainloop()


