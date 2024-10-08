import numpy as np
from random_agent import RandomAgent

# each cell in the board
class Cell:
    def __init__(self, coordinates) -> None:
        self.x, self.y = coordinates
        self._occupied = 0 # 0 - empty; 1 - USER; -1 - COMP
        self._neighbors = [] # number of empty neighbors
        self.value = 0
        
    @property
    def occupied(self):
        if (self.value == 0):
            self._occupied = 0
        return self._occupied
    
    @occupied.setter
    def occupied(self, value):
        self._occupied = value

    @property
    def neighbors(self):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (self.x+i) < 0 or (self.x+i) > 3:
                    continue
                if (i == 0 and j == 0):
                    continue
                if map[self.x+i][self.y+j].occupied in (self.occupied, 0):
                    neighbors.append((i,j))
        self._neighbors = neighbors
        return self._neighbors



# initialize players and map
board = np.array([[Cell((i, j)) for j in range(4)] for i in range(4)])

def print_map():
    for i in range(4):
        for j in range(4):
            if board[i][j].occupied == -1:
                print("[ " + f"{str(board[i][j].value):02}" + " ]", end="")
            elif board[i][j].occupied == 0:
                print("( " + f"{str(board[i][j].value):02}" + " )", end="")
            else:
                print("{ " + f"{str(board[i][j].value):02}" + " }", end="")
        print()
    print()


