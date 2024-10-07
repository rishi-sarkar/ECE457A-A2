import numpy as np

# each cell in the board
class Cell:
    def __init__(self, coordinates) -> None:
        self.x, self.y = coordinates
        self.occupied = 0 # 0 - empty; 1 - USER; -1 - COMP
        self.neighbors = self.openPaths() # number of empty neighbors
        self.value = 0

    def openPaths(self):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (self.x+i) < 0 or (self.x+i) > 3:
                    continue
                if map[self.x+i][self.y+j].occupied == self.occupied:
                    neighbors.append((i,j))
        self.neighbors = neighbors
        return neighbors


board = np.array([[Cell((i, j)) for j in range(4)] for i in range(4)])
# init players and map
USER = 1
COMP = -1

board[0][0].occupied = USER
board[0][0].value = 10

board[3][3].occupied = COMP
board[3][3].value = 10

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


