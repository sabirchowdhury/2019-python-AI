import numpy as np
import math as math
import random as rand


def updatePossActions(sudoku, sudoku_Poss_Actions, row, column):
    """
    This is a function that updates all the possibles actions given a number using the constraints
    """
    # Updating the possible actions of all the row
    number = sudoku[row][column]
    sudoku_Poss_Actions[row][column] = -1
    if number != 0:
        for i in range(0, 9):
           if isinstance(sudoku_Poss_Actions[row][i], list):
               if number in sudoku_Poss_Actions[row][i]:
                   sudoku_Poss_Actions[row][i].remove(number)

    # Updating the possible actions in the same column
        for i in range(0, 9):
            if isinstance(sudoku_Poss_Actions[i][column], list):
                if number in sudoku_Poss_Actions[i][column]:
                    sudoku_Poss_Actions[i][column].remove(number)

    # Updating the possible actions of the square 3*3 of the number
        rowModulo, columnModulo = math.floor(row/3) * 3, math.floor(column/3) * 3
        for rowI in range(rowModulo, rowModulo+3):
            for columnI in range(columnModulo, columnModulo+3):
                if isinstance(sudoku_Poss_Actions[rowI][columnI], list):
                    if number in sudoku_Poss_Actions[rowI][columnI]:
                        sudoku_Poss_Actions[rowI][columnI].remove(number)

    return sudoku_Poss_Actions


def constraintsCheck(sudoku, row, column, number):
    """
    This is the function that check if the number we just insert is valid in our sudoku

    """
    # First check if our value is in the same square
    sudokoTest = sudoku.copy()
    sudokoTest[row, column] = 0
    rowModulo, columnModulo = math.floor(row/3) * 3, math.floor(column/3) * 3

    #Matrix = [[0,0,0],[0,0,0],[0,0,0]]

    for rowI in range(rowModulo, rowModulo+3):
        for columnI in range(columnModulo, columnModulo+3):
            # Testing by creating a new Matrix to check the actual square
            #rowItest = rowI - rowModulo
            #columnITest = columnI - columnModulo
            #Matrix[rowItest][columnITest] = sudoku[rowI][columnI]
            if(sudokoTest[rowI][columnI] == number):
                return False

    # Second check in the same Row
    if number in sudokoTest[row]:
        return False

    # Third Checking in the Same column
    for y in range(0, 9):
        if sudokoTest[y][column] == number:
            return False

    return True


def findNextPosition(sudoku, sudoku_PossibleActions):
    """
    This is a function that find the next position to fill
    """
    """
    best = [11,0,0]
    for rowSudoku in range(0, 9):
        for columnSudoku in range(0, 9):
            if sudoku[rowSudoku][columnSudoku] == 0:
                test = len(sudoku_PossibleActions[rowSudoku][columnSudoku])
                if test < best[0]:
                    best = [test,rowSudoku,columnSudoku]
    
    if best[0] != 11:
        return [best[1],best[2]]

    return [-1,-1]
    """
    for rowSudoku in range(0, 9):
        for columnSudoku in range(0, 9):
            if(sudoku[rowSudoku][columnSudoku] == 0):
                return [rowSudoku, columnSudoku]

    return [-1, -1]
    


def search_backTrack(sudoku, sudoku_PossibleActions):
    """
    This is a function that implement the backTracking algorithm to search for values using back_tracking
    """
    positionVector = findNextPosition(sudoku, sudoku_PossibleActions)
    row = positionVector[0]
    column = positionVector[1]

    if row == -1 and column == -1:
        return sudoku

    # Loop through the possible values
    for x in sudoku_PossibleActions[row][column]:
        result = constraintsCheck(sudoku, row, column, x)

        if result == True:
            sudoku[row, column] = x
           
            test = search_backTrack(sudoku, sudoku_PossibleActions)

            if(np.array_equal(test, sudoku)):
                return sudoku

        # Updating back our possible values after reaching a dead end
        sudoku[row, column] = 0

    return None

def matrix9ToMatrix3(sudoku):
    """
    Function to divide the 9*9 matrix into 3*3 by matrix
    """
    blocks = [ [ [] , [] , []], [ [] , [] , []] , [ [] , [] , []] ]

    for i in range(0,3):
        for j in range(0,3):
            x,y = i*3,j*3
            blocks[i][j] = [ [sudoku[t][v] for v in range(y,y+3)] for t in range(x,x+3)  ]
        
    return blocks

def oneWayCoord(sudoku,sudoku_Poss_Actions):
    """
    Function to check for unique values where we can only place at this place
    """
    testChangeSudoku = False
    #blocks = matrix9ToMatrix3(sudoku)
    for i in range(0,3):
        for j in range(0,3) :
            row,column = i*3,j*3
            dictValues = {1: [],2: [],3: [],4: [],5: [],6: [],7: [],8: [],9: []}
            for x in range (1,10):
                for z in range(row,row+3):
                    for w in range(column,column+3):
                        if sudoku[z][w] == 0:
                            if x in sudoku_Poss_Actions[z][w]:
                                dictValues[x].append((z,w))
            #print(dictValues)
 
            for index,value in dictValues.items():
                lenPossPlace = len(value)
                if lenPossPlace == 1:
                    #print("Single")
                    test = value[0]
                    testChangeSudoku = True
                    sudoku[test[0],test[1]] = index
                    updatePossActions(sudoku,sudoku_Poss_Actions,test[0],test[1])
                    #Need to update the possible values



                ##DOUBLE ALGORITHM
                if lenPossPlace != 0 and lenPossPlace != 1: 

                    #Can only be in this Column
                    testValue = value[0][0]
                    for tuplesPoss in value:
                        if tuplesPoss[0] != testValue:
                            testValue = tuplesPoss[0]
                            break
                    
                    if testValue == value[0][0]:
                       # print("Double Column ")
                        for ijx in range(0,9):
                            if (testValue,ijx) not in value:
                                if sudoku[testValue][ijx] == 0:
                                    if index in sudoku_Poss_Actions[testValue][ijx]:
                                        testChangeSudoku = True
                                        sudoku_Poss_Actions[testValue][ijx].remove(index)
                    
                    #Can only be in this Row
                    testValue = value[0][1]
                    for tuplesPoss in value:
                        if tuplesPoss[1] != testValue:
                            testValue = tuplesPoss[1]
                            break
                    
                    if testValue == value[0][1]:
                        #print("Double Row")
                        for ijx in range(0,9):
                            if (ijx,testValue) not in value:
                                if sudoku[ijx][testValue] == 0:
                                    if index in sudoku_Poss_Actions[ijx][testValue]:
                                        testChangeSudoku = True
                                        sudoku_Poss_Actions[ijx][testValue].remove(index)

                ##Naked Pair Algorithm
                
                    

                    #If 2 possible actions arrays have two possible numbes and share a same row or column or 
                    # box we can elimate 
                    #This two possible actions from the entier row or column or box

                    #To implement 


    return testChangeSudoku
    
def onePossUpdate(sudoku,sudoku_Poss_Actions):
    """
    This function update our sudoku when there is only one possible value
    """
    test = False
    for i in range(0, 9):
        for j in range(0, 9):
            if sudoku[i][j] == 0:
                if len(sudoku_Poss_Actions[i][j]) == 1:
                    test = True
                    sudoku[i][j] = sudoku_Poss_Actions[i][j][0]
                    updatePossActions(sudoku, sudoku_Poss_Actions, i, j)
                    
    return test

def sudoku_solver(sudoku):
    """
    Main Function to solve a sudoku return an array of -1 if no solution 
    """
    # Creating a copy of our sudoku
   # sudoku_copy = sudoku.copy()
    sudoku_copy = sudoku

    # Creating The possibles Actions 3D array
    sudoku_PossibleActions = [[0 for _ in range(0, 9)] for _ in range(0, 9)]
    for rowSudoku in range(0, 9):
        for columnSudoku in range(0, 9):
            if(sudoku[rowSudoku][columnSudoku] == 0):
                sudoku_PossibleActions[rowSudoku][columnSudoku] = [ 1, 2, 3, 4, 5, 6, 7, 8, 9]
                rand.shuffle(sudoku_PossibleActions[rowSudoku][columnSudoku])
            else:
                sudoku_PossibleActions[rowSudoku][columnSudoku] = -1

    # Updating the Possible Values with the values already here and checking for wrong initial States
    for rowSudoku in range(0, 9):
        for columnSudoku in range(0, 9):
            if sudoku[rowSudoku][columnSudoku] != 0:
                test = constraintsCheck(
                    sudoku_copy, rowSudoku, columnSudoku, sudoku[rowSudoku][columnSudoku])
                # If the Values are initially wrong means that
                if test == False:
                    return np.zeros((9,9)) - 1
                # When its not zero we also need to update our possibleActions
                updatePossActions(
                    sudoku_copy, sudoku_PossibleActions, rowSudoku, columnSudoku)


    #Constraints updating before using backTracking
    changedSudoku = False
    while changedSudoku != True:

        testChangedSudoku1 = oneWayCoord(sudoku_copy,sudoku_PossibleActions)
        testChangedSudoku2 = onePossUpdate(sudoku_copy,sudoku_PossibleActions)
        if testChangedSudoku1 == True and testChangedSudoku2 == True:
            changedSudoku == False
            continue
        changedSudoku = True
    

    #print(sudoku_PossibleActions)
    # calling our BackTracking Search Algorithm
    solved_sudoku = search_backTrack(sudoku_copy, sudoku_PossibleActions)
    
    # If there is no solution return a numpy array 9*9 of -1
    if solved_sudoku is None:
        return np.zeros((9,9))- 1

    return solved_sudoku


SKIP_TESTS = False

if not SKIP_TESTS:
    import time
    difficulties = ['very_easy','easy','medium','hard']
    difficulties = ['hard']
    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")

        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0


        for i in range(len(sudokus)):
            

            sudoku = sudokus[i].copy()
            print(f"This is {difficulty} sudoku number", i)
            print(sudoku)

            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()

            print(f"This is your solution for {difficulty} sudoku number", i)
            print(your_solution)

            print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print("Yes! Correct solution.")
                count += 1
            else:
                print("No, the correct solution is:")
                print(solutions[i])

            print("This sudoku took", end_time -
                  start_time, "seconds to solve.\n")
            #input()

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break
"""
#world Hardest sudoku
s=np.array([\
 [0, 2, 0, 0, 0, 6, 9, 0, 0],\
 [0, 0, 0, 0, 5, 0, 0, 2, 0],\
 [6, 0, 0, 3, 0, 0, 0, 0, 0],\
 [9, 4, 0, 0, 0, 7, 0, 0, 0],\
 [0, 0, 0, 4, 0, 0, 7, 0, 0],\
 [0, 3, 0, 2, 0, 0, 0, 8, 0],\
 [0, 0, 9, 0, 4, 0, 0, 0, 0],\
 [3, 0, 0, 9, 0, 2, 0, 1, 7],\
 [0, 0, 8, 0, 0, 0, 0, 0, 2]])

print(s)

start_time = time.process_time()
print(sudoku_solver(s))
end_time = time.process_time()
print("Time:", end_time - start_time)
"""


