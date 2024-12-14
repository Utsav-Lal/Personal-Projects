import random
import math

# Activation function (Relu)
def activation(inp):
  if inp <= 0:
    return 0
  return inp

# Derivative of activation function
def dActivation(inp):
  if inp <= 0:
    return 0
  return 1

def minmax(inp):
  return 2/(1+math.exp(-8*inp))-1
def dminmax(inp):
  return 2*8*minmax(inp)*(1-minmax(inp))

# creates the weights randomly
def createWeights(ranges, amount, dense):
  weightlist = []
  for x in range(amount):
    weightlist.append(
      random.randint(-dense*ranges, dense * ranges) / dense)
  return weightlist

class Network:
  def __init__(self, inputs, layers, layerSize, outputs):
    self.inputList = [] # Input interface
    self.networkList = [] # List of all neurons
    self.outputList = [] # output neuron to read
    self.lRate = 0.1 # learning rate
    self.rang = 1 # range of weights (-self.rang - self.rang)
    self.density = 100 # "preciseness" of weights
    

    self.networkList = [[]]

    # creates input neurons
    for x in range(inputs):
      self.networkList[0].append(Node(x, inp=x))
      self.networkList[0][x].initializeWeights(createWeights(self.rang, layerSize, self.density))
      self.inputList.append(0)

    # creates first layer bias
    self.networkList[0].append(Node(inputs, bias=True))
    self.networkList[0][inputs].initializeWeights(createWeights(self.rang, layerSize, self.density))

    # creates hidden neurons
    for x in range(1, layers):
      self.networkList.append([])
      # creates hidden neurons of 1 layer
      for y in range(layerSize):
        self.networkList[x].append(Node(y))
        self.networkList[x][y].initializeWeights(createWeights(self.rang, layerSize, self.density))
        self.networkList[x][y].initializeBack(self.networkList[x - 1])
      # creates hidden biases
      self.networkList[x].append(Node(layerSize, bias=True))
      self.networkList[x][layerSize].initializeWeights(createWeights(self.rang, layerSize, self.density))
      # sets the frontlist of the neuron layer behind to the current layer
      for i in self.networkList[x - 1]:
        i.initializeFront(self.networkList[x])

    # creates last layer hidden neurons
    self.networkList.append([])
    for x in range(layerSize):
      self.networkList[layers].append(Node(x))
      self.networkList[layers][x].initializeWeights(createWeights(self.rang, outputs, self.density))
      self.networkList[layers][x].initializeBack(self.networkList[layers - 1])

    # creates last bias
    self.networkList[layers].append(Node(layerSize, bias=True))
    self.networkList[layers][layerSize].initializeWeights(createWeights(self.rang, outputs, self.density))
    for i in self.networkList[layers - 1]:
      i.initializeFront(self.networkList[layers])

    # creates output neuron
    for x in range(outputs):
      self.outputList.append(Node(x))
      self.outputList[x].initializeBack(self.networkList[layers])
      for i in (self.networkList[layers]):
        i.initializeFront(self.outputList)



  # starts backpropogation - calculates loss, then updates weights
  def BackPropogate(self, expected):
    for x in range(len(expected)):
      self.outputList[x].calculateLoss(expected[x], self.lRate)
    for x in range(len(self.networkList) - 1, -1, -1):
      for i in self.networkList[x]:
        i.calculateLoss(expected, self.lRate)
      for i in self.networkList[x]:
        i.updateWeights(self.lRate)

  def forwardPropogate(self, inputList):
    self.inputList = inputList
    a = []
    for i in self.outputList:
      a.append(i.forwardPropogate(self.inputList))
    return a

  def inputLoss(self, expected):
    for x in range(len(expected)):
      self.outputList[x].calculateLoss(expected[x], self.lRate)
    for x in range(len(self.networkList) - 1, -1, -1):
      for i in self.networkList[x]:
        i.calculateLoss(expected, self.lRate)
    a = []
    for i in self.networkList[0]:
      a.append(i.loss)
    return a


# Makes a Neuron
class Node:
  def __init__(self, pos, inp=None, bias=False):
    self.pos = pos # position of neuron in layer
    self.weightList = [] # weights in front of neuron
    self.frontList = [] # neurons in front
    self.backList = [] # neurons behind
    self.input = inp # position input Neuron (if input neuron)
    self.bias = bias # Neuron is bias or not
    self.output = 0 # Last output of neuron
    self.loss = None # Last loss of neuron

  # initializes weightlist
  def initializeWeights(self, weightList):
    self.weightList = weightList

  # initializes frontlist
  def initializeFront(self, frontList):
    self.frontList = frontList

  # intializes backlist
  def initializeBack(self, backList):
    self.backList = backList

  # does forwardpropogation on the node
  def forwardPropogate(self, inputList):
    if self.bias: # return 1 if bias
      self.output = activation(1)
      return self.output
    elif self.input != None: # return the activation of its input if input Neuron
      self.output = activation(inputList[self.input])
      return self.output
    else:
      self.output = 0
      # collects the outputs of the previous neurons
      for i in self.backList:
        self.output += i.forwardPropogate(inputList) * i.weightList[self.pos]
      self.output = activation(self.output)
      return self.output

  # calculates loss for backpropogation
  def calculateLoss(self, frontExpected, lRate):
    self.loss = 0
    if len(self.frontList) == 0: # expected-output if output neuron
      self.loss = (frontExpected - self.output)
    else:
      # Adds up the loss of all the forward neurons times the weight connecting it
      for x in range(len(self.weightList)):
        self.loss += self.weightList[x] * self.frontList[x].loss * dActivation(
          self.output)

  # updates the weights
  def updateWeights(self, lRate):
    for x in range(len(self.weightList)):
      self.weightList[x] += lRate * self.output * self.frontList[x].loss




def initializeNetwork(inputs, layers, layerSize):

  self.networkList = [[]]

  # creates input neurons
  for x in range(inputs):
    self.networkList[0].append(Node(x, inp=x))
    self.networkList[0][x].initializeWeights(createWeights(1,layerSize, 100))
    self.inputList.append(0)

  # creates first layer bias
  self.networkList[0].append(Node(inputs, bias=True))
  self.networkList[0][inputs].initializeWeights(createWeights(1, layerSize, 100))

  # creates hidden neurons
  for x in range(1, layers):
    self.networkList.append([])
    # creates hidden neurons of 1 layer
    for y in range(layerSize):
      self.networkList[x].append(Node(y))
      self.networkList[x][y].initializeWeights(createWeights(1, layerSize, 100))
      self.networkList[x][y].initializeBack(self.networkList[x - 1])
    # creates hidden biases
    self.networkList[x].append(Node(layerSize, bias=True))
    self.networkList[x][layerSize].initializeWeights(createWeights(1, layerSize, 100))
    # sets the frontlist of the neuron layer behind to the current layer
    for i in self.networkList[x - 1]:
      i.initializeFront(self.networkList[x])

  # creates last layer hidden neurons
  self.networkList.append([])
  for x in range(layerSize):
    self.networkList[layers].append(Node(x))
    self.networkList[layers][x].initializeWeights(createWeights(1, 1, 100))
    self.networkList[layers][x].initializeBack(self.networkList[layers - 1])

  # creates last bias
  self.networkList[layers].append(Node(layerSize, bias=True))
  self.networkList[layers][layerSize].initializeWeights(createWeights(1, 1, 100))
  for i in self.networkList[layers - 1]:
    i.initializeFront(self.networkList[layers])

  # creates output neuron
  self.outputNode = Node(0)
  self.outputNode.initializeBack(self.networkList[layers])
  for i in (self.networkList[layers]):
    i.initializeFront([self.outputNode])







# Test case - rating sandwiches - input as xxxxxxxx - x is 1 or 0
# 1 means ingredient in sandwich, 0 otherwise
# Ingredients:
# PB, J, Mud, Cheese, Lettuce, Tomato, Nutella
def TrainSandwich():
  k = Network(7, 2, 20, 1)
  yes = 0
  no = 0
  x = 0
  while (x < 2000):
    inputs = []
    if (not random.randint(0, 5) == 0):
      for y in range(7):
        inputs.append(random.randint(0, 1))
    else:
      inputs = [0, 0, 0, 0, 0, 0, 0]
    k.inputList = inputs
    if k.inputList[2]:
      if (yes >= no):
        k.forwardPropogate(inputs)
        k.BackPropogate([0])
        no += 1
        x += 1
        continue

    elif (k.inputList[0] or k.inputList[1]) and (k.inputList[3] or k.inputList[4] or k.inputList[5]):
      if (yes >= no):
        k.forwardPropogate(inputs)
        k.BackPropogate([0])
        no += 1
        x += 1
        continue
    elif k.inputList != [0, 0, 0, 0, 0, 0, 1] and k.inputList[6]:
      if (yes >= no):
        k.forwardPropogate(inputs)
        k.BackPropogate([0])
        no += 1
        x += 1
        continue
    elif max(k.inputList) == 0:
      if (yes >= no):
        k.forwardPropogate(inputs)
        k.BackPropogate([0])
        no += 1
        x += 1
        continue
    else:
      
      if (no >= yes):
        k.forwardPropogate(inputs)
        k.BackPropogate([1])
        yes += 1
        x += 1
        continue
  return k
def GenerateSandwich():
  j = Network(1, 2, 10, 7)
  k = TrainSandwich()
  for x in range(0, 2000):
    r = j.forwardPropogate([random.randint(0, 1000)/1000])
    t = []
    for i in r:
      t.append(minmax(i))

    k.forwardPropogate(t)
    l = k.inputLoss([1])
    for x in range(len(j.outputList)):
      j.outputList[x].loss = dminmax(activation(t[x]))*dActivation(t[x])*l[x]
    for x in range(len(j.networkList) - 1, -1, -1):
      for i in j.networkList[x]:
        i.calculateLoss(1, j.lRate)
      for i in j.networkList[x]:
        i.updateWeights(j.lRate)
  r = j.forwardPropogate([1])
  t = []
  p = []
  print(r)
  for i in r:
    p.append(minmax(i))
  print(p)
  for a in p:
    if (a >= 0.5):
      t.append(1)
    else:
      t.append(0)

  print(t)
  print(k.forwardPropogate(t))
def Sandwich():
  k = TrainSandwich()
  while True:
    inputListString = input(":")
    for x in range(len(k.inputList)):
      k.inputList[x] = int(inputListString[x])

    print(k.forwardPropogate(k.inputList))

for x in range(0, 10):
  GenerateSandwich()
#Sandwich()
