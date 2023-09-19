import numpy as np
import time

def sudoku_solver(sudoku):
    solved_sudoku=[]
    allPossibleVals = []
    emptyPos=[]
    ### Checking if the array is valid
    for x in range (0,9):
        for y in range (0,9):
            if sudoku[x,y]!=0:
                if is_valid(sudoku,x,y) == False:
                    solved_sudoku = np.zeros((9,9))-1
                    return solved_sudoku
            else:
                emptyPos.append([x,y])
    invalid,allPossibleVals=update_all_possible(sudoku,emptyPos)
    
    changed=True
    rowdel=[[],[],[],[],[],[],[],[],[]]
    coldel=[[],[],[],[],[],[],[],[],[]]
    squaredel=[[],[],[],[],[],[],[],[],[]]

    
    while changed==True and invalid==False:
        invalid,allPossibleVals=update_all_possible(sudoku,emptyPos,rowdel,coldel,squaredel)
        changed,sudoku,emptyPos=set_all_singles(sudoku,emptyPos,allPossibleVals)
        if changed == True:
            continue

        sudoku,changed,rowdel,coldel,invalid=uniqueCandidate(sudoku,emptyPos,allPossibleVals,rowdel,coldel,invalid)
        emptyPos=UpdateEmpties(sudoku)
        if changed == True:
            continue

        rowdel,coldel,squaredel,changed,invalid=pairFinder(emptyPos,allPossibleVals,rowdel,coldel,squaredel)



    if invalid==True:
        solved_sudoku = np.zeros((9,9))-1
        return solved_sudoku

    
    solution=depthFirst(-1,emptyPos,allPossibleVals,sudoku,rowdel,coldel,squaredel)
    if solution == False:
        solved_sudoku = np.zeros((9,9))-1
        return solved_sudoku

    for x in range (0,9):
        for y in range (0,9):
            if sudoku[x,y]!=0:
                if is_valid(sudoku,x,y) == False:
                    solved_sudoku = np.zeros((9,9))-1
                    return solved_sudoku
    
    

    solved_sudoku=sudoku
    return solved_sudoku



def is_valid(aSudoku,x,y,valCheck=0,rowdel=[],coldel=[],squaredel=[]):


    bSudoku=aSudoku.copy()
    if valCheck == 0:
        sval=bSudoku[x,y]
    elif valCheck > 0:
        sval=valCheck
    row = bSudoku[x,:]
    row[y]=-10
    column = bSudoku[:,y]
    column[x]=-10

    sx=x - x%3
    sy=y - y%3
    square = bSudoku[ sx:sx+3 , sy:sy+3]
    square[x%3,y%3]=-10

    if sval in row or sval in column or sval in square:
        return False
    if len(rowdel)>0:
        for dels in rowdel[x]:
            if sval == dels[0] and [x,y] not in dels[1]:
                return False
    if len(coldel)>0:
        for dels in coldel[y]:
            if sval == dels[0] and [x,y] not in dels[1]:
                return False
    if len(squaredel)>0:
        for dels in squaredel[y-y%3+x//3]:
            if sval == dels[0] and [x,y] not in dels[1]:
                return False
    return True

def update_all_possible(sudoku,vacant,rowdel=[],coldel=[],squaredel=[]):

    mapPossible = []
    invalid=False
    for position in vacant:
        xPos=int(position[0])
        yPos=int(position[1])
        invalid,newlist=possible_vals(sudoku,xPos,yPos,rowdel,coldel,squaredel)
        if invalid:
            return invalid,mapPossible
        mapPossible.append(newlist)
    return invalid,mapPossible

def possible_vals(sudoku,x,y,rowdel=[],coldel=[],squaredel=[]):
    positionPossible =[]
    for checkval in range(1,10):
        if is_valid(sudoku,x,y,checkval,rowdel,coldel,squaredel):
            positionPossible.append(checkval)
    invalid=False
    if len(positionPossible)==0:
        invalid=True
            
    return invalid,positionPossible


def set_all_singles(sudoku,emptyPos,allPossibleVals):
    x=0
    y=0
    found=False
    emptyPoscopy=emptyPos.copy()
    for Vals in allPossibleVals:
        if len(Vals) == 1:
            sudoku[emptyPos[x][0],emptyPos[x][1]]=Vals[0]
            emptyPoscopy.pop(y)
            found=True
            #print("Single Set: ",emptyPos[x],Vals[0])
        else:
            y=y+1
        x=x+1
    return found,sudoku,emptyPoscopy

def uniqueCandidate(sudoku,emptyPos,allPossibleVals,rowdel,coldel,invalid):
    allSquares=[[],[],[],[],[],[],[],[],[]]
    sortedPos=[[],[],[],[],[],[],[],[],[]]

    b=False
    b=0
    sudokug=sudoku.copy()
    for x,y in emptyPos:
        try:
            allSquares[y-y%3+x//3].append(allPossibleVals[b].copy())
        except:
            return sudokug,True,rowdel,coldel,True
        sortedPos[y-y%3+x//3].append([x,y])
        b=b+1
    for k in range(0,9):
        if len(allSquares[k]) != 0:
            for j in range(1,10):
                eSet=[]
                for u in range(0,len(allSquares[k])):
                    if j in allSquares[k][u]:
                        eSet.append(sortedPos[k][u])
                if len(eSet)==1:##only 1 coordinate
                    sudokug[eSet[0][0],eSet[0][1]]=j
                    b=True
                    #print("Unique Candidate Found")
                elif len(eSet)==3:
                    if eSet[0][0] == eSet[1][0] and eSet[1][0] == eSet[2][0]:
                        if [j,eSet] not in rowdel[eSet[0][0]]:
                            rowdel[eSet[0][0]].append([j,eSet])
                            b=True
                            #print("tripple rowdel")
                    if eSet[0][1] == eSet[1][1] and eSet[1][1] == eSet[2][1]:
                        if [j,eSet] not in coldel[eSet[0][1]]:
                            coldel[eSet[0][1]].append([j,eSet])
                            b=True
                            #print("tripple coldel")
                elif len(eSet) == 2:
                    if eSet[0][0] == eSet[1][0]:
                        if [j,eSet] not in rowdel[eSet[0][0]]:
                            rowdel[eSet[0][0]].append([j,eSet])
                            b=True
                            #print("double rowdel")
                    if eSet[0][1] == eSet[1][1]:
                        if [j,eSet] not in coldel[eSet[0][1]]:
                            coldel[eSet[0][1]].append([j,eSet])
                            b=True
                            #print("double coldel")

                    

    return sudokug,b,rowdel,coldel,invalid




def UpdateEmpties(sudoku):
    emptyPos=[]
    for q in range(0,9):
        for w in range(0,9):
            if sudoku[q,w]==0:
                emptyPos.append([q,w])
    return emptyPos
    

def pairFinder(emptyPos,allPossibleVals,rowdel,coldel,squaredel):##double unique
    found=False
    invalid=False
    seen=[]
    seenindex=[]
    count=[]
    seen3=[]
    seen3index=[]
    seen3mode=[]

    
    for indexo in range(0,len(emptyPos)):
        if len(allPossibleVals[indexo])==3 and allPossibleVals[indexo] not in seen3:
            seen3.append(allPossibleVals[indexo])
            seen3index.append([emptyPos[indexo]])
            seen3mode.append([-1])
            count.append([0,0,0])
        elif len(allPossibleVals[indexo])==3:
            itsin=False
            g2=[i for i,val in enumerate(seen3) if val==allPossibleVals[indexo]]
            for g in g2:
                x1=seen3index[g][0][0]
                y1=seen3index[g][0][1]
                x2=emptyPos[indexo][0]
                y2=emptyPos[indexo][1]
                sq1=y1-y1%3+x1//3
                sq2=y2-y2%3+x2//3
                if x1==x2 or y1==y2 or sq1==sq2:
                    itsin=True
            if itsin==False:
                seen3.append(allPossibleVals[indexo])
                seen3index.append([emptyPos[indexo]])
                seen3mode.append([-1])
                count.append([0,0,0])
    

    for indexo in range(0,len(emptyPos)):


        if len(allPossibleVals[indexo]) == 2 and allPossibleVals[indexo] not in seen:
            seen.append(allPossibleVals[indexo])
            seenindex.append(emptyPos[indexo])
        elif allPossibleVals[indexo] in seen:
            uniqueVal=False
            g2=[i for i,val in enumerate(seen) if val==allPossibleVals[indexo]]
            for g in g2:
                x1=seenindex[g][0]
                y1=seenindex[g][1]
                x2=emptyPos[indexo][0]
                y2=emptyPos[indexo][1]
                
                if x1 == x2:
                    uniqueVal=True
                    if [seen[g][0],[seenindex[g],emptyPos[indexo]]] not in rowdel[x1]:
                        rowdel[x1].append([seen[g][0],[seenindex[g],emptyPos[indexo]]])
                        #print("pair rowdel 1")
                        found=True
                    if [seen[g][1],[seenindex[g],emptyPos[indexo]]] not in rowdel[x1]:
                        rowdel[x1].append([seen[g][1],[seenindex[g],emptyPos[indexo]]])
                        #print("pair rowdel 2")
                        found=True


                if y1 == y2:
                    uniqueVal=True
                    if [seen[g][0],[seenindex[g],emptyPos[indexo]]] not in coldel[y1]:
                        coldel[y1].append([seen[g][0],[seenindex[g],emptyPos[indexo]]])
                        #print("pair coldel 1")
                        found=True
                    if [seen[g][1],[seenindex[g],emptyPos[indexo]]] not in coldel[y1]:
                        coldel[y1].append([seen[g][1],[seenindex[g],emptyPos[indexo]]])
                        #print("pair coldel 2")
                        found=True
                
                sq1=y1-y1%3+x1//3
                sq2=y2-y2%3+x2//3
                
                if sq1==sq2:
                    uniqueVal=True
                    if [seen[g][0],[seenindex[g],emptyPos[indexo]]] not in squaredel[sq1]:
                        squaredel[sq1].append([seen[g][0],[seenindex[g],emptyPos[indexo]]])
                        #print("pair squaredel 1")
                        found=True
                    if [seen[g][1],[seenindex[g],emptyPos[indexo]]] not in squaredel[sq1]:
                        squaredel[sq1].append([seen[g][1],[seenindex[g],emptyPos[indexo]]])
                        #print("pair squaredel 2")
                        found=True

            if uniqueVal == False and len(allPossibleVals[indexo])==2:
                seen.append(allPossibleVals[indexo])
                seenindex.append(emptyPos[indexo])
        
        g2=[]
        inside=False
        if len(allPossibleVals[indexo]) == 2:
            for ui in range(0,len(seen3)):
                insidex=allPossibleVals[indexo][0] in seen3[ui]
                insidex=insidex and allPossibleVals[indexo][1] in seen3[ui]
                if insidex==True:
                    inside=True
                    g2.append(ui)
        else:
            inside=allPossibleVals[indexo] in seen3
            g2=[i for i,val in enumerate(seen3) if val==allPossibleVals[indexo]]


        if inside:
            for g in g2:
                x1=seen3index[g][0][0]
                y1=seen3index[g][0][1]
                x2=emptyPos[indexo][0]
                y2=emptyPos[indexo][1]
                if [x2,y2] not in seen3index[g]:
                    if x1 == x2:
                            count[g][0]=count[g][0]+1
                            seen3mode[g].append(0)
                            seen3index[g].append([x2,y2])

                    if y1 == y2:
                            count[g][1]=count[g][1]+1
                            seen3mode[g].append(1)
                            seen3index[g].append([x2,y2])
                    
                    sq1=y1-y1%3+x1//3
                    sq2=y2-y2%3+x2//3
                    
                    if sq1==sq2:
                            count[g][2]=count[g][2]+1
                            seen3mode[g].append(2)
                            seen3index[g].append([x2,y2])


    for indexo in range(0,len(count)):
        rowindexes=[seen3index[indexo][0]]
        colindexes=[seen3index[indexo][0]]
        squindexes=[seen3index[indexo][0]]

        for gen in range(0,len(seen3mode[indexo])):
            if seen3mode[indexo][gen]==0:
                rowindexes.append(seen3index[indexo][gen])
            if seen3mode[indexo][gen]==1:
                colindexes.append(seen3index[indexo][gen])
            if seen3mode[indexo][gen]==2:
                squindexes.append(seen3index[indexo][gen])


        x=seen3index[indexo][0][0]
        y=seen3index[indexo][0][1]
        sq=y-y%3+x//3

        if count[indexo][0] > 2 or count[indexo][1] > 2 or count[indexo][2] > 2:
            invalid = False
            #if any triple has more than 3 pairs then its invalid.
        if count[indexo][0]==2:
            if [seen3[indexo][0],rowindexes] not in rowdel[x]:
                rowdel[x].append([seen3[indexo][0],rowindexes])
                found=True
                #triple pair delete from row first number
            if [seen3[indexo][1],rowindexes] not in rowdel[x]:
                rowdel[x].append([seen3[indexo][1],rowindexes])
                found=True
                #triple pair delete from row second number
            if [seen3[indexo][2],rowindexes] not in rowdel[x]:
                rowdel[x].append([seen3[indexo][2],rowindexes])
                found=True
                #triple pair delete from row third number
            
        if count[indexo][1]==2:
            if [seen3[indexo][0],colindexes] not in coldel[y]:
                coldel[y].append([seen3[indexo][0],colindexes])
                found=True
                #triple pair delete from column first number
            if [seen3[indexo][1],colindexes] not in coldel[y]:
                coldel[y].append([seen3[indexo][1],colindexes])
                found=True
                #triple pair delete from column second number
            if [seen3[indexo][2],colindexes] not in coldel[y]:
                coldel[y].append([seen3[indexo][2],colindexes])
                found=True
                #triple pair delete from column third number
            
        if count[indexo][2]==2:
            if [seen3[indexo][0],squindexes] not in squaredel[sq]:
                squaredel[sq].append([seen3[indexo][0],squindexes])
                found=True
                #triple pair delete from square first number
            if [seen3[indexo][1],squindexes] not in squaredel[sq]:
                squaredel[sq].append([seen3[indexo][1],squindexes])
                found=True
                #triple pair delete from square second number
            if [seen3[indexo][2],squindexes] not in squaredel[sq]:
                squaredel[sq].append([seen3[indexo][2],squindexes])
                found=True
                #triple pair delete from square third number



    return rowdel,coldel,squaredel,found,invalid

def depthFirst(posIndex,emptyPos,allPossibleVals,sudoku,rowdel,coldel,squaredel):
    iteration=-1
    solution=False

    posIndex=posIndex+1
    if posIndex==len(allPossibleVals):
        return True
    for o in allPossibleVals[posIndex]:
        iteration=iteration+1
        if isinstance(o,int):
            q=o
        else:
            q=o[iteration]
        if is_valid(sudoku,emptyPos[posIndex][0],emptyPos[posIndex][1],q,rowdel,coldel,squaredel):
            sudoku[emptyPos[posIndex][0],emptyPos[posIndex][1]]=q
            solution=depthFirst(posIndex,emptyPos,allPossibleVals,sudoku,rowdel,coldel,squaredel)
            if solution==True:
                return True
            sudoku[emptyPos[posIndex][0],emptyPos[posIndex][1]]=0
    return False



        

def SortEmptyPos(EmptyPos,allPossibleVals):
    pass
"""
        for(int s = 2; s <= contacts.length; s++)
        {
            Contact sortMe = contacts[s - 1];
            int i = s - 2;
            while (i >= 0 && sortMe.compareTo(contacts[i])<0)
            {
                contacts[i+1] = contacts[i];
                i--;
            }
            contacts[i+1] = sortMe;
        }
"""


############# keep setting all the singular values then updating all possible and seeting again until there are no singulars left
############# after do the same for all unique values
############# redo for all single values

print("Start")
sudoku = np.array([[1,7,4,3,8,2,9,5,6],[2,9,5,4,6,7,1,3,8],[3,8,6,9,5,1,4,7,2],[4,6,1,5,2,3,8,9,7],[7,3,8,1,4,9,6,2,5],[9, 5, 2, 8, 7, 6, 3, 1, 4],[5, 2, 9, 6, 3, 4, 7, 8, 1],[6, 1, 7, 2, 9, 8, 5, 4, 3],[8, 4, 3, 7, 1, 5, 2, 6, 9]])
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
'''
print()
print("[[4. 2. 5. 8. 1. 6. 9. 7. 3.]")
print("[8. 9. 3. 7. 5. 4. 6. 2. 1.]")
print("[6. 1. 7. 3. 2. 9. 5. 4. 8.]")
print("[9. 4. 1. 6. 8. 7. 2. 3. 5.]")
print("[5. 8. 2. 4. 3. 1. 7. 6. 9.]")
print("[7. 3. 6. 2. 9. 5. 1. 8. 4.]")
print("[2. 7. 9. 1. 4. 8. 3. 5. 6.]")
print("[3. 5. 4. 9. 6. 2. 8. 1. 7.]")
print("[1. 6. 8. 5. 7. 3. 4. 9. 2.]]")
'''

SKIP_TESTS = False

if not SKIP_TESTS:
    import time
    difficulties = ['very_easy', 'easy', 'medium', 'hard']
    difficulties = [ 'hard']

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")
        
        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")
        
        count = 0
        lens=len(sudokus)
        for id in range(0,lens):#(len(sudokus)):
            i=id
            sudoku = sudokus[i].copy()
            print(f"This is {difficulty} sudoku number", i)
            print(sudoku)
            
            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()
            
            print(f"This is {difficulty} sudoku number", i)
            print(sudoku)

            print(f"This is your solution for {difficulty} sudoku number", i)
            print(your_solution)
            
            print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print("Yes! Correct solution.")
                count += 1
            else:
                print("No, the correct solution is:")
                print(solutions[i])
                kl=0
                ol=0
                fkl=0
                for op in range(0,9):
                    for dp in range(0,9):
                        if your_solution[op,dp]!=0:
                            if sudoku[op][dp]==0:
                                fkl=fkl+1
                            kl=kl+1
                            if your_solution[op][dp]==solutions[i][op][dp]:
                                ol=ol+1
                print("Match Score: ",ol,"/",kl," Empties: ",fkl)
            


            print("This sudoku took", end_time-start_time, "seconds to solve.\n")
            #input()


        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break
        