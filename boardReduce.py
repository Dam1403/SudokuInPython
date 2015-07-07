"""
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

"""

def candidateLine(board,penMarks):
    for num in ['1','2','3','4','5','6','7','8','9']:
        for quadNo in range(0,9):
            coords = board.getQuadCoords(quadNo)
            possLocs = []
            for row in range(0,3):
                adjRow = row + coords[0]
                for col in range(0,3):
                    adjCol = col + coords[1]
                    #print("Thorough?",adjRow,adjCol)
                    marks = penMarks[(adjRow,adjCol)]
                    if marks == None:
                        continue
                    if  num in marks:
                        possLocs = possLocs + [(num,adjRow,adjCol)]
            #print("DONE")
            pLen = len(possLocs)
            if pLen == 2:
                loc1R = possLocs[0][1]
                loc1C = possLocs[0][2]
                loc2R = possLocs[1][1]
                loc2C = possLocs[1][2]

                if loc1R == loc2R:
                    #print(loc1R,"Num->",num,"INFERENCEROW")
                    reduceRowEx(penMarks,board,loc1R,quadNo,[num])
                if loc1C == loc2C:
                    #print(loc1C,num,"INFERENCECOL")
                    reduceColEx(penMarks,board,loc1C,quadNo,[num])
                    
            if pLen == 3:
                loc1R = possLocs[0][1]
                loc1C = possLocs[0][2]
                loc2R = possLocs[1][1]
                loc2C = possLocs[1][2]
                loc3R = possLocs[2][1]
                loc3C = possLocs[2][2]

                if loc1R == loc2R == loc3R:
                    #print(loc1R,num,"INFERENCEROW")
                    reduceRowEx(penMarks,board,loc1R,quadNo,[str(num)])
                if loc1C == loc2C == loc3C:
                    #print(loc1C,num,"INFERENCECOL")
                    reduceColEx(penMarks,board,loc1C,quadNo,[str(num)])
                            



#SEPARATE OBJECT
# REMOVE MAGIC NUMBERS FOR MORE READABILITY
def reduceQuad(penMarks,board,quadNo,reduceArray):
    coords = board.getQuadCoords(quadNo)
    bigMarks = []
    
    for row in range(0,3):
        adjRow = row + coords[0]
        for col in range(0,3):
            adjCol = col + coords[1]
            marks = penMarks[(adjRow,adjCol)]

            bigMarks += [marks]
            if marks == None:
                continue       
            
            for reduce in reduceArray:
                reduceCoords(penMarks,adjRow,adjCol,reduce)
    quadIso = reduceOccurences(bigMarks)
    for iso in quadIso:
        isoCrd = numToQuadCoords(iso[1])
        penMarks[(isoCrd[0]+coords[0],isoCrd[1]+coords[1])] = [iso[0]]

#returns the positions of the unique elements
#(element,position)
def numToQuadCoords(num):
    #print(type(num),"NUM")
    coords = [0,0]
    while num != 0:
        coords[1] = coords[1] + 1
        if coords[1] == 3:
            coords[0] = coords[0] + 1
            coords[1] = 0
        num -= 1
    return (coords[0],coords[1])


# MIGHT HAVE TO BE USED FOR ALL REDUCTIONS
def reduceOccurences(allMarks):
    #print(allMarks,"MARKSSS")
    banned = set()
    locations = dict()
    unique = []
    done = []
    for i in range(0,9):
        marks = allMarks[i]
        if marks == None:
            continue
        for mark in marks:
            if mark not in unique and mark not in banned:
     #           print(marks,"UNIQUE!!!")
                unique += [mark]
                locations[mark] = i
            elif mark in unique:
                unique.remove(mark)
                banned.add(mark)
    #print("END QUAD!!!")
        
    for element in unique:
        done += [(element,locations[element])]
    return done
        
    
#Excludes the current quadrant
def reduceRowEx(penMarks,board,rowNum,quadNo,reduceArray):
    coords = board.getQuadCoords(quadNo)
    
    cols = []
    num = coords[1]#starting col Num Counts six spaces back to exclude the chosen quadrant
    
    while len(cols) != 6:
        if num-1 == -1:
            num = 9
        cols += [num - 1]
        num = num - 1
    #print(coords,cols)  
    for col in cols:
        #FUNCTION??
        marks = penMarks[rowNum,col]
        if marks == None:
            continue
        for reduce in reduceArray:
            reduceCoords(penMarks,rowNum,col,reduce)
        #FUNCTION??
            
        
    
def reduceColEx(penMarks,board,colNum,quadNo,reduceArray):
    coords = board.getQuadCoords(quadNo)
    
    rows = []
    num = coords[0]#starting Row Num Counts six spaces back to exclude the chosen quadrant
    while len(rows) != 6:
        if num-1 == -1:
            num = 9
        rows += [num - 1]
        num = num - 1
    for row in rows:
        #FUNCTION??
        marks = penMarks[row,colNum]
        if marks == None:
            continue
        for reduce in reduceArray:
            reduceCoords(penMarks,row,colNum,reduce)
        #FUNCTION??
    



def reduceRow(penMarks,board,rowNum,reduceArray):
    bigMarks = []
    for col in range(0,9):
        #FUNCTION??
        
        marks = penMarks[rowNum,col]
        bigMarks += [marks]
        if marks == None:
            continue
        
        for reduce in reduceArray:
            reduceCoords(penMarks,rowNum,col,reduce)
        #FUNCTION??
    quadIso = reduceOccurences(bigMarks)
    for iso in quadIso:
        penMarks[(rowNum,iso[1])] = [iso[0]]

    
def reduceCol(penMarks,board,colNum,reduceArray):
    bigMarks = []
    for row in range(0,9):
        #FUNCTION??
        marks = penMarks[row,colNum]
        bigMarks += [marks]
        if marks == None:
            continue
        for reduce in reduceArray:
            reduceCoords(penMarks,row,colNum,reduce)
        #FUNCTION??
    quadIso = reduceOccurences(bigMarks)
    for iso in quadIso:
        penMarks[(iso[1],colNum)] = [iso[0]]

#NUM MUST BE CHAR
def reduceCoords(penMarks,row,col,num):
    marks = penMarks[(row,col)]
    #if row == 6 and col == 1:
        #print(marks,row,col,num)
        
    if marks == None or num == 'X':
        return
    if num in marks:
        marks.remove(num)
    penMarks[(row,col)] = marks



#SEPARATE OBJECT
