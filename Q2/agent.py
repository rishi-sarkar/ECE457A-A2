from board import *

class Agent:
    def __init__(self, piece):
        self.piece = piece
    
    def occupiedSquares(self, state):
        occupiedSquares = []
        for i in range(4):
            for j in range(4):
                if state[i][j].occupied == self.piece:
                    occupiedSquares.append(state[i][j])
        return occupiedSquares
    
    # goes through every piece on board and checks if any have neighbors
    def lost(self, state):
        occupiedSquares = self.occupiedSquares(state) # all of agent's pieces
        for _ in occupiedSquares:
            if len(_.neighbors(state)) > 0: # all open paths per occupied square
                return False
        return True
    
    def place(self, square, direction, state):
        x,y = direction
        i, j = square.x, square.y
        
        # checks for out of bounds on x and y direction as well as next piece in direction being an opponent piece
        AllowDirection = lambda i, j, piece: -1 < i < 4 and -1 < j < 4 and state[i][j].occupied in (piece, 0)
        
        for m in [1,2,10]:
            i += x
            j += y
            
            # placing appropriate amount of stones into current path
            state[i][j].value += min(1*m, square.value)
            square.value -= min(1*m, square.value)
            
            # assigning the cell as user's occupied cell
            state[i][j].occupied = self.piece
            
            #checking for empty initial cell, next cell being occupied, or next cell being out of bounds
            if (state[i][j].value == 0):
                break
            
            if (not AllowDirection(i+x, j+y, self.piece)):
                state[i][j].value += square.value
                square.value = 0
                break