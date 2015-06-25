"""





"""
import SudokuBoard


def main():
    board = SudokuBoard.SudokuBoard()
    inType = input("User input of File input?(USER/FILE): ")
    if inType == "USER":
        userBoard = board_Src_UInput()
        if not userBoard:
            return 
        board.setBoard(userBoard)
        print(userBoard)
    elif inType == "FILE":
        userBoard = board_Src_FileInput()
        if not userBoard:
            return 
        board.setBoard(userBoard)
    print("Initial Board:")
    print(board)
    print("======================================")
    solve(board)
    print("solved :) \n")
    print(board)

    



def board_Src_UInput():
    boardArray = []
    valid = [0,1,2,3,4,5,6,7,8]

    numsRead = 0
    print("Input 9x9 grid of numbers (1-9) or X(For Empty Squares)")
    print("From left to Right and From top to Bottom")
    print("\nExample: \n123456789[enter]")

    print("234567891[enter]")
    print("345678912[enter]")
    print("456789123[enter]")
    print("567891234[enter]")
    print("678912345[enter]")
    print("789123456[enter]")
    print("891234567[enter]")
    print("912345678[enter]")
    print("\ninput Numbers:")
    for i in range(0,9):
        line = input("")
        if not validateInLine(line):
            return False
        boardArray += list(line)
    return boardArray
        

def board_Src_FileInput():
    boardArray = []
    valid = [0,1,2,3,4,5,6,7,8]

    numsRead = 0
    print("File must contain a 9x9 grid of numbers (1-9) or X(For Empty Squares)")
    print("From left to Right and From top to Bottom")
    print("\nExample: \n123456789\\n")

    print("234567891\\n")
    print("345678912\\n")
    print("456789123\\n")
    print("567891234\\n")
    print("678912345\\n")
    print("789123456\\n")
    print("891234567\\n")
    print("912345678\\n")
    filename = input("\ninput Filename: ")
    f = open(filename)
    count = 1
    for line in f:
        line = line.strip()
        if not validateInLine(line):
            return False
        if count > 9:
            return invalid_Input("Too Many Lines")
        boardArray += list(line)
    return boardArray

#Takes a String of length 81  NO NEWLINE
def board_Src_External(data):
    offset = 0
    for i in range(0,9):
        line = validline[0+offset:9+offset]
        if not validateInLine(line):
            return False
    #CALL SOLVE METHOD
    board = SudokuBoard.SudokuBoard()
    board.setBoard(userBoard)
    #http://view.websudoku.com/?level=4 PARSE THIS For Board
    return solve(board).exportBoard()
    
    

def invalid_Input(message):
    print("Invalid input:",message)
    return False
    
def validateInLine(line):
    if len(line) != 9:
            return invalid_Input("Too (many/few) characters in " + str(line))
    for c in line:
        if c == "X":
            continue
        if c != "0" and c.isdigit():
            continue
        return invalid_Input(c + " Found In " + str(line))

    return True

def initPossDict(board):
    possDict = {}
    for quadNo in range(0,9):
        quadVals = getQuadrant(quadNo)
        for locValue in quadVals:
            if locValue != "X":
                continue
                #If You want to suggest a corrected user board use this     


def solve(board):
    quadsFull = 0
    loopCount = 0
    smart = False
    while True:
        if loopCount == 18:
            smart = True
            #print("NeedSmarts!!")
        if loopCount == 256:
            print("Too Hard :(")
            print(board)
            input("It's Ctrl-C Time :(")
        for quadNo in range(0,9):
            
            quadDict = {}#Global Dict?
            quadReqs = getQuadReqs(board,quadNo)#quadNeeds
            
            if quadReqs == []:# quadFull
                quadsFull += 1
                continue
            

            index = 0
            while index < len(quadReqs):
                quadReq = quadReqs[index]
                quadDict = isValidQuad(board,quadNo,quadReq,smart)
                
                locations = quadDict[quadReq]
                
                if len(locations) == 1:
                    board.setCoords(locations[0][1],locations[0][2],locations[0][0])
                    #print(board)
                    #print("==============================")
                    quadReqs.remove(quadReq)
                    index = 0
                    loopCount = 0
                    if smart:
                        board.dumpInf()
                        smart = False
                else:
                    index += 1
        if quadsFull == 9:
            break
        quadsFull = 0
        loopCount += 1
        compRow(board)
        compCol(board)
        #https://www.sudokuoftheday.com/techniques/naked-pairs-triples/
    return board  
        

def getQuadReqs(board,quadNo):
    standard = list("123456789")
    quad = board.getQuadrant(quadNo)
    for entry in quad:
        if entry in standard:
            standard.remove(entry)
    return standard
            
            
#REDUNDANCY?
#Validate return dict with proper positions
#rename!!!!
def isValidQuad(board,quadNo,num,smart=False):
    rows = []
    cols = []
    #OPTOMIZE
    #Switched a row is an array of columns
    # a column is an array of rows
    
    quadRow,quadCol = board.getQuadCoords(quadNo)
    
    quadDict = dict()
    quadDict[num] = []    

    for row in range(0,3):
        adjRow = quadRow + row
        rows.append(list(board.getRow(adjRow)))
        if smart:
            rows[-1] += board.getInf(adjRow,"ROW")
        if num in rows[row]:
            continue
        for col in range(0,3):
            adjCol = quadCol + col
            cols.append(list(board.getColumn(adjCol)))
            if smart:
                cols[-1] += board.getInf(adjCol,"COL")
            if num in cols[col] or board.getCoords(adjRow,adjCol) != "X":
                continue
            
            quadDict[num] = quadDict[num] + [(num,adjRow,adjCol)]
    #print(num,quadDict)
    board.mkInf(quadDict[num],num)
    return quadDict #Array instead?

"""
def isValidPos(board,rowNum,colNum,num):
    row = board.getRow(rowNum)
    col = board.getColumn(colNum)

    quadCol,quadRow = board.getQuadCoords(rowNum,colNum)

    for index in [0,1,2,3,4,5,6,7,8]:
        if not (quadRow <= index < quadRow + 3):
            if num == row[index]:        
                return False
        if not (quadCol <= index < quadCol + 3):
            if num == col[index]:
                return False
    return True
"""

#complete Row Col
#OPTOMIZE row and col could be done at the same time
def compRow(board):
    rowreqs = ['1','2','3','4','5','6','7','8','9']
    RxLocs = []
    rowNum = 0
    wasSet = False
    while rowNum < 9:
        row = board.getRow(rowNum)
        for i in range(0,len(row)):
            Rval = row[i]
            if Rval != "X":
                rowreqs.remove(Rval)
            else:
                RxLocs += [i]
        possLoc = [] 
        for RxLoc in RxLocs:
            column = board.getColumn(RxLoc)
            reqs = list(rowreqs)
            index = 0
            while index < len(reqs):
                req = reqs[index]
                if req in column:
                    reqs.remove(req)
                if len(reqs) == 1:
                    #print("SET ROW",reqs)
                    board.setCoords(rowNum,RxLoc,reqs[0])
                    #print(board)
                    rowreqs.remove(reqs[0])
                    wasSet = True
                    break
                index += 1
        if not wasSet:
            rowNum += 1
        wasSet = False
        RxLocs = []
        rowreqs = ['1','2','3','4','5','6','7','8','9']

def compCol(board):
    colreqs = ['1','2','3','4','5','6','7','8','9']
    CxLocs = []
    colNum = 0
    wasSet = False
    while colNum < 9:
        #print("Loop",colNum)
        col = board.getColumn(colNum)
        for i in range(0,len(col)):
            Cval = col[i]
            if Cval != "X":
                #print(col,i,"COLREQS")
                colreqs.remove(Cval)
            else:
                CxLocs += [i]
        possLoc = []
        for CxLoc in CxLocs:
            row = board.getRow(CxLoc)
            reqs = list(colreqs)
            index = 0
            while index < len(reqs):
                req = reqs[index]
                if req in row:
                    reqs.remove(req)
                if len(reqs) == 1:
                    #print("SET COL",reqs)
                    board.setCoords(CxLoc,colNum,reqs[0])
                    #print(board)
                    colreqs.remove(reqs[0])
                    wasSet = True
                    break
                index += 1
        #print(wasSet)
        if not wasSet:
            colNum += 1
        wasSet = False
        CxLocs = []
        colreqs = ['1','2','3','4','5','6','7','8','9']    
                    
        

main()

