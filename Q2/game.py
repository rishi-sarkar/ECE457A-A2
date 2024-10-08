from board import *


def main():
    # init players [user, comp]
    players = [RandomAgent(1),RandomAgent(-1)]
    
    # init board
    board[0][0].occupied = players[0].piece
    board[0][0].value = 10
    board[3][3].occupied = players[1].piece
    board[3][3].value = 10
    print_map()
    
    move = 0
    
    while True:
        turn = move % 2
        move += 1
        players[turn].randomMove()
    
    


main()