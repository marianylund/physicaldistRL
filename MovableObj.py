from graphics import *
import math

class MovableObj():
    up = [0, 1]
    down = [0, -1]
    right = [1, 0] 
    left = [-1, 0]

    def __init__(self, start_pos):
        self.directions = [[1, 3], [2, 0], [3, 1], [0, 2]]
        self.moves = [[[-1, -1], [1, -1]], [[1, -1], [1, 1]], [[1, 1], [-1, 1]], [[-1, 1],[-1, -1]]]
        self.states = [self.up, self.left, self.down, self.right]
        self.currentState = 0
        self.current_pos = start_pos
        
    def get_body_pos(self):
        return self.current_pos
    
    def get_vision_pos(self):
        return (self.current_pos[0] + self.states[self.currentState][0], self.current_pos[1] + self.states[self.currentState][1]) 
    
    def do_action(self, action_num):
        if action_num == 2:
            self.move_forward()
        else:
            self.look_left(action_num)
            
    def move_forward(self):
        #print("Old pos: ", self.get_body_pos(), self.get_vision_pos())
        direction = self.states[self.currentState]
        self.current_pos = (self.current_pos[0] + direction[0], self.current_pos[1] + direction[1])
        #print("After moving forward pos: ", self.get_body_pos(), self.get_vision_pos())
    
    def restart(self):
        self.currentState = 0

    def look_left(self, left = 0):
        #print(self.currentState, "Old pos: ", self.get_body_pos(), self.get_vision_pos())
        
        nextState = self.directions[self.currentState][left]
        self.currentState = nextState
        
        #print(self.currentState, "After looking left/right ", left, " pos: ", self.get_body_pos(), self.get_vision_pos())
        

class GraphicMovableObj():
    up = [0, 1]
    down = [0, -1]
    right = [1, 0] 
    left = [-1, 0]
    def __init__(self, window):
        self.win = window
        self.body = Rectangle(Point(5.3,5.3), Point(5.8,5.8)) # size 0.5
        self.body.draw(self.win)
        self.body.setFill("white")
        self.vision = Rectangle(Point(5,6), Point(6,7))
        self.vision.draw(self.win)
        self.vision.setFill("blue1")
        
        self.directions = [[1, 3], [2, 0], [3, 1], [0, 2]]
        self.moves = [[[-1, -1], [1, -1]], [[1, -1], [1, 1]], [[1, 1], [-1, 1]], [[-1, 1],[-1, -1]]]
        self.states = [self.up, self.left, self.down, self.right]
        self.currentState = 0
        
    def get_body_pos(self):
        return [math.floor(self.body.getCenter().getX()), math.floor(self.body.getCenter().getY())]
    
    def get_vision_pos(self):
        return [math.floor(self.vision.getCenter().getX()), math.floor(self.vision.getCenter().getY())]
    
    def move_forward(self):
        direction = self.states[self.currentState]
        self.vision.move(direction[0], direction[1])
        self.body.move(direction[0], direction[1])
    
    def restart(self):
        self.vision.undraw()
        self.vision = Rectangle(Point(5,6), Point(6,7))
        self.vision.draw(self.win)
        self.vision.setFill("blue1")
        self.body.undraw()
        self.body = Rectangle(Point(5.3,5.3), Point(5.8,5.8))
        self.body.draw(self.win)
        self.body.setFill("white")
        self.currentState = 0
    
    # TODO FIX not ending when found
    def get_body_vis_state(self, object_positions):
        visionPos = self.get_vision_pos()
        
        bodyPos = self.get_body_pos()
        print(visionPos, bodyPos)
        state_body_vis = [len(object_positions) + 1, len(object_positions) + 1]
        for i in range(len(object_positions)):
            if visionPos[0] == object_positions[i][0] and visionPos[1] == object_positions[i][1]:
                state_body_vis[1] = i
            elif bodyPos[0] == object_positions[i][0] and bodyPos[1] == object_positions[i][1]:
                state_body_vis[0] = i
        return state_body_vis

    def look_left(self, left = True):
        nextState = self.directions[self.currentState][0 if left else 1]
        
        #print("\nCurrentState: ", self.currentState, "left: ", left)
        #print("nextState: ", nextState)

        xPos = self.moves[self.currentState][0 if left else 1][0] #xDestination - visionPos[0]

        yPos = self.moves[self.currentState][0 if left else 1][1] #yDestination - visionPos[1]
        #print(xPos, yPos)
        #print("newPos", xPos, yPos)
        self.vision.move(xPos, yPos)
        self.currentState = nextState
        #print(self.vision.getP1(), self.vision.getP1())
        #print("newState: ", self.currentState)
