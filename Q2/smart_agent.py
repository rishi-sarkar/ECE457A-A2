from board import *
from agent import Agent
import copy
class SmartAgent(Agent):
    
    def heuristics_opponent_paths(self, square, direction):
        global board
        copy_board = copy.deepcopy(board)
        # copy_board = np.array([[copy.deepcopy(board[i][j]) for j in range(4)] for i in range(4)])
        
        def copy_place(square, direction):
            x,y = direction
            i, j = square.x, square.y
            
            AllowDirection = lambda i, j, piece: -1 < i < 4 and -1 < j < 4 and copy_board[i][j].occupied in (piece, 0)
            for m in [1,2,10]:
                i += x
                j += y
                
                # placing appropriate amount of stones into current path
                copy_board[i][j].value += min(1*m, square.value)
                square.value -= min(1*m, square.value)
                
                # assigning the cell as user's occupied cell
                copy_board[i][j].occupied = self.piece
                
                #checking for empty initial cell, next cell being occupied, or next cell being out of bounds
                if (copy_board[i][j].value == 0):
                    break
                
                if (not AllowDirection(i+x, j+y, self.piece)):
                    copy_board[i][j].value += square.value
                    square.value = 0
                    break
        
        copy_place(copy_board[square.x][square.y], direction)
        
        self.piece *= -1
        
        opp_squares = self.occupiedSquares
        opp_paths_length = 0
        
        for opp_square in opp_squares:
            opp_paths_length += len(opp_square.neighbors)
        
        self.piece *= -1        
        return opp_paths_length
    
    def sortPaths(self):
        # a = 1 # a is the weight for # of neighbors
        # b = 1 # b is the weight for value of cell
        # c = 1 # c is the weight for # of open cells in the direction of play
        # d = 1 # d is the weight for # of opponent cells occupied after a direction would be played
        occupiedSquares = self.occupiedSquares
        sortedPaths = []
        
        for square in occupiedSquares:
            for direction in square.neighbors:
                h = square.value + direction_length(square, direction) - self.heuristics_opponent_paths(square, direction)
                sortedPaths.append((square, direction, h))
        True #delete
        sortedPaths.sort(key = lambda x: x[2], reverse = True)
        
        return sortedPaths
    
    def smartPlace(self):
        sortedPaths = self.sortPaths()
        self.place(sortedPaths[0][0], sortedPaths[0][1])

            
        
        
        
        

def direction_length(square, direction):
    x,y = direction
    i, j = square.x, square.y
    
    for m in range(1,4):
        curr_i = i+ m*x
        curr_j = j+ m*y
        
        if curr_i+x < 0 or curr_i+x > 3:
            return m
        if curr_j+y < 0 or curr_j+y > 3:
            return m
        if (board[curr_i+x][curr_j+y].occupied == square.occupied*(-1)):
            return m