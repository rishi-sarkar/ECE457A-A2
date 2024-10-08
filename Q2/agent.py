from board import *

class Agent:
    def __init__(self, piece):
        self.piece = piece
        self._occupiedSquares = []
    
    @property
    def occupiedSquares(self):
        occupiedSquares = []
        for i in range(4):
            for j in range(4):
                if board[i][j].occupied == self.piece:
                    occupiedSquares.append(board[i][j])
        self._occupiedSquares = occupiedSquares
        return self._occupiedSquares
    
    # goes through every piece on board and checks if any have neighbors
    def lost(self):
        occupiedSquares = self.occupiedSquares # all of agent's pieces
        for _ in occupiedSquares:
            if len(_.neighbors) > 0: # all open paths per occupied square
                return False
        return True
    
    def place(self, square, direction):
        x,y = direction
        i, j = square.x, square.y
        
        for m in range(1,4):
            curr_i = i+ m*x
            curr_j = j+ m*y
            
            # two cases where remaining stones go to last spot
            if (m == 3):
                board[curr_i][curr_j].value += square.value
                board[curr_i][curr_j].occupied = self.piece
                square.value = 0
                break
            
            if (m == 2 and square.value == 1):
                board[curr_i][curr_j].value += square.value
                board[curr_i][curr_j].occupied = self.piece
                square.value = 0
                break
            
            # placing appropriate amount of stones into current path
            board[curr_i][curr_j].value += 1*m
            board[curr_i][curr_j].occupied = self.piece
            square.value -= 1*m
            
            #checking for empty initial cell, next cell being occupied, or next cell being out of bounds
            if (board[i][j].value == 0):
                break
            
            if curr_i+x < 0 or curr_i+1+x > 3:
                board[curr_i][curr_j].value += square.value
                square.value = 0
                break
            
            if curr_j+y < 0 or curr_j+y > 3:
                board[curr_i][curr_j].value += square.value
                square.value = 0
                break
                        
            if (board[curr_i+x][curr_j+y].occupied == self.piece*(-1)):
                board[curr_i][curr_j].value += square.value
                square.value = 0
                break
            
            print_map()
            
            
        
        