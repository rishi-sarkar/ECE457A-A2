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