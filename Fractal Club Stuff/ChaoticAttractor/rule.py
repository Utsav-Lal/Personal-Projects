import math

def rule(state):  # take in the previous state, return the values you want to use as the color/position as a list and the new state
    sigma = 10
    rho = 28
    beta = 8/3
    timestep = 0.01
    dx = sigma*(state[1]-state[0])
    dy = state[0]*(rho-state[2])-state[1]
    dz = state[0]*state[1]-beta*state[2]
    newstate = [state[0]+dx*timestep, state[1]+dy*timestep, state[2]+dz*timestep]
    return newstate[0:2], newstate

def linscale(x,y):  # scaling of values
    return x*10+200, y*10+200

def initstate(x, y):  # set initial values of unseen state variables
    newx, newy = linscale(x, y)
    return [newx, newy, 0]

def firststate():  # first state for attractor
    return [1, 1, 1]
