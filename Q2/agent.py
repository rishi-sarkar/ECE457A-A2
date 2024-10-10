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
        
        # checks for out of bounds on x and y direction as well as next piece in direction being an opponent piece
        AllowDirection = lambda i, j, piece: -1 < i < 4 and -1 < j < 4 and board[i][j].occupied in (piece, 0)
        
        for m in [1,2,10]:
            i += x
            j += y
            
            # placing appropriate amount of stones into current path
            board[i][j].value += min(1*m, square.value)
            square.value -= min(1*m, square.value)
            
            # assigning the cell as user's occupied cell
            board[i][j].occupied = self.piece
            
            #checking for empty initial cell, next cell being occupied, or next cell being out of bounds
            if (board[i][j].value == 0):
                break
            
            if (not AllowDirection(i+x, j+y, self.piece)):
                board[i][j].value += square.value
                square.value = 0
                break