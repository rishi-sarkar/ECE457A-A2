from board import *
from agent import Agent
import random


class RandomAgent(Agent):
    def move(self, state):
        if (self.lost(state)):
            return False
        # assign square a random occupied square that has >0 open paths
        occupiedSquares = self.occupiedSquares(state)
        square = random.choice(occupiedSquares)
        
        while (len(square.neighbors(state)) == 0):
            square = random.choice(occupiedSquares)
        
        direction = random.choice(square.neighbors(state))
        
        self.place(square, direction, state)
        
        return True
        
        
            