
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
    

    rowModulo, columnModulo = math.floor(row/3) * 3, math.floor(column/3) * 3

    for rowI in range(rowModulo, rowModulo+3):
        for columnI in range(columnModulo, columnModulo+3):
            if rowI != row and columnI != column:
                if(sudoku[rowI][columnI] == number):
                    return False

    # Second check in the same Row
    for yx in range(0, 9):
        if yx != column:
            if sudoku[row][yx] == number:
                return False

    # Third Checking in the Same column
    for y in range(0, 9):
        if y != row:
            if sudoku[y][column] == number:
                return False

    return True


def oneWayCoord(sudoku,sudoku_Poss_Actions):
    """
    Function to check for unique values where we can only place at this place
    """
    testChangeSudoku = False

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
                    print("Single Hidden")
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
                        for ijx in range(0,9):
                            if (testValue,ijx) not in value:
                                if sudoku[testValue][ijx] == 0:
                                    if index in sudoku_Poss_Actions[testValue][ijx]:
                                        print("Double Column ")
                                        testChangeSudoku = True
                                        sudoku_Poss_Actions[testValue][ijx].remove(index)
                    
                    #Can only be in this Row
                    testValue = value[0][1]
                    for tuplesPoss in value:
                        if tuplesPoss[1] != testValue:
                            testValue = tuplesPoss[1]
                            break
                    
                    if testValue == value[0][1]:
                        for ijx in range(0,9):
                            if (ijx,testValue) not in value:
                                if sudoku[ijx][testValue] == 0:
                                    if index in sudoku_Poss_Actions[ijx][testValue]:
                                        print("Double Row")
                                        testChangeSudoku = True
                                        sudoku_Poss_Actions[ijx][testValue].remove(index)


    return testChangeSudoku

def onePossValue(sudoku,sudoku_Poss_Actions):
    """
    Function That place one possibel values
    """
    test = False
    for i in range(0,9):
        for j in range(0,9): 
            if isinstance(sudoku_Poss_Actions[i][j], list):
                if len(sudoku_Poss_Actions[i][j]) == 1:
                    test = True
                    print("Single Possible")
                    sudoku[i][j] = sudoku_Poss_Actions[i][j][0]
                    updatePossActions(sudoku, sudoku_Poss_Actions, i, j)
    return test

def nakedPairTriple(sudoku,sudoku_Poss_Actions):
    """
    This Function is a constraint to remove possible values using Naked Pair and Triple Techniques
    and place 1 possible value
    """
    test = False
    dictPair = {}


    for i in range(0,9):
        for j in range(0,9): 

            if sudoku[i][j] == 0:
                
                # Two possible value we place it in our Pair Dict
                if len(sudoku_Poss_Actions[i][j]) == 2:
                    dictPair[(i,j)] = sudoku_Poss_Actions[i][j]

            ## Triplet Naked Algorithm
            # Checking for same row
            if j <= 6:
                if sudoku[i][j] == 0 and sudoku[i][j+1] == 0 and sudoku[i][j+2] == 0:
                    length1 =  len(sudoku_Poss_Actions[i][j])
                    length2 =  len(sudoku_Poss_Actions[i][j+1])
                    length3 =  len(sudoku_Poss_Actions[i][j+2])
                    setValues = set()
                    if (length1 == 3 or length1 == 2) and (length2 == 3 or length2 == 2) and (length3 == 3 or length3 == 2):
                        for x1 in sudoku_Poss_Actions[i][j]:
                            setValues.add(x1)
                        for x2 in sudoku_Poss_Actions[i][j+1]:
                            setValues.add(x2)
                        for x3 in sudoku_Poss_Actions[i][j+2]:
                            setValues.add(x3)

                    if len(setValues) == 3:
                        listValues = list(setValues)
                        for t in range(0,9):
                            if t == j or t == j+1 or t == j+2:
                                continue
                            if sudoku[i][t] == 0:
                                print("Triple Row")
                                if listValues[0] in sudoku_Poss_Actions[i][t]:
                                    sudoku_Poss_Actions[i][t].remove(listValues[0])
                                    test = True
                                if listValues[1] in sudoku_Poss_Actions[i][t]:
                                    sudoku_Poss_Actions[i][t].remove(listValues[1])
                                    test = True
                                if listValues[2] in sudoku_Poss_Actions[i][t]:
                                    sudoku_Poss_Actions[i][t].remove(listValues[2])
                                    test = True

            # Checking for same column
            if i <= 6:
                if sudoku[i][j] == 0 and sudoku[i+1][j] == 0 and sudoku[i+2][j] == 0:
                    length1 =  len(sudoku_Poss_Actions[i][j])
                    length2 =  len(sudoku_Poss_Actions[i+1][j])
                    length3 =  len(sudoku_Poss_Actions[i+2][j])
                    setValues = set()
                    if (length1 == 3 or length1 == 2) and (length2 == 3 or length2 == 2) and (length3 == 3 or length3 == 2):
                        for x1 in sudoku_Poss_Actions[i][j]:
                            setValues.add(x1)
                        for x2 in sudoku_Poss_Actions[i+1][j]:
                            setValues.add(x2)
                        for x3 in sudoku_Poss_Actions[i+2][j]:
                            setValues.add(x3)

                    if len(setValues) == 3:
                        listValues = list(setValues)
                        for t in range(0,9):
                            if t == i or t == i+1 or t == i+2:
                                continue
                            if sudoku[t][j] == 0:
                                print("Triple Column")
                                if listValues[0] in sudoku_Poss_Actions[t][j]:
                                    sudoku_Poss_Actions[t][j].remove(listValues[0])
                                    test = True
                                if listValues[1] in sudoku_Poss_Actions[t][j]:
                                    sudoku_Poss_Actions[t][j].remove(listValues[1])
                                    test = True
                                if listValues[2] in sudoku_Poss_Actions[t][j]:
                                    sudoku_Poss_Actions[t][j].remove(listValues[2])
                                    test = True
        


    ## Pairs Algorithm
    for iValDictPair,valueDictPair in dictPair.items():
        for index,valueItem in dictPair.items():
            if iValDictPair != index:
                if valueDictPair == valueItem:

                    #There is a pair where they share a row than we update Column
                    if index[0] == iValDictPair[0]:
                        for i in range(0,9):
                            if i == index[1] or i == iValDictPair[1]:
                                continue
                            if sudoku[index[0]][i] == 0:
                                print("Naked Pair Column")
                                if valueItem[0] in sudoku_Poss_Actions[index[0]][i]:
                                    sudoku_Poss_Actions[index[0]][i].remove(valueItem[0])
                                    test = True
                                if valueItem[1] in sudoku_Poss_Actions[index[0]][i]:
                                    sudoku_Poss_Actions[index[0]][i].remove(valueItem[1])
                                    test = True
                    
                    #There is a pair where they share a Column than we update Row
                    if index[1] == iValDictPair[1]:
                        for j in range(0,9):
                            if j == index[0] or j == iValDictPair[0]:
                                continue
                            if sudoku[j][index[1]] == 0:
                                print("Naked Pair Row")
                                if valueItem[0] in sudoku_Poss_Actions[j][index[1]]:
                                    sudoku_Poss_Actions[j][index[1]].remove(valueItem[0])
                                    test = True
                                if valueItem[1] in sudoku_Poss_Actions[j][index[1]]:
                                    sudoku_Poss_Actions[j][index[1]].remove(valueItem[1])
                                    test = True

                    #Now Checking to see if there is a Pair in the same square
                    rowModulo1, columnModulo1 = math.floor(index[0]/3) * 3, math.floor(index[1]/3) * 3
                    rowModulo2, columnModulo2 = math.floor(iValDictPair[0]/3) * 3, math.floor(iValDictPair[1]/3) * 3
                    if rowModulo1 == rowModulo2 and columnModulo1 == columnModulo2:

                        for rowI in range(rowModulo1, rowModulo1+3):
                            for columnI in range(columnModulo1, columnModulo1+3):
                                if (rowI,columnI) != index and (rowI,columnI) != iValDictPair:
                                    if sudoku[rowI][columnI] == 0:
                                        print("Naked Pair Square")
                                        if valueItem[0] in sudoku_Poss_Actions[rowI][columnI] :
                                            sudoku_Poss_Actions[rowI][columnI] .remove(valueItem[0])
                                            test = True
                                        if valueItem[1] in sudoku_Poss_Actions[rowI][columnI] :
                                            sudoku_Poss_Actions[rowI][columnI].remove(valueItem[1])
                                            test = True 


    return test


def findNextPosition(sudoku, sudoku_PossibleActions):

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
        return True

    # Loop through the possible values
    for x in sudoku_PossibleActions[row][column]:
        result = constraintsCheck(sudoku, row, column, x)

        if result == True:
            sudoku[row, column] = x
           
            test = search_backTrack(sudoku, sudoku_PossibleActions)

            if test == True:
                return True

        # Updating back our possible values after reaching a dead end
        sudoku[row, column] = 0

    return False

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
                #rand.shuffle(sudoku_PossibleActions[rowSudoku][columnSudoku])
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
        
        #First Update One possible values
        testChangedSudoku1 = onePossValue(sudoku_copy,sudoku_PossibleActions)
        if testChangedSudoku1 == True:
            continue

        testChangedSudoku2 = oneWayCoord(sudoku_copy,sudoku_PossibleActions)
        #Naked Pair and Triple and one possible value
        if testChangedSudoku2 == True :
            continue

        #Hidden Single and Double Row and Colum
        testChangedSudoku3 = nakedPairTriple(sudoku_copy,sudoku_PossibleActions)
        if testChangedSudoku3 ==  True:
            continue

    
        changedSudoku = True
    

    #print(sudoku_PossibleActions)
    # calling our BackTracking Search Algorithm
    solved_sudoku = search_backTrack(sudoku_copy, sudoku_PossibleActions)
    
    # If there is no solution return a numpy array 9*9 of -1
    if solved_sudoku is False:
        return np.zeros((9,9))- 1

    return sudoku_copy

SKIP_TESTS = True

if not SKIP_TESTS:
    import time
    difficulties = ['very_easy','easy','medium']
    difficulties = ['hard']
    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")

        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0


        for i in range(len(sudokus)):
        #for i in range(8,9):
            

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
            
            
            input()

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break

#world Hardest sudoku
skip_Hardest = False
if skip_Hardest != True:
    import time


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



sudoku=np.array([\
 [8, 0, 0, 0, 0, 0, 0, 0, 0],\
 [0, 0, 3, 6, 0, 0, 0, 0, 0],\
 [0, 7, 0, 0, 9, 0, 2, 0, 0],\
 [0, 5, 0, 0, 0, 7, 0, 0, 0],\
 [0, 0, 0, 0, 4, 5, 7, 0, 0],\
 [0, 0, 0, 1, 0, 0, 0, 3, 0],\
 [0, 0, 1, 0, 0, 0, 0, 6, 8],\
 [0, 0, 8, 5, 0, 0, 0, 1, 0],\
 [0, 9, 0, 0, 0, 0, 4, 0, 0]])

#print(sudoku_solver(sudoku))
print()

start_time = time.process_time()
print(sudoku_solver(sudoku))
end = time.process_time()
print(end-start_time)