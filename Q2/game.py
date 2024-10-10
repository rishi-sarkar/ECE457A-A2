from board import *
from random_agent import RandomAgent
from smart_agent import SmartAgent


def main():
    # init players [user, comp]
    players = [SmartAgent(1), RandomAgent(-1)]
    
    # init board
    board[0][0].occupied = players[0].piece
    board[0][0].value = 10
    board[3][3].occupied = players[1].piece
    board[3][3].value = 10
    print_map(board)
    
    move = 0
    
    while True:
        turn = move % 2
        move += 1
        if(not players[turn].move(board)):
            print("Player ", turn+1, " lost")
            break
        
        print("Move #: ", move)
        print_map(board)
    
    


main()