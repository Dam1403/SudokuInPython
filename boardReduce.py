"""
Douglas May 



"""





"""
This is the easiest technique to apply by eye – and the one that most people use first when completing paper Sudoku puzzles.

Choose a row, column or box, and then go through each of the numbers that hasn’t already been placed.
Because of other placements,the positions where you could place that number will be limited.
Often there will be two or three places that are valid, but if you’re lucky, there’ll only be one.
If you’ve narrowed it down to only one valid place where you can put the number…
you can fill that number straight in, since it can’t go anywhere else!
"""

def singlePosition(board,penMarks):
    # QUAD REDUCE
    for quadNo in range(0,9):
        quad = board.getQuadrant(quadNo)
        row = board.getRow(quadNo)
        col = board.getColumn(quadNo)
        reduceQuad(penMarks,board,quadNo,quad)
        reduceRow(penMarks,board,quadNo,row)# Row Num
        reduceCol(penMarks,board,quadNo,col)# Col Num




"""
If you look within a box, and find that all of the places where you can put a particular number lie along a single line,
then you can be sure that wherever you put the number in that box, it has to be on the line.

Even if you don’t know exactly where to put the number yet, you can use this knowledge!
You know that none of the other positions on that line (in the other two boxes)
could contain that number, so you can remove those as candidates!

    arguments:
        board - the SudokuBoard
        penMarks - The dictionary containing pencil marks

    return:
        nothing

"""

def candidateLine(board,penMarks):
    ROW_COORD = 1
    COL_COORD = 2

    LOCATION_1 = 0
    LOCATION_2 = 1
    LOCATION_3 = 2
    for num in ['1','2','3','4','5','6','7','8','9']:
        for quadNo in range(0,9):
            coords = board.getQuadCoords(quadNo)
            possLocs = []
            for row in range(0,3):
                adjRow = row + coords[0]
                for col in range(0,3):
                    adjCol = col + coords[1]
                    marks = penMarks[(adjRow,adjCol)]
                    if marks == None:
                        continue
                    if  num in marks:
                        possLocs = possLocs + [(num,adjRow,adjCol)]
            pLen = len(possLocs)
            if pLen == 2:
                loc1R = possLocs[LOCATION_1][ROW_COORD]
                loc1C = possLocs[LOCATION_1][COL_COORD]
                loc2R = possLocs[LOCATION_2][ROW_COORD]
                loc2C = possLocs[LOCATION_2][COL_COORD]
                
                if loc1R == loc2R:
                    reduceRow(penMarks,board,loc1R,[str(num)],quadNo)
                if loc1C == loc2C:
                    reduceCol(penMarks,board,loc1C,[str(num)],quadNo)
                    
            if pLen == 3:
                loc1R = possLocs[LOCATION_1][ROW_COORD]
                loc1C = possLocs[LOCATION_1][COL_COORD]
                loc2R = possLocs[LOCATION_2][ROW_COORD]
                loc2C = possLocs[LOCATION_2][COL_COORD]
                loc3R = possLocs[LOCATION_3][ROW_COORD]
                loc3C = possLocs[LOCATION_3][COL_COORD]
                if loc1R == loc2R == loc3R:
                    reduceRow(penMarks,board,loc1R,[str(num)],quadNo)
                if loc1C == loc2C == loc3C:
                    reduceCol(penMarks,board,loc1C,[str(num)],quadNo)
                            
"""
    
    Removes all pencil marks of all candidates within a given list of candidates
    From A Quadrant.

    arguments:
        penMarks = penMarks dictionary
        board = SudokuBoard Object
        quadNo = quadrant Number
        reduceArray = A list of candidates to be removed

    uses:
        bigMarks = a list of all pencilMark lists within the quad
        marks = the pencil marks for a specific tile on the board
        quadIso = The isolated candidates within the quad.
        bigMarks - a list of all pencilmark lists

    return:
        None
    
"""

def reduceQuad(penMarks,board,quadNo,reduceArray):
    coords = board.getQuadCoords(quadNo)
    bigMarks = []
    
    ROW_COORD = 0
    COL_COORD = 1

    ISO_ELEMENT = 0
    ISO_POSITION = 1
    
    for row in range(0,3):
        adjRow = row + coords[ROW_COORD]
        for col in range(0,3):
            adjCol = col + coords[COL_COORD]
            marks = penMarks[(adjRow,adjCol)]

            bigMarks += [marks]
            if marks == None:
                continue       
            
            for reduce in reduceArray:
                reduceCoords(penMarks,adjRow,adjCol,reduce)
    quadIso = reduceOccurences(bigMarks)
    for iso in quadIso:
        isoCrd = numToQuadCoords(iso[ISO_POSITION])
        isoRow = isoCrd[ROW_COORD]+coords[ROW_COORD]#convert quadrant relative position to board relative position
        isoCol = isoCrd[COL_COORD]+coords[COL_COORD]
        penMarks[(isoRow,isoCol)] = [iso[ISO_ELEMENT]]



"""
Currently used exclusively by the reduce quad Function.
takes in a single number (0,8) and converts it into quadCoordinates.
For Example. Number Five would be at coordinates (1,1)
012
345
678

    arguments:
        num - the number to be converted

    return:
        quadrant relative position
"""
def numToQuadCoords(num):
    coords = [0,0]
    while num != 0:
        coords[1] = coords[1] + 1
        if coords[1] == 3:
            coords[0] = coords[0] + 1
            coords[1] = 0
        num -= 1
    return (coords[0],coords[1])


"""
Single Position:
    https://www.sudokuoftheday.com/techniques/single-position/

This is the easiest technique to apply by eye 
and the one that most people use first when completing paper Sudoku puzzles.

Choose a row, column or box, and then go through each of the numbers that hasn’t already been placed.
Because of other placements, the positions where you could place that number will be limited.
Often there will be two or three places that are valid, but if you’re lucky, there’ll only be one.
If you’ve narrowed it down to only one valid place where you can put the number…
you can fill that number straight in, since it can’t go anywhere else!

This function checks a specific group of pencilmarks(size 9)
for any candidates that appear only once within the group


arguments - a list of pencilmark lists

banned - is the set that records which candidates have been encountered more than once
unique - is the list that stores the candidates that appear only once
done - is the list that contains the finished tuples for the calling function
locations - records the index in the allMarks list that the candidate was encountered
    Because this function doesn't know who called it (reduceRow,reduceCol or reduceQuad)
    so the calling function handles the location accordingly

returns - a list of tuples (int(1,9)element, int(0,8)location)
    

"""
def reduceOccurences(allMarks):
    banned = set()
    locations = dict()
    unique = []
    done = []
    for location in range(0,9):
        marks = allMarks[location] # Get a pencilmarks list
        if marks == None:
            continue
        for mark in marks:# Check the individual marks
            if mark not in unique and mark not in banned:
                unique += [mark] # Add to Unique
                locations[mark] = location # Record the location
            elif mark in unique:
                unique.remove(mark) # remove from Unique, Its been seen before
                banned.add(mark) # Ban this candidate its been seen more than once.
 
    for element in unique: # add all unique elements to done
        done += [(element,locations[element])]
    return done

"""
    Removes all pencil marks of all candidates within a given list of candidates
    From A Row.

    arguments:
        penMarks = penMarks dictionary
        board = SudokuBoard Object
        rowNum = row Number
        reduceArray = A list of candidates to be removed

    uses:
        bigMarks = a list of all pencilMark lists within the row
        marks = the pencil marks for a specific tile on the board
        rowIso = The isolated candidates within the row.
        bigMarks - a list of all pencilmark lists

    return:
        None
    
"""


def reduceRow(penMarks,board,rowNum,reduceArray,quadNo=None):
    bigMarks = []
    cols = [0,1,2,3,4,5,6,7,8]

    if quadNo != None:
        cols = []
        coords = board.getQuadCoords(quadNo)
        num = coords[1]#starting col Num Counts six spaces back to exclude the chosen quadrant
        while len(cols) != 6:
            if num-1 == -1:
                num = 9
            cols += [num - 1]
            num = num - 1
    for col in cols:
        #FUNCTION??
        
        marks = penMarks[rowNum,col]#get the Marks for these coordinates
        bigMarks += [marks]#Add to bigMarks
        if marks == None:# if there are no pencilmarks. meaning the space is already filled
            continue
        
        for reduce in reduceArray:
            reduceCoords(penMarks,rowNum,col,reduce) # remove this candidate from the pencil marks at
    if quadNo == None:                                      #These coordinates [rowNum,col]
        rowIso = reduceOccurences(bigMarks)
        for iso in rowIso:
            penMarks[(rowNum,iso[1])] = [iso[0]]

"""
    Removes all pencil marks of all candidates within a given list of candidates
    From A COlumn.

    arguments:
        penMarks = penMarks dictionary
        board = SudokuBoard Object
        colNum = row Number
        reduceArray = A list of candidates to be removed

    uses:
        bigMarks = a list of all pencilMark lists within the row
        marks = the pencil marks for a specific tile on the board
        colIso = The isolated candidates within the col.
        bigMarks - a list of all pencilmark lists

    return:
        None
    
"""

    
def reduceCol(penMarks,board,colNum,reduceArray,quadNo=None):
    bigMarks = []
    rows = [0,1,2,3,4,5,6,7,8]

    if quadNo != None:
        rows = []
        coords = board.getQuadCoords(quadNo)
        num = coords[0]#starting Row Num Counts six spaces back to exclude the chosen quadrant
        while len(rows) != 6:
            if num-1 == -1:
                num = 9
            rows += [num - 1]
            num = num - 1
    for row in rows:
        #FUNCTION??
        marks = penMarks[row,colNum]#get the pencilmarks for a specific Tile
        bigMarks += [marks]#Add to bigMarks
        if marks == None:# if there are no pencilmarks. meaning the space is already filled
            continue
        
        for reduce in reduceArray:
            reduceCoords(penMarks,row,colNum,reduce) # remove this candidate from the pencil marks at
                                                    #These coordinates [rowNum,col]
    if quadNo == None:
        colIso = reduceOccurences(bigMarks)
        for iso in colIso:
            penMarks[(iso[1],colNum)] = [iso[0]]



"""
Removes a specific candidate from a selected tiles pencilmarks
    arguments:
        penMarks - The dictionary of penmarks
        row - the row coordinate
        col - the col coordinate
        candidate - the candidate to be removed
    uses:
        marks - the selected tiles pencilMarks

"""
#Redundancy
#Marks can be passed in from the calling function
#Switch if this function does not change
def reduceCoords(penMarks,row,col,candidate):
    marks = penMarks[(row,col)]     # get the original marks
    if marks == None or candidate == 'X': 
        return
    if candidate in marks:
        marks.remove(candidate) #remove candidate from marks
    penMarks[(row,col)] = marks # set the new pencilmarks for the tile at (row,col)



#SEPARATE OBJECT
