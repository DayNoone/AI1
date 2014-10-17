import numpy as np
import math
import random
import copy
 
# Simulated Annealing
def objective_function(p):
    penalty = 0
 
    # Calculating row penalty
    for row in xrange(len(p[0])):
        rowValue = 0
        for column in xrange(len(p)):
            if p[row][column] == 1:
                rowValue += 1
        if rowValue > K:
            penalty += 1
 
    #Calculating column penalty
    for column in xrange(len(p)):
        columnValue = 0
        for row in xrange(len(p[0])):
            if p[row][column] == 1:
                columnValue += 1
        if columnValue > K:
            penalty += 1
 
    #Calculating diagonal value
    matrix = np.array(p)
    diags = [matrix[::-1, :].diagonal(i) for i in range(-matrix.shape[0] + 1, matrix.shape[1])]
    diags.extend(matrix.diagonal(i) for i in range(matrix.shape[1] - 1, -matrix.shape[0], -1))
    for n in diags:
        if sum(n) > K:
            penalty += 1

    #Rating returns 1 for an optimal solution and less
    # for a suboptimal solution with more conflicts
    rating = 1.0 / (1.0 + penalty)
    return rating
 
 
def generateNeighbors(p):
    # Neighbors are only created based on conflicting row and columns, not diagonals
    # Conflicts in diagonals are taken into account in the objective_function

    neighbors = []
    conflictEggs = []
 
    #Generating neighbors for problem-rows
    for row in range(len(p)):
        #rowValue is set to amount of eggs in row
        rowValue = 0
        for column in xrange(len(p[0])):
            if p[row][column] == 1:
                rowValue += 1
                conflictEggs.append([row, column])
        #Breaking loop when first conflict-row is found
        if rowValue > K:
            break
        else:
        #Clear conflict-eggs when the row is not a conflict-row
            conflictEggs = []

    #Moving a conflict-egg to another column
    for i in conflictEggs:
        for row in range(len(p[0])):
            child = copy.deepcopy(p)
 
            #Remove conflict node
            child[i[0]][i[1]] = 0
            if child[row][i[1]] == 0 and row != i[0]:
                child[row][i[1]] = 1
                neighbors.append(child)
 
    #Clearing conflict-eggs
    conflictEggs = []
 
    #Generating neighbors for problem-columns
    for column in range(len(p[0])):
        #columnValue is set to amount of eggs in column
        columnValue = 0
        for row in range(len(p)):
            if p[row][column] == 1:
                columnValue += 1
                conflictEggs.append([row, column])
        #Breaking loop when first conflict-column is found
        if columnValue > K:
            break
        #Clear conflict-eggs when the column is not a conflict-column
        else:
            conflictEggs = []

    #Moving a conflict-egg to another row
    for i in conflictEggs:
        for column in range(len(p[0])):
            child = copy.deepcopy(p)
 
            #Remove conflict node
            child[i[0]][i[1]] = 0
            if child[i[0]][column] == 0 and column != i[1]:
                child[i[0]][column] = 1
                neighbors.append(child)

    #If no neighbors are found and the objective_function does not return 1
    # we have a conflict in diagonals
    if len(neighbors) == 0:
        neighbors.append(generateRandomBoard(N, K*N))
    return neighbors
 
 
def findBestNeighbor(neighbors):
    #Selects the best neighbor in the list neighbours based
    # on the objective function and setting it to pMax
    bestValue = 0
    pMax = None
    for i in range(len(neighbors)):
        tempValue = objective_function(neighbors[i])
        if tempValue > bestValue:
            bestValue = tempValue
            pMax = neighbors[i]
    return pMax
 
 
def getQ(state, bestNeighbor):
    valueState = objective_function(state)
    if valueState == 0:
        return 0
    return (objective_function(bestNeighbor) - valueState) / valueState
 
 
def getNewP(q, T):
    return min(1, math.exp(-q / T))
 
 
def generateRandomBoard(sizeOfBoard, noOfEggs):
    eggsPlaced = 0
    board = [[0 for i in range(sizeOfBoard)] for j in range(sizeOfBoard)]
    while eggsPlaced < noOfEggs:
        x, y = random.randint(0, sizeOfBoard-1), random.randint(0, sizeOfBoard-1)
        if board[y][x] == 0:
            board[y][x] = 1
            eggsPlaced += 1
    return board
 
 
def SA():
    #Starting with a random board
    state = generateRandomBoard(N, K*N)
    temp = tempMax

    #Main loop
    while temp > dT:
        if objective_function(state) == 1:

            #Printing solution and value when
            # an optimal solution is found
            for a in state:
                print a
            print objective_function(state)
            print
            return 1

        else:
            neighbors = generateNeighbors(state)
            pMax = findBestNeighbor(neighbors)
 
            q = getQ(state, pMax)
 
            p = getNewP(q, temp)
 
            x = random.random()

            if x > p:
                state = pMax

            # A random neighbor is choosen if the
            # temperature is low enough
            else:
                if len(neighbors) == 1:
                    state = neighbors[0]
                else:
                    neighbors.remove(pMax)
                    state = neighbors[random.randint(0, len(neighbors) - 1)]
 
            temp -= dT
    for a in state:
        print a
    print objective_function(state)
    print
 
 
# MAIN
N = 10
K = 3
M = N
tempMax = 1.0
dT = 0.002

#Runs the code several times and the amount of optimal solutions found
counter = 0
runs = 100
for i in range(runs):
    if SA() == 1:
        counter += 1
print "Optimal solutions: " + str((counter/runs)*100) + "%"