from board import *
from agent import Agent


class SmartAgent(Agent):
    @property
    def sortPaths(self):
        occupiedSquares = self.occupiedSquares
        sortedCells = []
        h = []
        
        for i in range(len(occupiedSquares)):
            h.append(len(occupiedSquares[i].neighbors) + occupiedSquares[i].value)
            sortedCells.append((occupiedSquares[i], h[i]))
        True #delete
        sortedCells.sort(key = lambda x: x[1], reverse = True)
        
        sortedPaths = []
        
        for i in range(len(sortedCells)):
            for j in range(len(sortedCells[i][0].neighbors)):
                sortedPaths.append((sortedCells[i][0], sortedCells[i][1], sortedCells[i][0].neighbors[j], direction_length(sortedCells[i][0], sortedCells[i][0].neighbors[j])))
        True #delete
        sortedPaths.sort(key = lambda x: (x[1], x[3]), reverse = True)
        
        return sortedPaths
    
    def smartPlace(self):
        sortedPaths = self.sortPaths
        self.place(sortedPaths[0][0], sortedPaths[0][2])

            
        
        
        
        

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