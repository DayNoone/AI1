import numpy as np
import copy
import math
import random

# Simulated Annealing
def objective_function(list):
	penalty

	#Calculating row penalty
	for row in xrange(len(list[0])):
		rowValue = 0
		for column in xrange(len(list)):
			if list[row][column] == 1:
				rowValue += 1
		if rowValue > K:
			penalty += 1

	#Calculating column penalty
	for column in xrange(len(list)):
		columnValue = 0
		for row in xrange(len(list[0])):
			if list[row][column] == 1:
				columnValue += 1
		if columnValue > K:
			penalty += 1

	#Calculating diagonal value
	matrix = np.array(list)
	diags = [matrix[::-1,:].diagonal(i) for i in range(-matrix.shape[0]+1,matrix.shape[1])]
	diags.extend(matrix.diagonal(i) for i in range(matrix.shape[1]-1,-matrix.shape[0],-1))
	for n in diags:
		if sum(n) > K:
			penalty += 1

	rating =  1.0/(1.0+penalty)
	return rating

def generateNeighbors(p, currentNodeX, currentNodeY):
	neighbors = []
	path = []

	for i in range(4):
		child = copy.deepcopy(p)
		ydy = currentNodeY + dy[i]
		xdx = currentNodeX + dx[i]
		
		if ydy >= len(p) or xdx >= len(p[0]) or ydy < 0 or xdx < 0:
			continue
		
		if child[ydy][xdx] == 0:
			child[ydy][xdx] = 1
		elif child[ydy][xdx] == 1:
			child[ydy][xdx] = 0
		if objective_function(child) != -1:
			neighbors.append(child)
		path.append(i)
	print len(neighbors)
	return neighbors, path

def findBestNeighbor(neighbors, path):
	bestValue = -100
	pMax = None 
	newdx, newdy = 0, 0
	for i in range(len(neighbors)):
		tempValue = objective_function(neighbors[i])
		if tempValue > bestValue:
			bestNeighbor = neighbors[i]
			bestValue = tempValue
			newdx = dx[path[i]]
			newdy = dy[path[i]]
	return bestNeighbor, newdx, newdy

def getQ(state, bestNeighbor):
	valueState = objective_function(state)
	if valueState == 0:
		return 0
	return (objective_function(bestNeighbor) - valueState)/valueState

def getNewP(q, T):
	p = math.exp(-q/T)
	if p < 1:
		return p
	else:
		return 1

def SA():
	state = [[0 for x in xrange(N)] for y in xrange(N)]

	temp = tempMax

	currentNodeX = 0
	currentNodeY = 0

	while temp > 0:
		if state != None:
			for a in state:
				print a                
		print objective_function(state)
		print currentNodeX, currentNodeY

		print
		if objective_function(state) >= fTarget:
			print 'Optimal solution'
			return state
		else:
			neighbors, path = generateNeighbors(state, currentNodeX, currentNodeY)
			pMax, currentdx, currentdy = findBestNeighbor(neighbors, path)
			currentNodeX += currentdx
			currentNodeY += currentdy


			q = getQ(state, pMax)
			
			p = getNewP(q, temp)

			x = random.randint(0, fTarget)
			
			if x > p:
				state = pMax
			else:
				neighbors.remove(pMax)
				p = neighbors[random.randint(0, len(neighbors)-1)]

			temp -= dT

# MAIN
dx = [1, 1, 0, -1, -1, -1, 0, 1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]
N = 5
M = 5
K = 2
tempMax = 1.0
fTarget = 10
dT = 0.02

SA()
