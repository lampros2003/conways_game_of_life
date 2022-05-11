# Python code to implement Conway's Game Of Life
import argparse
from asyncore import loop
from cProfile import label
from distutils.command.config import config
from msilib.schema import Billboard
from multiprocessing.connection import wait
from pickle import TRUE
from random import randint
from sre_parse import State
from textwrap import fill
from time import sleep
from tkinter import BOTH, BOTTOM, RIGHT, Button, Entry, Frame, Label, StringVar, Tk
from tokenize import Octnumber
from traceback import FrameSummary
from turtle import color, right
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sympy import false, root, true
import pygame
def changecol(d,i,j):
    d[i-2][j-1]=30

class cell():
    
    def __init__(self):
        self.state = 0
    def isalive(self,*args):
        count = 0 
        for i in args:
            count += i.state
        if count < 2 or count>4:
            self.state = 0
        elif count == 3:
            self.state = 1
    def changestate(self):
        self.state = not (self.state)
    
    def __repr__(self) -> str:
        return str(self.state)
        
    def __str__(self) -> str:
        return str(self.state)
    def colour(self):
        if self.state:
            return "blue"
        else:return "white"
class conwaysboard():
    def __init__(self,n) -> None:
        self.n = n
        self.board = [[cell() for i in range(n+1)] for i in range(n+1)]
        state = [[i.state for i in j] for j in self.board]
        self.state = np.array(state)
    def update(self):
        i=1
        j=1
        while i < self.n-1:
            while j < self.n-1:
            
                self.board[i][j].isalive( self.board[i-1][j], self.board[i+1][j], self.board[i+1][j+1], self.board[i-1][j-1], self.board[i][j+1], self.board[i][j-1], self.board[i+1][j-1], self.board[i-1][j+1])
                j+=1
            i+=1
        state = [[i.state for i in j] for j in self.board]
        self.state = np.array(state)
    def randomize(self):
        for i in range(1,self.n):
            for j in  range(1,self.n) :
                self.board[i][j].state= randint(0,1)
                state = [[i.state for i in j] for j in self.board]
                self.state = np.array(state)
class conwindow():
    
    def __init__(self,wind,board) -> None:
        c1=0
        d = [[] for x in range(board.n)]
        self.d =d
        for i in range(board.n):
            for j in range(board.n):
                self.d[i].append(Label(wind,text=board.board[i][j]))
                self.d[i][j].bind("<Button-1>",lambda event : changecol(d,i,j))
                self.d[i][j].grid(row = i ,column = j)

            c1+=1

    def update(self,wind,board):
        c1=0
        d = [[] for x in range(board.n)]

        for i in range(board.n):
            for j in range(board.n):
                self.d[i][j].config(text=board.board[i][j])
            c1+=1

b = conwaysboard(5)

b.randomize()
while true:
    b.update()
    print(b.board)
    sleep(2)