"""
Roman Andres Aguilar Hernández
Ricardo Huerta Dorame
"""
import random
import time
import math
import fileinput
"""
FUNCTION DEFINITIONS
"""
#Auxiliary function to find X,Y in a matrix of a given number
def findPosition(val, someList):
        for index, row in enumerate(someList):
                if val in row:
                    return [index, row.index(val)]

#Auxiliary function to print any matrix
def printMatrix(nombre):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in nombre]))

# Auxiliary function to read file and divide it in matrixes
def readFile():
    global currentArray
    global goalArray
    global n

    generalArray = []
    currentArray = []
    goalArray = []
    myList = []

    n = 0;
    cont = 0;

    for line in fileinput.input():
        if(cont == 0):
            cont += 1
            n = int(line)
        else:
            generalArray.append(line)

    myList = [i.split('\n')[0] for i in generalArray]
    myList = [i.split(',') for i in myList]
    j = 0
    currentArray = myList[:n]
    goalArray = myList[n:]

#Number of incorrect positions (MINIMIZE)
def h1(someList):
    counter = 0
    for x, posX in enumerate(someList):
        for y, posY in enumerate(posX):
            if someList[x][y] != goalArray[x][y]:
                counter += 1
    #print(counter)
    return counter

#Number of direct steps to reach final position (MINIMIZE)
def h2(someList):
    counter = 0
    for x, posX in enumerate(someList):
        for y, posY in enumerate(posX):
            coord = findPosition(someList[x][y], goalArray)
            deltaX = abs(x - coord[0])
            deltaY = abs(y - coord[1])
            counter += deltaX + deltaY                               
    return counter

#Auxiliary function to add both h1 and h2 results and get the final Heuristic result
def h(someList):
    return h1(someList) + h2(someList)

#Function to generate and return an array with all possible children (nodes) of a given node
def generateChildren(someNode):
    global n
    children = []
    x = someNode.pos0[0]
    y = someNode.pos0[1]
    #UP
    if (x - 1) >= 0:
        newBoard = someNode.board
        value = newBoard[x - 1][y]
        newBoard[x][y] = value
        newBoard[x - 1][y] = 0
        new = Node(None, 'U', None, None, newBoard)
        children.append(new)
                    
    #DOWN
    if (x + 1) < n:
        newBoard = someNode.board
        value = newBoard[x + 1][y]
        newBoard[x][y] = value
        newBoard[x + 1][y] = 0
        new = Node(None, 'D', None, None, newBoard)
        children.append(new)
        
    #LEFT
    if (y - 1) >= 0:
        newBoard = someNode.board
        value = newBoard[x][y - 1]
        newBoard[x][y] = value
        newBoard[x][y - 1] = 0
        new = Node(None, 'L', None, None, newBoard)
        children.append(new)
                
    #RIGHT
    if (y + 1) < n:
        newBoard = someNode.board
        value = newBoard[x][y + 1]
        newBoard[x][y] = value
        newBoard[x][y + 1] = 0
        new = Node(None, 'R', None, None, newBoard)
        children.append(new)
    
    return children

"""
NODE DEFINITION
"""
class Node:     
    def __init__(self, fatherIndex, mov, hValue, gValue, board):
        self.fatherIndex = fatherIndex
        self.mov = mov
        self.hValue = hValue
        self.gValue = gValue
        self.board = board
        self.pos0 = findPosition(0, board)
    
    def __eq__(self, other):
        return self.board == other.board
    
    def displayNode(self):
        print ("Father : ", self.fatherIndex,  " Movement: ", self.mov, 
        " hValue: ", self.hValue, "gValue: ", self.gValue, "\nBoard:\n", printMatrix(self.board))
"""
PROGRAM
"""
#MATRIX CREATION
readFile()
#print ("Size of Matrix is {} x {}".format(n, n))
#BFS START
global op 
global cl 
op = []
cl = []
firstNode = Node(None, None, h(currentArray), 0, currentArray)
op.append(firstNode)

#Continue while Open is not empty
while not op:
    x = op.pop(0)

    if x.board == goalArray:
        #Return path Example = (U,U,D,R)
        pass
    else:
        children = generateChildren()

        for child in children:
            #case child is already in open
            if child in op:
                print("Hijo en OPEN")
            #case child is already in closed
            elif child in children:
                if child in cl:
                    print("Hijo en CLOSED")
            #case child is not on open or closed
            else:
                child.hValue = h(child.board)
                op.append(child)