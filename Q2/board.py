import numpy as np

# each cell in the board
class Cell:
    def __init__(self, coordinates) -> None:
        self.x, self.y = coordinates
        self._occupied = 0 # 0 - empty; 1 - USER; -1 - COMP
        self.value = 0
    
    
    @property
    def occupied(self):
        if (self.value == 0):
            self._occupied = 0
        return self._occupied
    
    @occupied.setter
    def occupied(self, value):
        self._occupied = value

    def neighbors(self, state):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (self.x+i) < 0 or (self.x+i) > 3:
                    continue
                if (self.y+j) < 0 or (self.y+j) > 3:
                    continue
                if (i == 0 and j == 0):
                    continue
                if state[self.x+i][self.y+j].occupied in (self.occupied, 0):
                    neighbors.append((i,j))
        return neighbors



# initialize players and map
board = np.array([[Cell((i, j)) for j in range(4)] for i in range(4)])

# value_board = np.array([[0 in range(4)] in range(4)])
# player_board = np.array([[0 in range(4)] in range(4)])

# value_board[0][0] = 10
# value_board[3][3] = 10

# player_board[0][0] = 1
# player_board[3][3] = -1


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


