# **Sudoku Solver**


In my sudoku solving algorithm, I decided to take the approach of using backtracking with constraint propagation. I decided to further reduce the possible actions of each cell using solving techniques a human would use to reduce the run time.

>Backtracking is the process of using recursive calls to solve a puzzle by building a solution gradually. It iteratively fills in vacancies with values and eliminates possible actions that do not progress towards the solution through the use of defined constraints. Constraints also highlight dependencies between vacancies allowing the algorithm to quickly determine if a value cannot be positioned there due to an interference/conflict. Eventually, by filling in non-conflicting values into each vacancy, the algorithm either comes to a solution or a dead-end. In the case of a solution, the puzzle is complete, however, when a dead-end is found, the algorithm backtracks until it finds another non-conflicting possible value to replace a value in a previous vacancy.

From this definition, we can deduce that the more possible values and vacancies, the longer the average run time of backtracking will be. Thus, I've decided to eliminate as many vacancies as possible and further eliminate possible values in every vacancy.

|**Eliminate Vacancies**       |    **Reduce Possible Values**             |
|------------------------------|-------------------------------------------|
|Single Set/Naked Single       |Single Set / Naked Single                  |
|Unique Candidate/Hidden Single|Unique Candidate / Hidden Single           |
|                              |Unique (Row/Column) Delete / Pointing Pairs|
|                              |Naked Pairs / Naked Triples                |

<br>

A further justification for eliminating possible values is to spot invalid puzzles, where a cell wouldn't have any possible values. This means there is no possible way a solution can be reached as the cell cannot be filled with any value that gives rise to a solution.

By eliminating vacancies, also reduces possible values in other cells. For example, if a vacancy at the first column second row is destined to be a value - _hence we fill it in with its defined value_ - it eliminates that value as a possibility from all vacancies in the second row, first column and first square.

<br>

### Stage 1 of Eliminating Possible Values:
The first step in eliminating possible values is the most intuitive step. It involves eliminating possible values that can fit into a vacant cell by looking at the surrounding cells that it is dependent on. This means all non-zero/non-vacant cells in the same row, column and 3 by 3 square. This reduces checking each if every value is possible and creates new opportunities for the more advanced algorithms to eliminate vacancies and numbers.

### Stage 2 - Eliminating Single Naked.
A naked single is a vacant cell that only has a single possible value. Logically, if this cell can possibly only have that number and no others from 1 to 9, then it is destined for the single possibility for that cell to be the actual value for the cell. This eliminates a cell as it is set in stone, and above this, it reduces the possible values for its surrounding values. At the second stage, my algorithm sets all the naked singles.

### Stage 3 part 1 - Eliminating Unique Candidates.
A unique candidate, otherwise known as a hidden single, is a number that can exclusively be applied to only a single cell within a square - but cannot be applied to any other cell within that square. This means, say, for instance, the middle cell of a square has multiple possible values and one of those possible values can only be applied to the middle square and not any other, then it is most logical for that middle square to be that unique value. At the third stage of elimination, my program looks for unique candidates to eliminate the cell and set the value.

### Stage 3 part 2 - Eliminating Pointing Pairs and Triples.
The format of finding pointing pairs follows a similar structure to stage 3 part 1, so to reduce complexity, I embedded pointing pairs inside a unique candidate. Pointing pairs uses the idea if a number can only be put in two/three cells within a square, but all those numbers align in a single row/column, then regardless of where it is placed, the numbers outside this square on the same corresponding row/column (depending on the alignment) will eventually have that value eliminated from their possible values. For example, if the top-left square had a value that can only be positioned within the top-right cell or the top-left cell, for the case the value is positioned on the top-right cell, every cell on the first row (excluding itself) will have this value eliminated from there possible states. For the second case of the value falling on the top-left cell, everything on the first row (excluding itself) will have this value eliminated from the cells possible states. This value is destined to be one or the other, so regardless, looking ahead we can determine that this entire row (excluding the top-right and top-left call of the top-left square) will eventually have the value eliminated from their possible states. Therefore, my algorithm finds these pair/triples and eliminates the possible values in other cells immediately.

### Stage 4 - Eliminating Naked Pairs and Triples.
A naked pair is when two cells have the same two possible states and are in the same row/column/square. Whatever one it is in, my algorithm eliminates that pair of numbers from all the other cells of that row/column/square aside from the pair itself. The theory behind this is that since the two values have two cells that exclusively have them both if one of the values is placed within one, it eliminates that same value in the other paired cell (because they are in the same row/column/square) leaving this other cell with one possible value - so a single set occurs. The same happens for the other value, just the opposite value elimination, so regardless of the combination, these two cells must contain either of both values. Using this logic we can introduce a pair elimination in that same square/row/column since that value can not be placed in any other cell other than the pair.
\
A naked triple uses the same logic however the only difference is that a triple has more ways of being defined. All three pairs can have the same three possible values OR two possible values that fall within the three and do not make a pair. This may sound confusing but a simple example may help:
\
If the possible values of three cells within the same square/row/column were:
|Possible Values|Triple?|
|---|---|
|[1,2,3] [1,2,3] [1,2,3]|True, all cells have the same three values.| 
|[1,2,3] [2,3,4] [2,3,4]|False.|
|[1,5,9] [1,5] [5,9]|True, the cells with two possible states do not form a pair <br>and they are a subset of the cell with three possible values.|
|[1,5,9] [1,5] [1,5]|False, because the cells with two possible states form a pair <br>so they would eliminate from the cell with three possible values.|
|[2,3,7] [2,3,7] [3,7]|True, the values can be shared between the three cells and not <br> eliminate any values within each other.|
### Looping through the stages.
All these stages are looped through iteratively from stage 1 to 4. If any of the stages makes a change to the possible values or the sudoku cells, the algorithm skips the rest of the stages and restarts the cycle from stage 1. If there are no changes in any of the stages, the algorithm marks the sudoku as fully optimised and finished filling in values using backtracking. If any of the stages realises an illogical state i.e. a cell with no possible states, the algorithm terminates and outputs the invalid sudoku condition.
\
\
The justification of using this loop is that when any of the stages make an elimination or a change, it will open up the previous stages to create more eliminations as essentially they are operating on a newly modified sudoku. The stages are also designed to rank in order from the most impactful changes to the least impactful changes - 1 being the most impactful. Therefore by restarting the loop for every change we are technically finding the quickest way to keep eliminating values. This improves run time.

### Backtracking / Depth-First Search
From the remaining possible values, my backtracking algorithm uses a depth-first search with constraints. The depth-first algorithm functions like a normal algorithm, iterating through the possible states and filling them all in from start to end. However, the modification is, every time it sets a state, it uses the valid checker (stage 1) to determine whether the state can exist in that position. if it cannot due to a previous state that was set by backtracking, then this value will not be set. As opposed to setting the entire sudoku, then checking the validity, this reduces the number of states the algorithm has to visit. Logically this makes sense because if we imagined a tree with p amount of cells with q amount of possible states, the tree would have q^p leaves. However, each time one value is set, it eliminates other possible routes the tree could take and this is the logic behind using the constraint.
\
\
This function could have been improved and reduce time complexity by applying the stage 1-5 every time a value is set, but it would greatly change the design of my algorithm, and the elimination process resulted in all algorithms being solved in around 0.1 seconds. The performance gains to further reduce the solve time minimally were not worth the added complexity.


## **Functions and Important Variables**
<br>

## Functions:
---
### sudoku_solver()

1. Given the parameter of unsolved sudoku.
1. Checks if every existing value in the sudoku is valid using [is_valid()](#is_valid)
1. Makes note of the location of all zeros (vacant positions) in a variable called [emptyPos](#emptyPos).
1. Calls [update_all_possible](#update_all_possible) to create an array of an array of all possible values that fit into each cell and is stored in [allPossibleVals](#allPossibleVals)
<br>
<br>

1. Repeatedly loops trying out the following functions until there is an iteration where none of the functions makes any changes or the algorithm discovers an invalid state.

    1. [update_all_possible()](#update_all_possible) - _to re-evaluate the possible values with the new state/updated sudoku._

    1. [set_all_singles()](#set_all_singles) - _sets the cells which have only one possibility with its only possible value._
    1. [uniqueCandidate()](#uniqueCandidate) - _sets any cell that contains a value that all cells in its square do not have. It means that the value couldn't have gone anywhere else. It also eliminates values using pointing pairs._
    1. [pairFinder()](#pairFinder) - _eliminates possible values by finding cells that are in pairs or triplets_
<br>
<br>

1. If the **invalid** flag is **True**, then this function returns a 9 by 9 sudoku puzzle filled with "-1" - the "no solution" output.

1. With the optimised possible values and updated puzzle, [depthFirst()](#depthFirst) is called and if it finds that the puzzle is unsolvable, it returns the 9 by 9 filled with "-1". However, if every value is valid and the puzzle is solved, it returns the solved solution.


---
### is_valid()
1. Checks if the function has been called in co-ordinate checking mode or value checking mode, and assigns the corresponding value to the checking part.
1. Collectes all the items in the variables row, square and column.
1. Checks if the value being checked exists within the row, column and square, return false if it is.
1. Uses [rowdel](#rowdel), [coldel](#coldel) and [squaredel](#squaredel) to evaluate if the item needs to be eliminated because it contradicts with an elimination.
1. If it contradicts, it returns False.
1. Otherwise, it returns True.
---
### update_all_possible()
1. Creates a map to store every single array of possible values.
1. Goes through every vacant position from [emptyPos](#emptyPos) and applies the [possibleVals()](#possibleVals) algorithm to return an array of all the possible values at that position.
    1. If there arent any vacant positions in that empty position co-ordinate, it means that the sudoku is contradictory and invalid, so the function returns an invalid to the main function.
    1. It adds the array of possible values to the map if it is not an invalid case.

---
### possibleVals()
1. Iterates 1 through till 9, testing every value using [is_valid()](#is_valid) in value check mode.
1. If True is returned, the value is added to a list.
1. If by the end of the loop this loop is length 0, the algorithm flags an invalid state - as no number can go in that co-ordinate.
---
### setAllSingles()

This function goes through all the possible values [allPossibleVals](#allPossibleVals), and where there is a possible value array with the length of 1, this sets it in the sudoku (and changes found to True to denote this algorithm made a change). This allows us to set a value in sudoku because there isn't any other number that can go in that vacancy.

---
### uniqueCandidate()

This algorithm uses the allPossibleVals array to create a set of occurrences of each number (1-9) within each square. Whenever a number only has 1 occurrence, it means it must go there and cannot go anywhere else. Therefore, we can set this value in the main sudoku.
\
Using the same data, we can easily find pointing pairs to eliminate numbers in the same row or column. The way this works is by looking if a value can only go in one row/one column within a square. Since that value is forced to be in that row/column, we can safely eliminate that value from all the possible values in that same row/column. It uses rowdel or coldel to establish a row or column elimination.

---
### pairFinder()

This function goes through all the possible values [allPossibleVals](#allPossibleVals), looks for values within the same square, same row or same column that have the same set of possible values. However, the implementation is much more difficult and complex. To find naked pairs, all that needs to happen is matching the possible values of length of 2 that are on the same row, column or square (i.e. both sets interact with each other). If they interact with each other then a pair is formed.
\
For a triple, the two other possible values do not have to exactly contain the same possible values, they can contain a subset of the items in the array. When a pair or triple is found, they are added to the corresponding elimination variable ([rowdel](#rowdel), [coldel](#coldel) and [squaredel](#squaredel)). Using these variables, this pair finding algorithm can make square, row and column eliminations easily.

---
### depthFirst()

This algorithm uses all the positions in [emptyPos](#emptyPos) and declares them all as the "empty spaces" that we are going to do our search on. It uses [allPossibleVals](#allPossibleVals) as an optimised version to see what actions are possible to fill the vacancies. In comparison to filling every empty space from 1 to 9, this reduces the total amount of steps greatly. Essentially from here, it is a depth-first search where it fills in a vacancy, goes to the next empty space and fills it with a valid state. This repeats until the puzzle is complete or an invalid state is reached. In the case of an invalid state, the program backtracks to a position where there is a different possibility, and depth-first carries on from there. If it is such that the root/first search node has run out of possible values that aren't invalid, the search recognises that the sudoku given is invalid and the algorithm returns a false.

---
<br>

## Variables:
---

### emptyPos
- Holds the **co-ordinates/positions** of every **vacancy/zero** of the sudoku puzzle.
- It updates when my algorithm makes a permanent change to the puzzle (doesn't update during backtracking).
---
### allPossibleVals
- Each cell has an array of possible values.
- allPossibleVals stores all these arrays in an array.

*This works by mapping every co-ordinate in emptyPos to the array of possible values. Essentially this variable and emptyPos will have the same amount of items within them where the location that these possible values belong in emptyPos and this stores all possible actions that can be applied to that cell. The reason why I chose this data structure format is that it accommodates a lot of the eliminations used later and makes accessing the array quick.*

---
### rowdel
\
"rowdel" is a multidimensional array that contains values that need to be eliminated from a row and the cells on that row that fall exception to this elimination.

This variable is formatted such that the first dimension defines the row. Therefore to search if an elimination needs to be performed on a cell you'd find the values that apply to it by using the Y-coordinate as the first dimension when calling the variable - _"rowdel [ y-coordinate ]"_

The second dimension defines elimination blocks. Elimination blocks consist of two things: the value to be eliminated and the cell co-ordinate that are exempt from the elimination. A cell can be exempt from elimination if it defined the elimination. This restricts pair eliminations from eliminating themselves.

\
Format:
```python
rowdel[rowNumber]=
    #Exception co-ordinates for the delete.
    [Co-ordinate1Exception1, Co-ordinate1Exception2,...],[valueToEliminate1],
    [Co-ordinate2Exception1, Co-ordinate2Exception2,...],[valueToEliminate2],
    ... #Elimination blocks ^^^
```
---
### coldel
\
"coldel" is a multidimensional array that contains values that need to be eliminated from a column and the cells on that column that fall exception to this elimination.

This variable is formatted such that the first dimension defines the column. Therefore to search if an elimination needs to be performed on a cell you'd find the values that apply to it by using the x co-ordinate as the first dimension when calling the variable - _"coldel [ x-coordinate ]"_

The second dimension defines elimination blocks. Elimination blocks consist of two things: the value to be eliminated and the cell co-ordinate that are exempt from the elimination. A cell can be exempt from elimination if it defined the elimination. This restricts pair eliminations from eliminating themselves.

\
Format:
```python
coldel[colNumber]=
    #Exception co-ordinates for the delete.
    [Co-ordinate1Exception1, Co-ordinate1Exception2,...],[valueToEliminate1],
    [Co-ordinate2Exception1, Co-ordinate2Exception2,...],[valueToEliminate2],
    ... #Elimination blocks ^^^
```
---
### squaredel
\
"squaredel" is a multidimensional array that contains values that need to be eliminated from a square and the cells on that square that fall exception to this elimination.

This variable is formatted such that the first dimension defines the square. However there is a slight twist, the squares are numbered from 1 to 9 using a "left to right" line by line naming convention. Therefore, square one is the top-left square, the top-middle is two, top-right is three. The middle row left is four, the square to its right is five and so on. A simple algorithm can be used to calculate the square using co-ordinates:

>y = y co-ordinate
\
>x = x co-ordinate
\
\
>numberOfSquare = y - y%3 + x//3

Therefore to search if an elimination needs to be performed on a cell you'd find the values that apply to it by using the formula to calculate the square value and use it as a parameter in the first dimension when calling the variable - _"squaredel [ numberOfSquare ]"_

The second dimension defines elimination blocks. Elimination blocks consist of two things: the value to be eliminated and the cell co-ordinate that are exempt from the elimination. A cell can be exempt from elimination if it defined the elimination. This restricts pair eliminations from eliminating themselves.

\
Format:
```python
squaredel[numberOfSquare]=
    #Exception co-ordinates for the delete.
    [Co-ordinate1Exception1, Co-ordinate1Exception2,...],[valueToEliminate1],
    [Co-ordinate2Exception1, Co-ordinate2Exception2,...],[valueToEliminate2],
    ... #Elimination blocks ^^^
```
---