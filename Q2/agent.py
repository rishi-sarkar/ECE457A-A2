from board import *

class Agent:
    def __init__(self, piece):
        self.piece = piece
        self.occupiedSquares = []
    
    @property
    def occupiedSquares(self):
        occupiedSquares = []
        for i in range(4):
            for j in range(4):
                if board[i][j].occupied == self.piece:
                    occupiedSquares.append(board[i][j])
        return occupiedSquares
    
    # goes through every piece on board and checks if any have neighbors
    def lost(self):
        occupiedSquares = self.occupiedSquares() # all of agent's pieces
        for _ in len(occupiedSquares):
            if len(occupiedSquares[_].openPaths()) > 0: # all open paths per occupied square
                return False
        return True
    
    def place(self, square, direction):
        x,y = direction
        i, j = square.x, square.y
        
        for m in range(1,4):
            if i+m*x 
            
            if (m == 3):
                board[i+m*x][j+m*y].value += board[i][j].value
                board[i][j].value == 0
                break
            board[i+m*x][j+m*y].value += 1*m
            board[i][j].value -= 1
            if (board[i][j].value == 0):
                break
            
            
        
        