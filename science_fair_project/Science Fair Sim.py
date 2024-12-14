import random
import math
import sys
from tkinter import *

tk = Tk()
canvas = Canvas(tk, width=400, height=400)
canvas.pack()

creaturelist = {}
predatorlist = {}
mutationrate = 10
filled = 10
waterlist = []
rate = 2
foodlist = []
foodfill = 10
changelist = ['flood(10, 10)', 'drought(20, 20)', 'flood(30, 30)', 'drought(10, 10)', 'flood(10, 10)', 'drought(20, 20)']
debug = True

def average(nums):
    k = 0
    for i in nums:
        k += i
    k /= len(nums)
    return k


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


class creature:
    def __init__(self, genesGiven=None, coords=None, focus=False):
        if genesGiven == None:
            self.genes = {
                'speed': [random.randint(0, 100),
                          random.randint(0, 100)],
                'vision': [random.randint(0, 100),
                           random.randint(0, 100)],
                'hunger tolerance':
                [random.randint(0, 100),
                 random.randint(0, 100)],
                'thirst tolerance':
                [random.randint(0, 100),
                 random.randint(0, 100)],
                'forwardmove': [random.randint(0, 50),
                                random.randint(0, 50)],
                'minturn': [random.randint(0, 359),
                            random.randint(0, 359)],
                'maxturn': [random.randint(0, 359),
                            random.randint(0, 359)]
            }
        else:
            self.genes = genesGiven
        if coords == None:
            self.coords = [
                random.randint(0, 400),
                random.randint(0, 400),
                random.randint(0, 359)
            ]
        else:
            self.coords = coords
        self.x = self.coords[0]
        self.y = self.coords[1]
        self.degrees = self.coords[2]
        self.phenotype = {
            'speed': [average(self.genes['speed'])],
            'vision': [average(self.genes['vision'])],
            'hunger tolerance': [average(self.genes['hunger tolerance'])],
            'thirst tolerance': [average(self.genes['thirst tolerance'])],
            'forwardmove': [average(self.genes['forwardmove'])],
            'minturn': [average(self.genes['minturn'])],
            'maxturn': [average(self.genes['maxturn'])]
        }
        self.age = 0
        self.moved = 0
        creaturelist[self] = self
        self.index = self
        self.thirst = 100
        self.hunger = 100
        self.state = 'wander'
        self.focus = focus
        self.matecooldown = 0
        self.dead = False
        self.draw()
        self.testmove()

    def draw(self):
        thirsttolerance = self.phenotype['thirst tolerance'][0]
        hungertolerance = self.phenotype['hunger tolerance'][0]
        vision = self.phenotype['vision'][0]
        
        self.id = canvas.create_oval(self.x - 3,
                                     self.y - 3,
                                     self.x + 3,
                                     self.y + 3,
                                     fill='black')
        if debug == True:
            self.see = canvas.create_oval(self.x - vision, self.y - vision,
                                      self.x + vision, self.y + vision)
            self.thirstbar = canvas.create_rectangle(self.x - 10, \
                                                     self.y - 10, self.x + 10, self.y - 15, fill='grey')
            self.thirstfill = canvas.create_rectangle(self.x-10, self.y-10, \
                                                      self.x-10+self.thirst/5, self.y-15, fill='blue')
            self.thirstmark = canvas.create_rectangle(self.x-10+thirsttolerance/5,\
                                                 self.y-10, self.x-10+thirsttolerance/5, self.y-15, outline='white')
            self.hungerbar = canvas.create_rectangle(self.x - 10, \
                                                     self.y - 20, self.x + 10, self.y - 25, fill='grey')
            self.hungerfill = canvas.create_rectangle(self.x-10, self.y-20, \
                                                      self.x-10+self.hunger/5, self.y-25, fill='#a6a419')
            self.hungermark = canvas.create_rectangle(self.x-10+hungertolerance/5,\
                                                 self.y-20, self.x-10+hungertolerance/5, self.y-25, outline='black')
            self.matebar = canvas.create_rectangle(self.x-10, self.y-30, self.x+10, self.y-35, fill='grey')
            self.matefill = canvas.create_rectangle(self.x-10, self.y-30, self.x-10+self.matecooldown*4, self.y-35, fill='red')
            self.agebar = canvas.create_rectangle(self.x-10, self.y-40, self.x+10, self.y-45, fill='grey')
            self.agefill = canvas.create_rectangle(self.x-10, self.y-40, self.x-10+self.age/3, self.y-45, fill='white')
            if self.age < 10:
                canvas.itemconfig(self.matefill, fill='black')
    def testmove(self):
        if self.focus == True:

            pass

        if self.state == 'wander':
            canvas.itemconfig(self.id, fill='black')
        elif self.state == 'drink':
            canvas.itemconfig(self.id, fill='cyan')
        elif self.state == 'eat':
            canvas.itemconfig(self.id, fill='yellow')
        elif self.state == 'run':
            canvas.itemconfig(self.id, fill='white')
        elif self.state == 'mate':
            canvas.itemconfig(self.id, fill='pink')
        vision = self.phenotype['vision'][0]
        thirsttolerance = self.phenotype['thirst tolerance'][0]
        hungertolerance = self.phenotype['hunger tolerance'][0]
        speed = self.phenotype['speed'][0]
        p = []
        q = []
        b = None
        for i in predatorlist:
          if distance(i.x, i.y, self.x, self.y) <= vision:
            if b == None:
              b = i
            elif b != None:
              if distance(i.x, i.y, self.x, self.y) < distance(b.x, b.y, self.x, self.y):
                b = i
        if b != None:
          self.degrees = math.degrees(
                      math.atan((b.y - self.y) / (b.x - self.x)))
          self.degrees -= 180
          x1 = math.cos(math.radians(self.degrees)) * speed / 100
          y1 = math.sin(math.radians(self.degrees)) * speed / 100
          x1 += self.x
          y1 += self.y
          if distance(x1, y1, b.x, b.y) < distance(self.x, self.y, b.x, b.y):
            self.degrees += 180
          self.state = 'run'
        else:
          if self.state == 'run':
            self.state = 'wander'
        
        if self.thirst < thirsttolerance and self.state != 'run':
            

            k = False
            b = None
            for i in waterlist:
                if distance(i.x, i.y, self.x, self.y) < i.fill and i.water == True:
                    k = True
                elif distance(i.x, i.y, self.x, self.y) < i.fill + vision and i.water == True:
                    if b == None or distance(b.x, b.y, self.x,
                                             self.y) > distance(
                                                 i.x, i.y, self.x, self.y):
                        b = i
            if k == True:
                self.thirst = 100
                self.state = 'wander'
            elif b != None:
                self.degrees = math.degrees(
                    math.atan((b.y - self.y) / (b.x - self.x)))
                x1 = math.cos(math.radians(self.degrees)) * speed / 100
                y1 = math.sin(math.radians(self.degrees)) * speed / 100
                x1 += self.x
                y1 += self.y
                if distance(x1, y1, b.x, b.y) > distance(self.x, self.y, b.x, b.y):
                  self.degrees += 180
                self.state = 'drink'
            elif b == None:
              self.state = 'wander'
        if self.thirst < thirsttolerance:
            if debug == True:
                canvas.itemconfig(self.thirstbar, fill='cyan', outline='cyan')
        else:
            if debug == True:
                canvas.itemconfig(self.thirstbar, fill='grey', outline='black')
        if self.hunger < hungertolerance:
            if debug == True:
                canvas.itemconfig(self.hungerbar, fill='yellow', outline='yellow')
        else:
            if debug == True:
                canvas.itemconfig(self.hungerbar, fill='grey', outline='black')
        if self.age >= 10:
            if debug == True:
                canvas.itemconfig(self.matefill, fill='red')
        if self.matecooldown <= 0 and self.age >= 10 and \
           self.thirst >= thirsttolerance and self.hunger >= hungertolerance:
            if debug == True:
                canvas.itemconfig(self.matebar, fill='pink', outline='pink')
        else:
            if debug == True:
                canvas.itemconfig(self.matebar, fill='grey', outline='black')
        

        if self.hunger < hungertolerance and self.state != 'drink' and self.state != 'run':
            k = False
            b = None
            c = None
            for i in foodlist:
                if distance(i.x, i.y, self.x, self.y) < 10 and i.food == True:
                    k = True
                    c = i
                    if self.focus == True:
                        #print(distance(i.x, i.y, self.x, self.y))
                      pass
                elif distance(i.x, i.y, self.x, self.y) < 10 + vision and i.food == True:
                    if b == None or distance(b.x, b.y, self.x,
                                             self.y) > distance(
                                                 i.x, i.y, self.x, self.y):
                        b = i
            if self.focus == True:
                #print(b)
              pass
            if k == True:

                self.hunger = 100
                c.eaten()
                self.state = 'wander'

            elif b != None:
                self.degrees = math.degrees(
                    math.atan((b.y - self.y) / (b.x - self.x)))
                x1 = math.cos(math.radians(self.degrees)) * speed / 100
                y1 = math.sin(math.radians(self.degrees)) * speed / 100
                x1 += self.x
                y1 += self.y
                if distance(x1, y1, b.x, b.y) > distance(self.x, self.y, b.x, b.y):
                  self.degrees += 180
                self.state = 'eat'
            elif b == None:
              self.state = 'wander'
        if self.hunger > hungertolerance and self.thirst > thirsttolerance and self.age >= 10 and self.matecooldown <= 0 and self.state != 'run':

          b = None
          k = False
          c = None
          for i in creaturelist:
            if i.hunger > i.phenotype['hunger tolerance'][0] and i.thirst > i.phenotype['thirst tolerance'][0] and i.age >= 10 and i.matecooldown <= 0 and i.state != 'run' and i != self:
               if distance(self.x, self.y, i.x, i.y) <= 5:
                 k = True
                 c = i
               elif distance(self.x, self.y, i.x, i.y) <= vision:
                  if b == None:
                    b = i
                  elif b != None:
                    
                    if distance(self.x, self.y, i.x, i.y) < distance(self.x, self.y, b.x, b.y):
                      b = i
          
          if k == True:
            l = random.randint(0, 5)
            for x in range(0, l):
              self.procreate(c, l)
            self.matecooldown = 5
            self.state = 'wander'
          elif b != None:
           
            self.degrees = math.degrees(
                    math.atan((b.y - self.y) / (b.x - self.x)))
            x1 = math.cos(math.radians(self.degrees)) * speed / 100
            y1 = math.sin(math.radians(self.degrees)) * speed / 100
            x1 += self.x
            y1 += self.y
            if distance(x1, y1, b.x, b.y) > distance(self.x, self.y, b.x, b.y):
                self.degrees += 180
            self.state = 'mate'
          elif b == None:
            self.state = 'wander'
        if self.moved == 0 and self.state == 'wander':

            if self.phenotype['minturn'][0] > self.phenotype['maxturn'][0]:
                newminturn = self.phenotype['minturn'][0] - 360
                self.degrees += random.randint(
                    int(newminturn), int(self.phenotype['maxturn'][0]))
            else:

                self.degrees += random.randint(
                    int(self.phenotype['minturn'][0]),
                    int(self.phenotype['maxturn'][0]))
            if self.degrees >= 360:
                self.degrees -= 360
            elif self.degrees < 0:
                self.degrees = 360 - self.degrees
        #self.degrees -= 90

        speed = self.phenotype['speed'][0]
        xmove = math.cos(math.radians(self.degrees)) * speed / 100
        ymove = math.sin(math.radians(self.degrees)) * speed / 100
        if self.state == 'wander':
            self.moved += speed / 100
            if self.moved >= self.phenotype['forwardmove'][0]:
                self.moved = 0

        if self.x + xmove < 401 and self.x + xmove > -1:
            self.x += xmove
        else:
            xmove = 0
        if self.y + ymove < 401 and self.y + ymove > -1:
            self.y += ymove
        else:
            ymove = 0
        if self.focus == True:
            pass
        canvas.move(self.id, xmove, ymove)
        if debug == True:
            canvas.move(self.see, xmove, ymove)
            canvas.move(self.thirstbar, xmove, ymove)
            canvas.move(self.thirstfill, xmove, ymove)
            canvas.coords(self.thirstfill, self.x-10, self.y-10, \
                                                      self.x-10+self.thirst/5, self.y-15)
            canvas.move(self.thirstmark, xmove, ymove)
            canvas.move(self.hungerbar, xmove, ymove)
            canvas.move(self.hungerfill, xmove, ymove)
            canvas.coords(self.hungerfill, self.x-10, self.y-20, \
                                                      self.x-10+self.hunger/5, self.y-25)
            canvas.move(self.hungermark, xmove, ymove)
            canvas.move(self.matebar, xmove, ymove)
            canvas.move(self.matefill, xmove, ymove)
            canvas.coords(self.matefill, self.x-10, self.y-30, self.x-10+self.matecooldown*4, self.y-35)
            canvas.move(self.agebar, xmove, ymove)
            canvas.move(self.agefill, xmove, ymove)
            canvas.coords(self.agefill, self.x-10, self.y-40, self.x-10+self.age/3, self.y-45)

        if self.matecooldown > 0:
          self.matecooldown -= 0.01
        self.age += 0.01
        self.thirst -= speed / 1000 + vision / 1000
        self.hunger -= speed / 1000 + vision / 1000




        if self.age > 60 or self.thirst <= 0 or self.hunger <= 0 or self.dead == True:

          self.death()
        else:

          canvas.after(10, self.testmove)
    def procreate(self, other, amount):
      newgenes = other.genes
      otherhalfgene = []
      selfhalfgene = []
      for i in newgenes:
        otherhalfgene.append(random.choice(newgenes[i])+random.randint(-1*mutationrate, mutationrate))
      for i in self.genes:
        selfhalfgene.append(random.choice(self.genes[i])+random.randint(-1*mutationrate, mutationrate))
        
 
      
      fullgenome = {'speed': [selfhalfgene[0], otherhalfgene[0]],
                'vision': [selfhalfgene[1],
                          otherhalfgene[1]],
                'hunger tolerance':
                [selfhalfgene[2],
                          otherhalfgene[2]],
                'thirst tolerance':
                [selfhalfgene[3],
                          otherhalfgene[3]],
                'forwardmove': [selfhalfgene[4],
                          otherhalfgene[4]],
                'minturn': [selfhalfgene[5],
                          otherhalfgene[5]],
                'maxturn': [selfhalfgene[6],
                          otherhalfgene[6]]}
      l = creature(genesGiven=fullgenome, coords=[self.x, self.y, random.randint(0, 359)])
      l.hunger = 50 + (self.hunger - 50)/amount
      l.thirst = 50 + (self.thirst - 50)/amount
      self.hunger -= 10
      self.thirst -= 10
      
      
    def death(self):

        canvas.delete(self.id)
        if debug == True:
            canvas.delete(self.see)
            canvas.delete(self.thirstbar)
            canvas.delete(self.thirstfill)
            canvas.delete(self.thirstmark)
            canvas.delete(self.hungerbar)
            canvas.delete(self.hungerfill)
            canvas.delete(self.hungermark)
            canvas.delete(self.matebar)
            canvas.delete(self.matefill)
            canvas.delete(self.agebar)
            canvas.delete(self.agefill)
        canvas.coords(self.id, -10, -10, -10, -10)
        self.dead = True
        del creaturelist[self]
        del self




class Water():
    def __init__(self, coords, fill, offset=0, changeoffset=1):
        self.coords = coords
        self.fill = fill
        self.offset = offset
        self.coset = changeoffset
        self.x = self.coords[0]
        self.y = self.coords[1]
        self.id = canvas.create_oval(self.x - self.fill,
                                     self.y - self.fill,
                                     self.x + self.fill,
                                     self.y + self.fill,
                                     fill='blue')
        self.water = True
        waterlist.append(self)
        self.draw()

    def draw(self):
        self.fill = filled + self.offset
        if self.coset == -1:
          self.fill = 10-self.fill
        if self.fill > 0:
            self.water = True
            canvas.coords(self.id, self.x - self.fill, self.y - self.fill,
                          self.x + self.fill, self.y + self.fill)
        else:
          canvas.coords(self.id, -10, -10,
                          -10, -10)
          self.water = False
        canvas.tag_lower(self.id)
        canvas.after(10, self.draw)


class Food():
    def __init__(self, coords, rate, offset=0, changeoffset=1):
        self.coords = coords
        self.rate = rate
        self.offset = offset
        self.coset = changeoffset
        self.x = self.coords[0]
        self.y = self.coords[1]
        self.id = canvas.create_oval(self.x - 10,
                                     self.y - 10,
                                     self.x + 10,
                                     self.y + 10,
                                     fill='green')
        self.foodimage = canvas.create_oval(self.x - 5,
                                            self.y - 5,
                                            self.x + 5,
                                            self.y + 5,
                                            fill='red',
                                            outline='red')
        self.food = True
        self.time = rate+self.offset
        foodlist.append(self)
        self.grow()

    def grow(self):
        self.time -= 0.01

        if self.time <= 0:
            self.time = rate+self.offset
            if self.coset == -1:
                self.time = self.rate-self.time
            if self.time <= 0.5:
              self.time = 0.5
            if self.food == False:
                canvas.itemconfig(self.foodimage, fill='red', outline='red')
                self.food = True

        canvas.after(10, self.grow)

    def eaten(self):
        self.food = False
        canvas.itemconfig(self.foodimage, fill='green', outline='green')
        self.time = rate+self.offset
        if self.coset == -1:
            self.time = self.rate-self.time
        if self.time <= 0.5:
            self.time = 0.5

class Predator:
  def __init__(self, coords=None, behavior=None, strength=None, cooldown=None):
    self.coords = coords
    if coords == None:
      self.coords = [random.randint(0, 400), random.randint(0, 400), random.randint(0, 359)]
    self.x = self.coords[0]
    self.y = self.coords[1]
    self.degrees = self.coords[2]
    self.behavior = behavior
    if behavior == None:
      self.behavior = [random.randint(20, 100), random.randint(0, 359), random.randint(0, 359)]
    self.forwardmove = self.behavior[0]
    self.minturn = self.behavior[1]
    self.maxturn = self.behavior[2]
    self.strength = strength
    if strength == None:
      self.strength = [random.randint(50, 100), random.randint(50, 100)]
    self.speed = self.strength[0]
    self.vision = self.strength[1]
    self.cooldown = cooldown
    if cooldown == None:
      self.cooldown = random.randint(0, 20)
    self.cooldowntimer = random.randint(0, self.cooldown)
    self.moved = 0
    self.state = 'wander'
    predatorlist[self] = self
    self.killed = 0
    self.draw()
    self.move()
  def draw(self):
    self.id = canvas.create_oval(self.x-5, self.y-5, self.x+5, self.y+5, fill='grey')
    if debug == True:
        self.see = canvas.create_oval(self.x+self.vision, self.y+self.vision, self.x-self.vision, self.y-self.vision)
        self.killtime1 = canvas.create_rectangle(self.x - 10, self.y - 10, self.x + 10, self.y - 20, fill='grey')
        self.killtime2 = canvas.create_rectangle(self.x-10, self.y - 10, self.x-10+self.cooldowntimer, self.y-20, fill='red')

    
  def move(self):
    if self.state == 'wander':
      canvas.itemconfig(self.id, fill='grey')
    elif self.state == 'chase':
      canvas.itemconfig(self.id, fill='red')
    if self.cooldowntimer <= 0:
      k = False
      c = None
      b = None
      for i in creaturelist:
        if distance(self.x, self.y, i.x, i.y) <= 3:
          k = True
          c = i
        elif distance(self.x, self.y, i.x, i.y) <= self.vision:
          if b == None:
            b = i
          else:
            if b.phenotype['speed'][0] > i.phenotype['speed'][0]:
              b = i
      if k == True:
        creaturelist[c].dead = True
        
        

        self.cooldowntimer = self.cooldown
        self.state = 'wander'
        self.killed += 1
        

      elif b != None:
           
        self.degrees = math.degrees(
                    math.atan((b.y - self.y) / (b.x - self.x)))
        x1 = math.cos(math.radians(self.degrees)) * self.speed / 100
        y1 = math.sin(math.radians(self.degrees)) * self.speed / 100
        x1 += self.x
        y1 += self.y
        if distance(x1, y1, b.x, b.y) > distance(self.x, self.y, b.x, b.y):
            self.degrees += 180
        self.state = 'chase'
      if b == None:
        self.state = 'wander'
    if self.cooldowntimer > 0 or self.state == 'wander':
      if self.moved == 0:
        if self.minturn > self.maxturn:
          newminturn = self.minturn - 360
          self.degrees += random.randint(newminturn, self.maxturn)
        else:
          self.degrees += random.randint(self.minturn, self.maxturn)
    xmove = math.cos(math.radians(self.degrees)) * self.speed / 100
    ymove = math.sin(math.radians(self.degrees)) * self.speed / 100
    if self.state == 'wander':
        self.moved += self.speed / 100
        if self.moved >= self.forwardmove:
            self.moved = 0

    if self.x + xmove < 401 and self.x + xmove > -1:
        self.x += xmove
    else:
        xmove = 0
    if self.y + ymove < 401 and self.y + ymove > -1:
        self.y += ymove
    else:
        ymove = 0
    if self.cooldowntimer > 0:
      self.cooldowntimer -= 0.01
    canvas.move(self.id, xmove, ymove)
    if debug == True:
        canvas.move(self.see, xmove, ymove)
        canvas.move(self.killtime1, xmove, ymove)
        canvas.move(self.killtime2, xmove, ymove)
    
    
        if self.cooldown > 0:
          canvas.coords(self.killtime2, self.x-10, self.y - 10, self.x-10+self.cooldowntimer/self.cooldown*20, self.y-20)
        if self.cooldowntimer <= 0:
          canvas.itemconfig(self.killtime1, fill='#581112')
        else:
          canvas.itemconfig(self.killtime1, fill='grey')
    canvas.after(10, self.move)
  def death(self):
    canvas.delete(self.id)
    if debug == True:
        canvas.delete(self.see)
        canvas.delete(self.killtime1)
        canvas.delete(self.killtime2)
    del predatorlist[self]
    del self
    






      


process = False
f = open('Results.txt', 'w')
f.write("")
f.close()

def drought(length, actual):
    global process
    process = True
    global filled
    global rate
    if length > 0:
        
        filled -= 1
        
        rate += 0.8

        canvas.after(int(60/actual*1000), lambda: [drought(length-1, actual)])
    else:
      process = False


def flood(length, actual):
    global process
    process = True
    global filled
    global rate
    if length > 0:
        filled += 1

        rate -= 0.8
        canvas.after(int(60/actual*1000), lambda: [flood(length-1, actual)])
    else:
      process = False
r = 0
def showpopulation():
  global r
  f = open('Results.txt', 'a')
  f.write(str(len(creaturelist))+"\n")
  f.close()
  canvas.after(10000, showpopulation)

n = 600
v = 0
w = 60
p = 20
def startsim():
  global mutationrate
  g = input("Put in the mutation rate: ")
  while g.isdigit() == False:
    g = input("Put in the mutation rate: ")
  mutationrate = int(g)
  a = creature()
  b = creature()
  for x in range(0, 20):
    creature()
  d = Predator()
  Predator()
  Water([66, 150], filled, offset=10, changeoffset=-1)
  Water([152, 0], filled, offset=-5, changeoffset=-1)
  Water([152, 100], filled, offset=7)
  Water([152, 200], filled, offset=-5)
  Water([152, 300], filled, offset=1, changeoffset=-1)
  Water([152, 400], filled, offset=6, changeoffset=-1)
  Water([238, 250], filled, offset=-1)
  Water([324, 0], filled, offset=10, changeoffset=-1)
  Water([324, 200], filled, offset=2)
  Water([324, 400], filled)
  c = Food([200, 200], rate, offset=0.55)
  Food([150, 286], rate, offset=-0.43)
  Food([350, 182], rate, offset=-0.66, changeoffset=-1)
  Food([350, 40], rate, offset=-0.83, changeoffset=-1)
  Food([130, 317], rate, offset=0.69)
  Food([180, 302], rate, offset=0.37)
  Food([147, 175], rate, offset=-0.13, changeoffset=-1)
  Food([30, 130], rate, offset=0.3)
  Food([190, 119], rate, offset=-0.72, changeoffset=-1)
  Food([45, 329], rate, offset=-0.5, changeoffset=-1)
  showamountleft()
  showpopulation()
  timer()
  dochanges()
r = canvas.create_text(5, 5, text='0', font=('Arial', 20), fill='red', anchor=NW)
u = canvas.create_text(5, 25, text='22', font=('Arial', 20), fill='blue', anchor=NW)
def showamountleft():
    global u
    canvas.itemconfig(u, text=str(len(creaturelist)))
    canvas.tag_raise(u)
    canvas.after(10, showamountleft)
def timer():
  global r
  global n
  if n > 0:
    n -= 1
    canvas.itemconfig(r, text=str(600-n))
    canvas.tag_raise(r)

    canvas.after(1000, timer)
  else:
    
    quit()
def dochanges():
  global v
  global w
  global p
  if w > 0:
    w -= 1
  else:
    eval(changelist[v])
    v += 1
    if v > len(changelist)-1:
      v = 0
    w = 60
  if p > 0:
    p -= 1
  else:
    
    a = len(creaturelist)
    while len(predatorlist) != (a - a % 10) / 10:
      a = len(creaturelist)
      if len(predatorlist) < (a - a % 10) / 10:
        Predator()
      elif len(predatorlist) > (a - a % 10) / 10:
        b = None
        for i in predatorlist:
          if b == None:
            b = i
          else:
            if b.killed < i.killed:
              b = i
      
        b.death()
      
    p = 20
    
    
      
  canvas.after(1000, dochanges)


startsim()
    
  
  
    


#drought(10)

#flood(10)
