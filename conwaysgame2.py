from multiprocessing.reduction import steal_handle
from pickle import TRUE
from tkinter import Y
from turtle import width
import numpy as np
import matplotlib.pyplot as plt
from sympy import Transpose, div, false, true


def GosperGliderGun(height, width):
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


def gunatpos(state, i, j, bigrotate=False, rotate=False, xsym=False, ysym=False,allsym=False):
    # minimum sizeof gun
    gun = GosperGliderGun(38, 38)
    # put gun inside of state
    if rotate:

        newgun = rot90gun(gun)
        #gun = orientedgun(newgun)
        state[i:i+38, j:j+38] = newgun
        return

    elif ysym:
        gun = np.flip(gun, 1)
        state[i:i+38, j:j+38] = gun
        return
    elif allsym:
        gun = np.flip(gun, 0)
        gun = np.flip(gun, 1)
        state[i:i+38, j:j+38] = gun
        return
    elif bigrotate:
        newgun = np.rot90(gun)
        newgun = np.rot90(newgun)
        state[i:i+38, j:j+38] = newgun
        return

    elif xsym:
        newgun = flipedgun(gun)
        state[i:i+38, j:j+38] = newgun
        return
    else:

        state[i:i+38, j:j+38] = gun
        return

def permbistableswitch(state,r,c,inp=0):

    n = """.OO........................................................
..O........................................................
.O.........................................................
.OO...............................................OO.......
...................................................O.......
..................................................O........
..................................................OO.......
..................................O........................
..................................O.O......................
O...OO............................OO.......................
OO..OO.....................................................
.OO......................OO................................
OO.......................OO..........................OO....
.....................................................OO....
...........................................................
...........................................................
...........................................................
...........................................................
.............OO............................................
............O.O........OO..................................
..............O.......O.O..................................
......................O....................................
.....................OO.........................OO.........
................................................OO.........
...........................................................
...........................................................
..................................OO.....................OO
...................................O......................O
................................OOO....................OOO.
................................O......................O...
............................................OO.............
............................................O..............
.............................................OOO...........
...............................................O..........."""
    ar = []
    count = 0
    for i in n.split("\n"):
        print(i+":", end="")
        ar.append([])
        for j in i:
            if j == "O":
                ar[count].append(1)
            else:
                ar[count].append(0)
        
        count += 1
    ar = np.array(ar)
    state[r:r+34, c:c+59] = ar

    
                
def eater():
    eater = np0zeros(4*4).reshape(4, 4)
    eater[0][0] = 1
    eater[0][1] = 1
    eater[1][0] = 1
    eater[1][2] = 1
    eater[2][2] = 1
    eater[3][2] = 1
    eater[3][3] = 1
    return eater


def cutter(flip=False, length=10):
    cutter = np.zeros(100*100).reshape(100, 100)
    cutter[0:38, 0:38] = GosperGliderGun(38, 38)
    cutter[15+length:19+length, 29+length:33+length] = eater()
    if flip:
        cutter = np.flip(cutter, 1)
    return cutter
# makes +60 period gun into +30 period gun
# can serve as a logic clock pulse
# can be used to make a logic clock of varying frequency by adding many in series


def periodicdivisor(state, i, j, down=False):
    if not down:
        gunatpos(state, i, j)
        gunatpos(state, i+20, j+11, rotate=True)
    else:
        gunatpos(state, i, j)
        gunatpos(state, i+25, j+16, rotate=True)

# better than  not gate example


def notgate(state, i, j, inp=0):
    if inp:
        gunatpos(state, i, j)
    periodicdivisor(state, i+90, j+30)
# equivalenet to not gate
# better than initial not gate
# better than my first not gate,best gate?


def periodicnulifierwithinput(state, i, j, inp=0):
    if inp:
        gunatpos(state, i, j)
    gunatpos(state, i+20, j+12, rotate=True)


def andgate(state, i, j, inp=1, inp2=1):

    state[i+30:i+130, j+40:j+140] = cutter(flip=True, length=60)
    if inp2:
        gunatpos(state, i, j+15)
    if inp:
        gunatpos(state, i+21, j)

        # periodicdivisor(state,i+21,j,down=True)


def orgate(state, i, j, inp=0, inp2=0):
    #state[i+30:i+130,j+40:j+140] = cutter(flip= True,length=60)
    gunatpos(state, i, j)
    if inp:
        state[i:i+100, j+40:j+140] = cutter(length=60)
    if inp2:
        gunatpos(state, i, j+100)
    gunatpos(state, i, j+145, ysym=True)

def latch(state,i,j,set =0 ,reset=0):
    l = 30
    
    gunatpos(state,i+l,j+l)
    gunatpos(state,i+l,j+l+37,ysym= True)
    gunatpos(state,i+60,j+30,rotate=True)

    
    
    
def clock(state):
    periodicdivisor(state, 0, 10,down=True)
    periodicdivisor(state, 70, 0, )

class Board():
    def __init__(self, size, seed="or"):
        if seed == 'Random':
            self.state = np.random.randint(2, size=size)
            print(type(self.state))

        if seed == "perkin":
            self.state = np.zeros(100*100).reshape(100, 100)
            permbistableswitch(self.state,20,15)
        elif seed == "clock":
            self.state = np.zeros(250*250).reshape(250, 250)
            clock(self.state)
        elif seed == "or":
            self.state = np.zeros(250*250).reshape(250, 250)
            orgate(self.state, 0, 0)

        elif seed == 'and':
            self.state = np.zeros(250*250).reshape(250, 250)
            andgate(self.state, 4, 4)
        elif seed == "not":
            self.state = np.zeros(100*100).reshape(100, 100)
            periodicnulifierwithinput(self.state, 4, 4, inp=0)
        elif seed == "tgun":
            self.state = np.zeros(100*100).reshape(100, 100)
            gunatpos(self.state, 10, 10, transpose=True)
        elif seed == "Gun":
            self.state = GosperGliderGun(size, size)
        elif seed == "eat":
            self.state = np.zeros(10*10).reshape(10, 10)
            eater(self.state, 3, 3)
        elif seed == "div":
            self.state = np.zeros(100*100).reshape(100, 100)
            periodicdivisor(self.state, 10, 10)
        elif seed == "latch":
            self.state = np.zeros(200*200).reshape(200, 200)
            latch(self.state,10,10)
        self.engine = Engine(self)
        self.iteration = 0

    def animate(self):
        i = self.iteration
        im = None
        plt.title("Conway's Game of Life")
        while True:
            if i == 0:
                plt.ion()
                im = plt.imshow(self.state, vmin=0, vmax=2, cmap=plt.cm.gray)
            else:
                im.set_data(self.state)
            i += 1
            self.engine.applyRules()
            plt.pause(0.01)
            yield self


class Engine():
    def __init__(self, board):
        self.state = board.state

    def countNeighbors(self):
        state = self.state

        n = (state[0:-2, 0:-2] + state[0:-2, 1:-1] + state[0:-2, 2:] +
             state[1:-1, 0:-2] + state[1:-1, 2:] + state[2:, 0:-2] +
             state[2:, 1:-1] + state[2:, 2:])

        return n

    def applyRules(self):
        n = self.countNeighbors()
        state = self.state
        birth = (n == 3) & (state[1:-1, 1:-1] == 0)
        survive = ((n == 2) | (n == 3)) & (state[1:-1, 1:-1] == 1)
        state[...] = 0
        state[1:-1, 1:-1][birth | survive] = 1
        nBirth = np.sum(birth)
        self.nBirth = nBirth
        nSurvive = np.sum(survive)
        self.nSurvive = nSurvive
        return state


def main():

    board = Board(38, seed="latch")
    for i in board.animate():
        pass


if __name__ == '__main__':
   main()

