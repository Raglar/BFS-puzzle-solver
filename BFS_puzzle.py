"""
Roman Andres Aguilar Hernández
Ricardo Huerta Dorame

Para interpretarlo:
python parcial1.py texto.txt
"""
import random
import time
import math
import fileinput
import copy
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
    for i in range(len(myList)):
        for j in range(int(len(myList)/2)):
            myList[i][j] = int(myList[i][j])

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
    return h1(someList) * 0.30 + h2(someList) * 0.70
    #return h1(someList)
    #return h2(someList)

#Function to generate and return an array with all possible children (nodes) of a given node
def generateChildren(someNode):
    global n
    children = []
    coord = findPosition(0, someNode.board)
    x = coord[0]
    y = coord[1]
    #UP
    if (x - 1) >= 0 and someNode.mov != 'D':
        newBoard = copy.deepcopy(someNode.board)
        value = newBoard[x - 1][y]
        newBoard[x][y] = value
        newBoard[x - 1][y] = 0
        children.append(Node( someNode.id, 'U', h(newBoard), someNode.gValue + 1, newBoard, someNode))
        #printMatrix(newBoard)
        #print()

    #DOWN
    if (x + 1) < n and someNode.mov != 'U':
        newBoard = copy.deepcopy(someNode.board)
        value = newBoard[x + 1][y]
        newBoard[x][y] = value
        newBoard[x + 1][y] = 0
        children.append(Node(someNode.id, 'D', h(newBoard), someNode.gValue + 1, newBoard, someNode))
        #printMatrix(newBoard)
        #print()

    #LEFT
    if (y - 1) >= 0 and someNode.mov != 'R':
        newBoard = copy.deepcopy(someNode.board)
        value = newBoard[x][y - 1]
        newBoard[x][y] = value
        newBoard[x][y - 1] = 0
        children.append(Node(someNode.id, 'L', h(newBoard), someNode.gValue + 1, newBoard, someNode))
        #printMatrix(newBoard)
        #print()

    #RIGHT
    if (y + 1) < n and someNode.mov != 'L':
        newBoard = copy.deepcopy(someNode.board)
        value = newBoard[x][y + 1]
        newBoard[x][y] = value
        newBoard[x][y + 1] = 0
        children.append(Node(someNode.id, 'R', h(newBoard), someNode.gValue + 1, newBoard, someNode))
        #printMatrix(newBoard)
        #print()

    return children

#Function to print the path of movements
def printPath(someNode):
    #print(someNode.fatherIndex)
    if someNode.fatherIndex == -1:
        return ""
    else:
        fullPath = someNode.mov + "," + printPath(cl[findIndexByID(someNode.fatherIndex, cl)])
        return fullPath

#Function to count the path of movements
def countPath(someNode):
    return someNode.gValue

def killChildrenOf(idToSearch):

    for i, nodes in enumerate(cl):
        if nodes.fatherIndex == idToSearch:
            #print("Hijo matado en CLOSED")
            cl.pop(i)

    for i, nodes in enumerate(op):
        if nodes.fatherIndex == idToSearch:
            #print("Hijo matado en OPEN")
            op.pop(i)



#Function to find the index of a node in a list of nodes, given an ID
def findIndexByID(idToFind, someList):
    for i, node in enumerate(someList):
        #print(node.id)
        if node.id == idToFind:
            return someList.index(node)
    return 0

"""
NODE DEFINITION
"""
class Node:
    nodeId = 0

    def __init__(self, fatherIndex, mov, hValue, gValue, board, fatherNode):
        self.fatherIndex = fatherIndex
        self.mov = mov
        self.hValue = hValue
        self.gValue = gValue
        self.board = board
        self.id = Node.nodeId
        self.fatherNode = fatherNode
        Node.nodeId += 1

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
#BFS START
global op
global cl

fullPath = ""

op = []
cl = []
print("ARREGLO INICIAL")
printMatrix(currentArray)
#print()
firstNode = Node(-1, 'root', h(currentArray), 0, currentArray, None)
op.append(firstNode)

#Continue while Open is not empty
while op != []:
    x = op.pop(0)

    if x.board == goalArray:
        print("RESPUESTA:")
        printMatrix(x.board)
        fullPathToPrint = printPath(x)
        fullPathToPrint = fullPathToPrint[:-1]
        fullPathToPrint = fullPathToPrint[::-1]
        print("La salida es:",fullPathToPrint)
        exit()
    else:
        children = generateChildren(x)
        childInOpen = False
        childInClosed = False

        for i, child in enumerate(children):

            #case child is already in open
            for j, nodes in enumerate(op):
                if  op[j] == child:
                    childInOpen = True
                    if child.gValue < op[j].gValue:
                        op[j].hValue = child.hValue
                        op[j].gValue = child.gValue
                        op[j].fatherIndex = child.fatherIndex

            #case child is already in closed
            for k, nodes in enumerate(cl):
                if  cl[k] == child:
                    #print("Hijo en CLOSED")
                    childInClosed = True
                    if child.gValue < cl[k].gValue:
                        killChildrenOf(cl[k].id)
                        cl.pop(k)
                        op.append(child)

            #case child is not on open or closed
            if not childInOpen and not childInClosed:
                #print("Hijo siendo agregado a OPEN")
                op.append(child)

            childInOpen = False
            childInClosed = False

    cl.append(x)
    op.sort(key=lambda la: la.hValue, reverse=False)
