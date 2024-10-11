import numpy as np

# each cell in the board
class Cell:
    def __init__(self, coordinates) -> None:
        self.x, self.y = coordinates
        self.occupied = 0 # 0 - empty; 1 - USER; -1 - COMP
        self.value = 0

    def neighbors(self, state):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0 and j == 0):
                    continue
                if -1 < (self.x+i) < 4 and -1 < (self.y+j) < 4 and state[self.x+i][self.y+j].occupied in (self.occupied, 0):
                    neighbors.append((i,j))
        return neighbors

# initialize players and map
board = np.array([[Cell((i, j)) for j in range(4)] for i in range(4)])

def print_map(state):
    for i in range(4):
        for j in range(4):
            if state[i][j].occupied == -1:
                print("[ " + f"{state[i][j].value:02}" + " ]", end="")
            elif state[i][j].occupied == 0:
                print("( " + f"{state[i][j].value:02}" + " )", end="")
            else:
                print("{ " + f"{state[i][j].value:02}" + " }", end="")
        print()
    print()


