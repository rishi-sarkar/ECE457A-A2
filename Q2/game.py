from board import *
from random_agent import RandomAgent
from smart_agent import *


def main():
    depth = 6
    # init players [comp, user(stupid comp)]
    players = [SmartAgent(1), RandomAgent(-1)]
    
    # init board
    board[0][0].occupied = players[0].piece
    board[0][0].value = 10
    board[3][3].occupied = players[1].piece
    board[3][3].value = 10
    print_map(board)
    
    move = 0
    max_nodes = 0
    
    while True:
        turn = move % 2
        move += 1
        if(not (max_nodes := players[turn].move(board, depth))):
            print("Player ", turn+1, " lost")
            break
        
        print("Move #: ", move, ", Depth Reached: ", depth, ", Max Nodes Searched: ", max_nodes) if turn == 0 else \
        print("Move #: ", move)
        print_map(board)
    
    

main()