from pickle import TRUE
from tkinter import Y
from turtle import width
import numpy as np
import matplotlib.pyplot as plt

import argparse
import time

from sympy import Transpose, div, false, true
def GosperGliderGun(height,width):
    gun = np.zeros(height*width).reshape(height, width)
    gun[5][1] = gun[5][2] = 1
    gun[6][1] = gun[6][2] = 1
    gun[3][13] = gun[3][14] = 1
    gun[4][12] = gun[4][16] = 1
    gun[5][11] = gun[5][17] = 1
    gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 1
    gun[7][11] = gun[7][17] = 1
    gun[8][12] = gun[8][16] = 1
    gun[9][13] = gun[9][14] = 1
    gun[1][25] = 1
    gun[2][23] = gun[2][25] = 1
    gun[3][21] = gun[3][22] = 1
    gun[4][21] = gun[4][22] = 1
    gun[5][21] = gun[5][22] = 1
    gun[6][23] = gun[6][25] = 1
    gun[7][25] = 1
    gun[3][35] = gun[3][36] = 1
    gun[4][35] = gun[4][36] = 1   
    return gun
def orientedgun(gun):
    
    newgun = gun.T
    return newgun
def rot90gun(gun):
    
    newgun = np.rot90(gun)
    return newgun
def flipedgun(gun):
    newgun = np.flip(gun)
    return newgun
def gunatpos(state,i,j,bigrotate = False,rotate=False,xsym=False):
    #minimum sizeof gun
    gun = GosperGliderGun(38,38)
    #put gun inside of state 
    if rotate:
        
        newgun = rot90gun(gun)
        #gun = orientedgun(newgun)
        state[i:i+38, j:j+38] = newgun
    elif bigrotate:
        newgun = np.rot90(gun)
        newgun = np.rot90(newgun)
        state[i:i+38, j:j+38] =newgun
       
    elif xsym:
        newgun = flipedgun(gun)
        state[i:i+38, j:j+38] = newgun
    else:
        
        state[i:i+38, j:j+38] = gun
    

def eater():
    eater = np.zeros(4*4).reshape(4,4)
    eater[0][0]=1
    eater[0][1]=1
    eater[1][0]=1
    eater[1][2]=1
    eater[2][2]=1
    eater[3][2]=1
    eater[3][3] = 1
    return eater
def cutter(flip=False,length=10):
    cutter = np.zeros(100*100).reshape(100,100)
    cutter[0:38,0:38] = GosperGliderGun(38,38)
    cutter[15+length:19+length,29+length:33+length] = eater()
    if flip:
        cutter = np.flip(cutter,1)
    return cutter
#makes +60 period gun into +30 period gun
def periodicdivisor(state,i,j,rotate=False):
    gunatpos(state,i,j)
    gunatpos(state,i+20,j+11,rotate=True)
#better than  not gate example
def notgate(state,i,j,inp=0):
    if inp:
        gunatpos(state,i,j)
    periodicdivisor(state,i+90,j+30)
#equivalenet to not gate
#better than initial not gate
#better than my first not gate,best gate?
def periodicnulifierwithinput(state,i,j,inp = 0 ):
    if inp:
        gunatpos(state,i,j)
    gunatpos(state,i+20,j+12,rotate=True)
    
def orgate(state,i,j,inp = 1 ,inp2 = 1):
    
    
    state[i+30:i+130,j+40:j+140] = cutter(flip= True,length=60)
    if inp2:
        gunatpos(state,i,j+15)
    if inp:
        gunatpos(state,i+21,j)
    


class Board(object):
   def __init__(self, size, seed = "or"):
      if seed == 'Random':
         self.state = np.random.randint(2, size = size)
         print(type(self.state))

      elif seed == 'or':
          self.state  =  np.zeros(250*250).reshape(250,250)
          orgate(self.state,4,4)
      elif seed == "not":
          self.state  =  np.zeros(100*100).reshape(100,100)
          periodicnulifierwithinput(self.state,4,4,inp=1)
      elif seed == "tgun":
          self.state  =  np.zeros(100*100).reshape(100,100)
          gunatpos(self.state,10,10 ,transpose=True)
      elif seed == "Gun":
          self.state  =  GosperGliderGun(size,size)
      elif seed == "eat":
          self.state = np.zeros(10*10).reshape(10,10)
          eater(self.state,3,3)
      elif seed == "div":
          self.state  =  np.zeros(100*100).reshape(100,100)
          periodicdivisor(self.state,10,10)
      self.engine = Engine(self)
      self.iteration = 0
   def animate(self):
      i = self.iteration
      im = None
      plt.title("Conway's Game of Life")
      while True:
         if i == 0:
            plt.ion()
            im = plt.imshow(self.state, vmin = 0, vmax = 2, cmap = plt.cm.gray)
         else:
            im.set_data(self.state)
         i += 1
         self.engine.applyRules()
         #print('Life Cycle: {} Birth: {} Survive: {}'.format(i, self.engine.nBirth, self.engine.nSurvive))
         plt.pause(0)
         yield self
         


class Engine(object):
   def __init__(self, board):
      self.state = board.state
   def countNeighbors(self):
      state = self.state
      n = (state[0:-2,0:-2] + state[0:-2,1:-1] + state[0:-2,2:] +
          state[1:-1,0:-2] + state[1:-1,2:] + state[2:,0:-2] +
          state[2:,1:-1] + state[2:,2:])
      return n
    
   def applyRules(self):
      n = self.countNeighbors()
      state = self.state
      birth = (n == 3) & (state[1:-1,1:-1] == 0)
      survive = ((n == 2) | (n == 3)) & (state[1:-1,1:-1] == 1)
      state[...] = 0
      state[1:-1,1:-1][birth | survive] = 1
      nBirth = np.sum(birth)
      self.nBirth = nBirth
      nSurvive = np.sum(survive)
      self.nSurvive = nSurvive
      return state
def main():
   
   """ bHeight = int(input("height"))
   bWidth = int(input("width")) """
   board = Board((100))
   for _ in board.animate():
      pass

if __name__ == '__main__':
   main()