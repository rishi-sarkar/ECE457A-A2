from board import *
from agent import Agent
import copy

full_count = 0

class SmartAgent(Agent):
    
    def evaluation_function(self, square, direction, state):
        # a = 1.5 # weight for # of stones in a square
        # b = 1.0 # weight for length of the direction
        c = 0.1 # weight for number of opponent paths for selected direction
        
        ev1 = square.value
        ev2 = self.direction_length(square, direction, state)
        ev3 = c * self.heuristics_opponent_paths(square, direction, ev2, state)
        h = (ev1 + ev2 - ev3)/(ev1 + ev2)
        return h
        
    def heuristics_opponent_paths(self, square, direction, directionLength, state):
        x,y = direction
        prev_occupied = [self.piece]
        square.occupied = 0
        for _ in range(1,(directionLength+1)):
            prev_occupied.append(state[square.x+x*_][square.y+y*_].occupied)
            state[square.x+x*_][square.y+y*_].occupied = self.piece
                
        self.piece *= -1
        
        opp_squares = self.occupiedSquares(state)
        opp_paths_length = 0
        
        for opp_square in opp_squares:
            opp_paths_length += len(opp_square.neighbors(state))
        
        self.piece *= -1
        
        for _ in range(directionLength+1):
            state[square.x+x*_][square.y+y*_].occupied = prev_occupied[_]
                
        # next_state = copy.deepcopy(state)
        
        # self.place(next_state[square.x][square.y], direction, next_state)
        
        # self.piece *= -1
        
        # opp_squares = self.occupiedSquares(next_state)
        # opp_paths_length = 0
        
        # for opp_square in opp_squares:
        #     opp_paths_length += len(opp_square.neighbors(next_state))
        
        # self.piece *= -1        
        return opp_paths_length
    
    def direction_length(self, square, direction, state):
        x,y = direction
        i, j = square.x, square.y
        
        for m in range(4):            
            i += x
            j += y
            
            if (-1 < i < 4 and -1 < j < 4 and state[i][j].occupied in (square.occupied, 0)):
                continue
            return m
    
    def beam_sortPaths(self, state):
        occupiedSquares:list[Cell] = self.occupiedSquares(state)
        sortedPaths = []
        count = 0
        for square in occupiedSquares:
            for direction in square.neighbors(state):
                h = self.evaluation_function(square, direction, state)
                if (count <= 3 or h > 0.5):
                    sortedPaths.append((square, direction, h))
                count += 1
                
        sortedPaths.sort(key = lambda x: x[2], reverse = True)
        
        return sortedPaths[:3]
    
    def move(self, state, depth):
        global full_count
        if (self.lost(state)):
            return False
        
        full_count = 0
        
        sortedPaths = self.beam_sortPaths(state)
        
        # takes the best move according to evaluation function
        '''
        self.place(sortedPaths[0][0], sortedPaths[0][1], state)
        '''
        
        
        # uses minmax alg
        alpha = -1000
        beta = 1000
        # iterates all positions and chooses the one with highest score
        # '''
        score = []
        for (square, path, _) in sortedPaths:
            next_state = copy.deepcopy(state)
            next_square = next_state[square.x][square.y]
            self.place(next_square, path, next_state)
            
            score.append((square, path, minimax(-1, depth-1, next_state, alpha, beta)))
        
        score.sort(key = lambda x: x[2], reverse = True)
        
        bestSquare = score[0][0]
        bestPath = score[0][1]

        self.place(bestSquare, bestPath, state)
        # '''
        
        return full_count
        
# Minimax algorithm
def minimax(isMaximizing, depth, state, alpha, beta):
    global full_count
    switch_minmax = -1 * isMaximizing
    agent = SmartAgent(isMaximizing)
        
    if agent.lost(state):
        full_count += 1
        return switch_minmax
    
    sortedPaths = agent.beam_sortPaths(state)
    
    score = []
    
    if depth == 0:
        full_count += 1
        return sortedPaths[0][2]
    else:
        for square, path, _ in sortedPaths:
            next_state = copy.deepcopy(state)
            next_square = next_state[square.x][square.y]
            agent.place(next_square, path, next_state)
            
            score.append((square, path, minimax(switch_minmax, depth-1, next_state, alpha, beta)))

        score.sort(key = lambda x: x[2], reverse = isMaximizing)
        full_count += 1
        return score[0][2]   
    