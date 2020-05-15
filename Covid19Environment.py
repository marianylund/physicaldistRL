from MovableObj import MovableObj
import numpy as np
from random import randint
from graphics import *
import math
import traceback
import sys
import enum 

class Covid19Environment():
    reward = 0
    visited_kiwi = False

    def __init__(self):
        try:
            self.win = GraphWin('Floor', 500, 500)
            self.win.setCoords(0.0, 0.0, 10.0, 10.0)
            self.win.setBackground("blue4")

            self.draw_grid()
            self.add_house()
            self.add_kiwi()
            self.add_survivor()
            
            self.listen_for_keys()   
            self.win.close()
        except Exception:
            print("Ooops, something is wrong")
            print(traceback.format_exc())
            if self.win != None:    
                self.win.close()
        
    def listen_for_keys(self):
        while True:
            k = self.win.checkKey()

            if k == 'Left':
                self.do_action(0)
                self.calculate_rewards(self.get_state())
            elif k == 'Right':
                self.do_action(1)
                self.calculate_rewards(self.get_state())
            elif k == 'Up':
                self.do_action(2)
                self.calculate_rewards(self.get_state())
            elif k == 'Down':
                self.do_action()
                self.calculate_rewards(self.get_state())
            elif k == 'period':
                break
                  
        
    def draw_grid(self):
        print("PlottingGrid")
        for x in range(10):
            for y in range(10):
                self.win.plotPixel(x*50, y*50, "yellow")
        print("FinishedPlotting")
    
    def add_house(self):
        print("add_house")
        
        self.housePos = [0, 0]
        house = Rectangle(Point(0,0), Point(1,1))
        house.draw(self.win)
        house.setFill("brown")
        print("add_house")
    
    def add_survivor(self):
        print("add_survivor")
        self.survivor = MovableObj(self.win)
        print("add_survivor")
        
    def add_kiwi(self):
        print("add_kiwi")
        
        self.kiwiPos = [9, 9]
        kiwi = Rectangle(Point(9,9), Point(10, 10))
        kiwi.draw(self.win)
        kiwi.setFill("green")
        print("add_kiwi")
    
    def reset_environment(self):
        self.survivor.restart()
    
    def get_state(self):
        state_body_vis = self.survivor.get_body_vis_state([self.kiwiPos, self.housePos])
        print("State: ", state_body_vis)
        enum_state = [self.convert_to_state(state_body_vis[0]), self.convert_to_state(state_body_vis[1])]
        print(enum_state)
        return enum_state

    def convert_to_state(self, stateNum, lenOfObj = 2):
        if stateNum >= lenOfObj:
            return States.NOTHING
        elif stateNum > 1:
            return States.SOMEONE
        else:
            return States(stateNum)
    
    def do_action(self, num = -1):
        if num == -1:
            # Do random choice
            num = randint(0, 2)
        if num == 0:
            self.survivor.look_left()
        elif num == 1:
            self.survivor.look_left(True)
        elif num == 2:
            self.survivor.move_forward()
        else:
            print("Something is wrong when doing an action: ", num)

        self.reward -= 1
        print(self.reward)
    
    def calculate_rewards(self, enum_state):
        if enum_state[0].value == 1:
            self.reward += 5
            print("Ending reward: ", self.reward)
            self.win.close()
            sys.exit()
        elif enum_state[0].value == 0:
            print("Standing on KIWI")
            if not self.visited_kiwi:
                print("Kiwi visited")
                self.reward += 30
                self.visited_kiwi = True
        elif enum_state[0].value == 2:
            print("Oh, no, another person")
            self.reward -= 10









class States(enum.Enum): 
    KIWI = 0
    HOUSE = 1
    SOMEONE = 2
    NOTHING = 3
    BORDER = 4
