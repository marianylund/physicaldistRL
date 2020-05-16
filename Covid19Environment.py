from MovableObj import GraphicMovableObj, MovableObj
import numpy as np
from random import randint
import random
from graphics import *
import math
import traceback
import sys
import enum 

class States(enum.Enum): 
    NOTHING = 0
    HOUSE = 1
    SOMEONE = 2
    KIWI = 3
    BORDER = 4

class Actions(enum.Enum): 
    LEFT = 0
    RIGHT = 1
    FORWARD = 2

class Covid19Environment():
    
    have_been_to_kiwi = False
    total_actions = 0
    random_actions = 0

    def __init__(self, q_table, epsilon, random_others, world_size = (5, 5), learning_rate = 0.7, discount_rate = 0.618):
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.epsilon = epsilon
        
        self.world_size = world_size
        self.environment_table = np.zeros(world_size, dtype = int)
        self.environment_table[0][0] = States.HOUSE.value
        
        for other_pos in random_others:
            self.environment_table[other_pos[0]][other_pos[1]] = States.SOMEONE.value
        
        self.environment_table[world_size[0]-1][world_size[1]-1] = States.KIWI.value
        self.q_table = q_table
        start_pos = [math.floor(world_size[0]/2), math.floor(world_size[1]/2)]
        self.survivor = MovableObj(start_pos)
        #print("vision: ", self.survivor.get_vision_pos())
        #print("direction: ", self.survivor.states[survivor.currentState]) 

    def is_within_bounds(self, pos):
        return pos[0] < self.world_size[0] and pos[1] < self.world_size[1] and pos[0] >= 0 and pos[1] >= 0

    def get_stand_state(self, stand_pos):
        if not self.is_within_bounds(stand_pos):
            return 4
        return self.environment_table[stand_pos[0]][stand_pos[1]]

    def get_see_state(self, see_pos):
        if not self.is_within_bounds(see_pos):
            return 4
        return self.environment_table[see_pos[0]][see_pos[1]]

    def get_state(self, stand_pos, see_pos):
        return self.get_stand_state(stand_pos), self.get_see_state(see_pos)

    def get_possible_actions_from_state(self, state):
        possible_actions = []
        for i in range(3):
            if(self.q_table[state[0]][state[1]][i] != -math.inf):
                possible_actions.append(i)
        return possible_actions

    def get_max_value_from_state(self, state):
        return max(self.q_table[state[0]][state[1]])

    def calculate_reward(self, state):
        if state[0] == States.NOTHING.value:
            return -1, False
        elif state[0] == States.SOMEONE.value:
            return -10, False
        elif state[0] == States.KIWI.value:
            if self.have_been_to_kiwi:
                return 0, False
            else:
                self.have_been_to_kiwi = True
                return 50, False
        elif state[0] == States.HOUSE.value:
            if self.have_been_to_kiwi:
                #print("Wooow! House reached after Kiwi!")
                return 200, True
            else:
                #print("House reached")
                return 30, True
            
            return 10, True
        elif state[0] == States.BORDER.value:
            print("Out of the border.")
            return -1000, True
        else:
            print("Something is wrong: ", state)

    def step(self):
        current_state = self.get_state(self.survivor.get_body_pos(), self.survivor.get_vision_pos())
        #print("current_state: ", current_state)
        possible_actions = self.get_possible_actions_from_state(current_state)
        #print("possible_actions: ", possible_actions)

        exp_exp_tradeoff = random.uniform(0,1)
        if exp_exp_tradeoff > self.epsilon:
            action_to_choose = np.argmax(self.q_table[current_state[0],current_state[1],:])
        else:
            action_to_choose = random.choice(possible_actions)
            self.random_actions += 1
        
        #print("old_pos: ", self.survivor.get_body_pos(), self.survivor.get_vision_pos())
        #print("Action chosen: ", Actions(action_to_choose))
        self.survivor.do_action(action_to_choose)
        
        new_state = self.get_state(self.survivor.get_body_pos(), self.survivor.get_vision_pos())
        #print("new_pos: ", self.survivor.get_body_pos(), self.survivor.get_vision_pos())
        #print("new_state: ", States(new_state[0]), States(new_state[1]))

        highest_Q_value = self.get_max_value_from_state(new_state)
        current_Q_value = self.q_table[current_state[0]][current_state[1]][action_to_choose]
        reward, done = self.calculate_reward(new_state)

        # New Q value =    Current Q value +    lr * [Reward + discount_rate * (highest Q value between possible actions from the new state s’ ) — Current Q value ]
        new_Q_value = current_Q_value + self.learning_rate * (reward + self.discount_rate * highest_Q_value - current_Q_value)

        self.q_table[current_state[0]][current_state[1]][action_to_choose] = new_Q_value
        self.total_actions += 1
        return done, reward
        #print("new_Q_value: ", new_Q_value)

    
class GraphicCovid19Environment():
    reward = 0
    have_been_to_kiwi = False
    done = False

    def __init__(self, random_others, q_table_choice = False, q_table = None):
        try:
            self.win = GraphWin('Floor', 500, 500)
            self.win.setCoords(0.0, 0.0, 10.0, 10.0)
            self.win.setBackground("blue4")

            self.world_size = (10, 10)
            self.environment_table = np.zeros(self.world_size, dtype = int)
            self.environment_table[0][0] = States.HOUSE.value
            
            self.draw_grid()
            self.add_house()
            self.add_kiwi()
            self.add_survivor()
            self.add_someone(random_others)
            
            self.environment_table[self.world_size[0]-1][self.world_size[1]-1] = States.KIWI.value
            
            self.q_table = q_table
            self.q_table_choice = q_table_choice
            
            self.listen_for_keys()   
            self.win.close()
        except Exception:
            print("Ooops, something is wrong")
            print(traceback.format_exc())
            if self.win != None:    
                self.win.close()
                
    def add_someone(self, random_others):
        
        for other_pos in random_others:
            self.environment_table[other_pos[0]][other_pos[1]] = States.SOMEONE.value
            other1 = Rectangle(Point(other_pos[0] + 0.3,other_pos[1] + 0.3), Point(other_pos[0] + 0.8, other_pos[1] + 0.8))
            other1.draw(self.win)
            other1.setFill("orange")
        
        print("Others are added")
        
    def listen_for_keys(self):
        while not self.done:
            k = self.win.checkKey()

            if k == 'Left':
                self.do_action(Actions.LEFT.value)
            elif k == 'Right':
                self.do_action(Actions.RIGHT.value)
            elif k == 'Up':
                self.do_action(Actions.FORWARD.value)
            elif k == 'Down':
                if self.q_table_choice:
                    self.do_action_from_q_table()
                else:
                    self.do_action()
            elif k == 'period':
                break
        print("Total reward: ", self.reward)
    
    def do_action_from_q_table(self):
        current_state = self.get_state(self.survivor.get_body_pos(), self.survivor.get_vision_pos())
        action_to_do = np.argmax(self.q_table[current_state[0],current_state[1],:])
        self.do_action(action_to_do)
        
    def is_within_bounds(self, pos):
        return pos[0] < self.world_size[0] and pos[1] < self.world_size[1] and pos[0] >= 0 and pos[1] >= 0
    
    def get_stand_state(self, stand_pos):
        if not self.is_within_bounds(stand_pos):
            return 4
        return self.environment_table[stand_pos[0]][stand_pos[1]]

    def get_see_state(self, see_pos):
        if not self.is_within_bounds(see_pos):
            return 4
        return self.environment_table[see_pos[0]][see_pos[1]]

    def get_state(self, stand_pos, see_pos):
        return self.get_stand_state(stand_pos), self.get_see_state(see_pos)
        
    def draw_grid(self):
        print("PlottingGrid")
        for x in range(10):
            for y in range(10):
                self.win.plotPixel(x*50, y*50, "yellow")
        print("FinishedPlotting")
    
    def add_house(self):
        self.housePos = [0, 0]
        house = Rectangle(Point(0,0), Point(1,1))
        house.draw(self.win)
        house.setFill("brown")
        print("House added")
    
    def add_survivor(self):
        self.survivor = GraphicMovableObj(self.win)
        print("Survivor added")
        
    def add_kiwi(self):
        self.kiwiPos = [9, 9]
        kiwi = Rectangle(Point(9,9), Point(10, 10))
        kiwi.draw(self.win)
        kiwi.setFill("green")
        print("Kiwi added")
    
    def reset_environment(self):
        self.survivor.restart()
    
    def do_action(self, num = -1):
        if num == -1:
            # Do random choice
            num = randint(0, 2)
        if num == Actions.LEFT.value:
            self.survivor.look_left()
        elif num == Actions.RIGHT.value:
            self.survivor.look_left(False)
        elif num == Actions.FORWARD.value:
            self.survivor.move_forward()
        else:
            print("Something is wrong when doing an action: ", num)
        new_reward, done = self.calculate_rewards(self.get_state(self.survivor.get_body_pos(), self.survivor.get_vision_pos()))
        self.reward += new_reward
        self.done = done
    
    def calculate_rewards(self, state):
        print(States(state[0]), States(state[1]))
        if state[0] == States.NOTHING.value:
            return -1, False
        elif state[0] == States.SOMEONE.value:
            return -10, False
        elif state[0] == States.KIWI.value:
            if self.have_been_to_kiwi:
                return 0, False
            else:
                self.have_been_to_kiwi = True
                return 50, False
        elif state[0] == States.HOUSE.value:
            if self.have_been_to_kiwi:
                print("Wooow! House reached after Kiwi!", self.reward + 200)
                return 200, True
            else:
                print("House reached: ", self.reward + 30)
                return 30, True
            
            return 10, True
        elif state[0] == States.BORDER.value:
            print("Out of the border.", self.reward - 1000)
            return -1000, True
        else:
            print("Something is wrong: ", state)


