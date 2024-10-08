from board import *
from agent import Agent
import random


class RandomAgent(Agent):
    def randomMove(self):
        if (self.lost()):
            return False
        # assign square a random occupied square that has >0 open paths
        square = random.choice(self.occupiedSquares)
        
        while (len(square.neighbors) == 0):
            square = random.choice(self.occupiedSquares)
        
        direction = random.choice(square.neighbors)
        
        self.place(square, direction)
        
        
            