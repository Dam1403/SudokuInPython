"""
"""



"""
This is the easiest technique to apply by eye – and the one that most people use first when completing paper Sudoku puzzles.

Choose a row, column or box, and then go through each of the numbers that hasn’t already been placed.
Because of other placements,the positions where you could place that number will be limited.
Often there will be two or three places that are valid, but if you’re lucky, there’ll only be one.
If you’ve narrowed it down to only one valid place where you can put the number… you can fill that number straight in, since it can’t go anywhere else!
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
    
#SEPARATE OBJECT
def reduceQuad(penMarks,board,quadNo,reduceArray):
    coords = board.getQuadCoords(quadNo)
    for row in range(0,3):
        adjRow = row + coords[0]
        
        for col in range(0,3):
            
            adjCol = col + coords[1]
            marks = penMarks[(adjRow,adjCol)]
            
            if marks == None:
                continue
            
            for reduce in reduceArray:
                reduceCoords(penMarks,adjRow,adjCol,reduce)
    
def reduceRow(penMarks,board,rowNum,reduceArray):
    for col in range(0,9):
        #FUNCTION??
        marks = penMarks[rowNum,col]
        if marks == None:
            continue
        for reduce in reduceArray:
            reduceCoords(penMarks,rowNum,col,reduce)
        #FUNCTION??
    
def reduceCol(penMarks,board,colNum,reduceArray):
    for row in range(0,9):
        #FUNCTION??
        marks = penMarks[row,colNum]
        if marks == None:
            continue
        for reduce in reduceArray:
            reduceCoords(penMarks,row,colNum,reduce)
        #FUNCTION??

#NUM MUST BE CHAR
def reduceCoords(penMarks,row,col,num):
    marks = penMarks[(row,col)]
    if marks == None or num == 'X':
        return
    if num in marks:
        marks.remove(num)
    penMarks[(row,col)] = marks



#SEPARATE OBJECT
