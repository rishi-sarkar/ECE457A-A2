from board import *
from random_agent import RandomAgent
from smart_agent import SmartAgent


def main():
    # init players [user, comp]
    user = SmartAgent(1)
    comp = RandomAgent(-1)
    
    # init board
    board[0][0].occupied = user.piece
    board[0][0].value = 10
    board[3][3].occupied = comp.piece
    board[3][3].value = 10
    print_map()
    
    move = 0
    
    while True:
        turn = move % 2
        move += 1
        if (turn == 0):
            user.smartPlace()
        else:
            comp.randomMove()
        print_map()
    
    


main()