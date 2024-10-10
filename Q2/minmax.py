from board import move

def gameplay(currentNode):
    move = 0
    turn = move % 2
    move = move + 1
    exitFound = 0
    stepsTaken = -1
    queue = [currentNode]

    while (not exitFound):
        currentNode = queue.pop()
        if (currentNode.outBounds() or currentNode.closed()):
            continue

        stepsTaken = stepsTaken + 1

        if (currentNode.exit()):
            return currentNode, stepsTaken

        queue.append(Node((currentNode.i, currentNode.j-1), currentNode))
        queue.append(Node((currentNode.i-1, currentNode.j), currentNode))
        queue.append(Node((currentNode.i, currentNode.j+1), currentNode))
        queue.append(Node((currentNode.i+1, currentNode.j), currentNode))

        currentNode.updateMap()
    return start, stepsTaken


def DFS(currentNode):
    if (currentNode.outBounds()):
        return 0
    if(currentNode.location() == 7 or currentNode.location() == 1):
        return 0
        
    if (currentNode.exit()):
        return currentNode
    
    memory[currentNode.i][currentNode.j] = 7
    
    path.append(DFS(Node(currentNode.i+1, currentNode.j)))
    if(path[0]):
        return currentNode
    path.pop(0)
    memory[currentNode.i][currentNode.j] = 7
    
    path.append(DFS(Node(currentNode.i, currentNode.j+1)))
    if(path[0]):
        return currentNode
    path.pop(0)
    memory[currentNode.i][currentNode.j] = 7
    
    path.append(DFS(Node(currentNode.i-1, currentNode.j)))
    if(path[0]):
        return currentNode
    path.pop(0)
    memory[currentNode.i][currentNode.j] = 7
    
    path.append(DFS(Node(currentNode.i, currentNode.j-1)))
    if(path[0]):
        return currentNode
    path.pop(0)
    memory[currentNode.i][currentNode.j] = 7
    
    return 0



def A(currentNode, targetLocation):
    stepsTaken = -1

    queue = [currentNode]

    while (not exitFound):
        currentNode = queue.pop(0)
        if (currentNode.outBounds() or currentNode.closed()):
            continue

        stepsTaken = stepsTaken + 1

        if (currentNode.exit()):
            return currentNode, stepsTaken
        
        queue.sort(key=lambda x: (x.dist[target] + len(x.path)))

        queue.append(Node((currentNode.i, currentNode.j-1), currentNode))
        queue.append(Node((currentNode.i-1, currentNode.j), currentNode))
        queue.append(Node((currentNode.i, currentNode.j+1), currentNode))
        queue.append(Node((currentNode.i+1, currentNode.j), currentNode))

        currentNode.updateMap()

    return start, stepsTaken


# iterates all positions and chooses the one with highest score
def compMove():
    bestMove = - 1
    bestScore = -100
    for x in range(9):
        if position[x] == ' ':
            position[x] = 'o'
            score = minimax(False)
            position[x] = ' '
            if score > bestScore:
                bestScore = score
                bestMove = x
    return bestMove


# Minimax algorithm
def minimax(isMaximizing):
    if isWinner('o') and not isMaximizing:
        return 1
    elif isWinner('x') and isMaximizing:
        return -1
    elif isBoardFull():
        return 0
    else:
        if (isMaximizing):  # Computer's Move
            bestScore = -100
            for x in range(9):
                if position[x] == ' ':
                    position[x] = 'o'
                    score = minimax(False)
                    position[x] = ' '
                    bestScore = max(bestScore, score)
            return bestScore
        else:  # Player's Move
            bestScore = 100
            for x in range(9):
                if position[x] == ' ':
                    position[x] = 'x'
                    score = minimax(True)
                    position[x] = ' '
                    bestScore = min(bestScore, score)
            return bestScore
