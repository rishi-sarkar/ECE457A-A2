from board import *
import random

class RandomAgent:
    def __init__(self, piece):
        self.piece = piece
    
    def occupiedSquares(self):
        occupiedSquares = []
        for i in range(4):
            for j in range(4):
                if board[i][j].occupied == self.piece:
                    occupiedSquares.append((i,j))
        return occupiedSquares
    def randomMove(self):
        occupiedSquares = self.occupiedSquares()
        i = random.randint(0, len(occupiedSquares))
        
        