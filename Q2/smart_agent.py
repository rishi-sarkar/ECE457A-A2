from board import *
from agent import Agent
import copy
class SmartAgent(Agent):
    
    def heuristics_opponent_paths(self, square, direction, state):
        global board
        next_state = copy.deepcopy(state)
        # prev_state = np.array([[copy.deepcopy(board[i][j]) for j in range(4)] for i in range(4)])
        
        self.place(next_state[square.x][square.y], direction, next_state)
        
        self.piece *= -1
        
        opp_squares = self.occupiedSquares(next_state)
        opp_paths_length = 0
        
        for opp_square in opp_squares:
            opp_paths_length += len(opp_square.neighbors(next_state))
        
        self.piece *= -1        
        return opp_paths_length
    
    def sortPaths(self, state):
        a = 0.8 # weight for # of stones in a square
        b = 0.4 # weight for length of the direction
        c = 1.0 # weight for number of opponent paths for selected direction
        occupiedSquares:list[Cell] = self.occupiedSquares(state)
        sortedPaths = []
        
        for square in occupiedSquares:
            for direction in square.neighbors(state):
                h = a*square.value + b*direction_length(square, direction, state) - c*self.heuristics_opponent_paths(square, direction, state)
                sortedPaths.append((square, direction, h))
        True #delete
        sortedPaths.sort(key = lambda x: x[2], reverse = True)
        
        return sortedPaths
    
    def move(self, state):
        if (self.lost(state)):
            return False
        
        sortedPaths = self.sortPaths(state)
        
        self.place(sortedPaths[0][0], sortedPaths[0][1], state)
        
        return True

            
        
        
        
        

def direction_length(square, direction, state):
    x,y = direction
    i, j = square.x, square.y
    
    for m in range(4):            
        i += x
        j += y
        
        if (-1 < i < 4 and -1 < j < 4 and state[i][j].occupied in (square.occupied, 0)):
            continue
        return m
    