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
gravstrength = 0.1/timestep*8

enddict = {}
pointlist = []

currpos = canvas.create_oval(0, 0, 2, 2, fill='red', outline='red')
co6 = 36
spx=0
spy=-175
spy2=90
class carrier:
    mass = 3  # water mass
    maxful = 200
    def __init__(self, dist, rad, invisible=False):
        self.dist = dist
        self.rad = rad
        self.full = 0
        self.invisible = invisible
        if not self.invisible:
            self.sphere = canvas.create_oval(math.cos(self.rad)*self.dist+self.full+w/2+spx, math.sin(self.rad)*self.dist+self.full+h/2+spy, math.cos(self.rad)*self.dist-self.full+w/2+spx, math.sin(self.rad)*self.dist-self.full+h/2+spy)
            self.rod = canvas.create_line(w/2+spx, h/2+spy, math.cos(self.rad)*self.dist+w/2+spx, math.sin(self.rad)*self.dist+h/2+spy)

    def rotate(self, speed):
        self.rad += speed*timestep
        if not self.invisible:
            canvas.coords(self.sphere, math.cos(self.rad)*self.dist+self.full+w/2+spx, math.sin(self.rad)*self.dist+self.full+h/2+spy, math.cos(self.rad)*self.dist-self.full+w/2+spx, math.sin(self.rad)*self.dist-self.full+h/2+spy)
            canvas.coords(self.rod, w/2+spx, h/2+spy, math.cos(self.rad)*self.dist+w/2+spx, math.sin(self.rad)*self.dist+h/2+spy)

    def torquemass(self):  # torque, inertia
        return (carrier.mass*self.full*gravstrength*math.cos(self.rad)*self.dist, carrier.mass*self.full*self.dist**2)

class wheel:
    threshold = 1
    fillspeed = 5
    emptyspeed = 0.25/3
    basemass = 0
    time = 0
    friction=15/timestep*75
    def __init__(self, size, spokes, tilt, fillspeed, emptyspeed, invisible=False):
        self.size = size
        self.spokes = spokes
        self.carrierlist = []
        self.tilt = tilt
        self.fillspeed = fillspeed
        self.emptyspeed = emptyspeed
        for i in range(self.spokes):
            self.carrierlist.append(carrier(self.size, 2*i*math.pi/self.spokes+self.tilt+math.pi/2, invisible))
        self.vel = 10
        self.tiltchange = self.tilt
        self.invisible = invisible
        self.threshold=math.pi/self.spokes*wheel.threshold

    @classmethod
    def timeupdate(cls):
        wheel.time += 1
        canvas.after(int(timestep*100), wheel.timeupdate)


    def run(self):
        spokechange = (self.spokes/10)
        totalamomentum = wheel.basemass*self.vel
        totaltorque = 0
        inertia = wheel.basemass
        totalmass = wheel.basemass
        totaly = 0
        totalx = 0
        for i in self.carrierlist:
            # collect current information
            n = i.torquemass()
            totalamomentum += self.vel*n[1]

            if abs(i.rad%(2*math.pi)-(3*math.pi/2)) <= self.threshold:  # fill
                maxamount = carrier.maxful-i.full
                dropmomentum = (2*(self.size-self.size*math.sin(i.rad))*gravstrength)**0.5*min(maxamount, self.fillspeed*timestep)*carrier.mass
                sidemomentum = -dropmomentum*math.sin(i.rad-math.pi/2)
                amomentum = sidemomentum*self.size
                amomentum=0
                totalamomentum += amomentum
                
                i.full += min(maxamount, self.fillspeed * timestep)

            # empty
            totalamomentum -= self.vel*(i.full-max(i.full-self.emptyspeed*i.full*timestep, 0))*carrier.mass*self.size**2
            i.full = max(i.full-self.emptyspeed*i.full*timestep, 0)

            # get new information
            m = i.torquemass()
            inertia += m[1]
            totaltorque += m[0]*timestep

            totalmass += carrier.mass*i.full
            totaly += carrier.mass*i.full*i.dist*math.sin(i.rad)
            totalx += carrier.mass*i.full*i.dist*math.cos(i.rad)


        # fix velocity
        self.vel = totalamomentum/inertia

        # apply torque
        self.vel += (totaltorque-self.vel*wheel.friction*spokechange*timestep)/inertia
        for i in self.carrierlist:
            i.rotate(self.vel)
        comy = totaly/totalmass
        comx = totalx/totalmass
        comx = comx*5+w/2
        comy=comy*4+h/2
        comvel=self.vel*400+h/2
        colorx = "#"+3*format(math.floor(((totalx/totalmass*0.5+self.size))*128/self.size), '02x')
        colory = "#"+3*format(math.floor(((totaly/totalmass*0.5+self.size))*128/self.size),'02x')
        colorvel = "#"+3*format(math.floor(self.vel*60+120),'02x')
        colort = colory
        #print(colort)
        #print(color)
        if wheel.time % 50 == 0:
            #canvas.create_oval((wheel.time/80), (self.tiltchange/10+200), (wheel.time/80)+1, (self.tiltchange/10+200) + 1)
            if wheel.time == 10000 or True:
                #print(self.tiltchange)
                #print(1)
                if True:
                    #print(self.vel)
                    if len(pointlist) != 0:
                        #canvas.create_line(pointlist[-1][0], pointlist[-1][1], (inertia/4000), (self.vel*200+h/2))
                        canvas.create_line(pointlist[-1][0], pointlist[-1][1], comvel-spx, h-comy+spy2, fill=colorx)
                    #canvas.create_oval((inertia/8000)%400, (self.vel*100+200) % 400, (inertia/8000)%400+1, (self.vel*100+200) % 400 + 1)
                    #pointlist.append(((inertia/4000), (self.vel*200+h/2)))
                    pointlist.append((comvel-spx, h-comy+spy2))
                    canvas.coords(currpos, pointlist[-1][0]-1, pointlist[-1][1]-1, pointlist[-1][0]+1, pointlist[-1][1]+1)
                    canvas.tag_raise(currpos)
        self.tiltchange += self.vel

        if not self.invisible or False:
            canvas.after(int(100*timestep), self.run) 



    # def run(self):
    #     totaltorque = 0
    #     inertia = wheel.basemass
    #     newinertia = wheel.basemass
    #     amountin = 0
    #     avel = 0
    #     for i in self.carrierlist:
    #         n = i.torquemass()
    #         inertia += n[1]
    #         if abs(i.rad%(2*math.pi)-(3*math.pi/2)) <= wheel.threshold:
    #             i.full += wheel.fillspeed*timestep
    #             #k = i.full
    #             #i.full = min(i.full+wheel.fillspeed*timestep, carrier.maxful)
    #             amountin += i.full*carrier.mass
    #         i.full = max(i.full-wheel.emptyspeed*timestep, 0)
    #         m = i.torquemass()
    #         totaltorque += m[0]
    #         newinertia += m[1]

    #     if inertia != 0:
    #         avel = inertia*self.vel
    #         self.vel = avel/(inertia+amountin*self.size**2)
    #         self.vel += totaltorque/(newinertia)
    #         #self.vel *= 0.9999
    #     for i in self.carrierlist:
    #         i.rotate(self.vel)
    #     canvas.after(int(100*timestep), self.run)

tiltshift = 0.003
tiltshift = 0
fillshift = 0.0001
times = 1
plots = 5
basetilt=0.153
basetilt=0.153
basetilt=0.3

wheellist = []
import matplotlib.pyplot as plt
#for i in range(times-1,0-1,-1):
for i in range(1, 2):
    for j in range(times-1, 0-1,-1):
        k=wheel(100, 60, basetilt+j*tiltshift*10/times, wheel.fillspeed+i*fillshift*10/times, wheel.emptyspeed, invisible=False)
        wheellist.append(k)
        k.run()
        if False:
            wheel.time = 0
            for x in range(0, 10001):
                k.run()
                wheel.timeupdate()
            if k.tiltchange <= 1100:
                plt.scatter(i*tiltshift*10/times, j*fillshift*10/times)
            plt.pause(0.01)

# for x in range(0, 200000):
#     wheellist[0].run()


print(len(wheellist))

def runfunc():

    # if wheel.time == 20000:
        
    #     for i in range(len(wheellist)):
    #         enddict[(i//times, i%times)] = wheellist[i].vel
    #     for i in range(times):
    #         for j in range(times):
    #             k = enddict[(i, j)]
    #             #print(k)
    #             color = None
    #             if k <= 0:
    #                 color = "red"
    #                 #plt.scatter(i, j)
    #             else:
    #                 color = "white"
    #             canvas.create_oval(i, j, i, j, fill=color, outline=color)
    #     plt.show()
    #     return
    for i in wheellist:
        i.run()
    #wheel.timeupdate()
    #canvas.after(int(timestep*100), runfunc)
    #runfunc()
    canvas.after(1, runfunc)

wheel.timeupdate()
tk.mainloop()
if False:
    for x in range(0, 20001):
        runfunc()
        if x % 100 == 0 and True:
            print(x)
        #print(x)
        tk.update()
        time.sleep(0.01)
#plt.show()


