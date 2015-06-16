import SudokuBoard
import random
import cProfile

GLboard = None

def main():
   cProfile.run('createTen()')
   print(GLboard)
    
def createTen():
    boards = []
    for i in range(0,1):
       boards += [createBoard()]
    global GLboard
    GLboard = boards[0]

def createBoard():
    board = SudokuBoard.SudokuBoard()
    blankQuad = ["X","X","X","X","X","X","X","X","X"]
    index = 0

    progress = 0
    rlBack = 1
    while index != 9:
        
        if not popQuadrant(board,index):
            if rlBack >= index:
                rlBack = index
            for num in range(0,rlBack):
                board.writeQuad(blankQuad,index)
                index -= 1
            board.writeQuad(blankQuad,index)        
            rlBack = 1
        else:
            index += 1
            if index > progress:
                progress = index
                rlBack = 1
            else:
                rlBack += 1
            
        
    return board
    

def popQuadrant(board,quadNo):
    nums = ["1","2","3","4","5","6","7","8","9"]
    
    num = nums.pop(random.randint(0,8))
    movTrack = []
    quadCount = 0
    while True:
        if(quadCount == 18):
            return False
        placedNum = placeNum(board,num,quadNo)
        if placedNum == None:
            
            if len(movTrack) != 0:
                move = movTrack.pop(0)      
                oldNum = board.getCoords(move[0],move[1])
                board.setCoords(move[0],move[1],"X")   
                nums += [num,oldNum]
            else :
                nums +=[num]
        else:
            
            movTrack.append(placedNum)
        if len(nums) == 0:
            
            break

        if len(nums) == 1:
            num = nums[0]
            nums = []
        else:
            #You may Have just placed a number on the end of the list
            num = nums.pop(random.randint(0,len(nums) - 2))
        quadCount += 1
    return True
        
                                     
                       
def placeNum(board,num,quadNo):
        #Swap Dict in this function
    quadCount = 0
    
    while True:
        if(quadCount == 18):
            return None
        offsets = board.getQuadCoords(quadNo)
        for rowNum in [0,1,2]:
            for colNum in [0,1,2]:
                
                
                adjRow = offsets[0] + rowNum
                adjCol = offsets[1] + colNum
                #is Valid Position
                
                if isValidPos(board,adjRow,adjCol,num,True):
                    
                    board.setCoords(adjRow,adjCol,num)
                    return (adjRow,adjCol)
        if swapNumQuads(board,num,quadNo) == False:
            return None
        quadCount += 1
        


def swapNumQuads(board,numToSwap,quadNo):
    quadNos = board.getDecQuads(quadNo)
    potPos = []
    #531
    #246
    #789
    for decQuad in quadNos:
        potPos = []
        numPos = None
        for rowNum in [0,1,2]:
            for colNum in [0,1,2]:
                if isValidPos(board,rowNum,colNum,numToSwap):
                   potPos +=[(rowNum,colNum)]
            
        offsets = board.getQuadCoords(decQuad)
        for coordTup in potPos:
            adjRow = offsets[0] + coordTup[0]
            adjCol = offsets[1] + coordTup[1]
            
            currNum = board.getCoords(adjRow,adjCol)
            if currNum == numToSwap:
                numPos = (adjRow,adjCol)

        
        if numPos == None: # Bad Fix
            continue
        
        for coordTup in potPos:
            numTup = potPos[random.randint(0,len(potPos) - 1)]
            if numPos == coordTup:
                continue
            
            currNum = board.getCoords(coordTup[0],coordTup[1])
            valid = isValidPos(board,adjRow,adjCol,currNum)
            if valid:
                board.setCoords(numPos[0],numPos[1],currNum)
                board.setCoords(coordTup[0],coordTup[1],numToSwap)        
                return True
        potPos = []
    return False
            

#Validate including quadrant Set None 
def isValidPos(board,rowNum,colNum,num,checkQuad=False):
    if checkQuad != False:
        if board.getCoords(rowNum,colNum) != "X":
            return False
    row = board.getRow(rowNum)
    col = board.getColumn(colNum)

    #OPTOMIZE
    
    #Switched a row is an array of columns
    # a column is an array of rows
    #quadCol,quadRow = ((rowNum//3)*3,(colNum//3)*3)
    quadCol,quadRow = board.getQuadCoords(rowNum,colNum)

    for index in [0,1,2,3,4,5,6,7,8]:
        if not (quadRow <= index < quadRow + 3):
            #print("CHECK Row",num,row,quadRow,index)
            if num == row[index]:        
                return False
        if not (quadCol <= index < quadCol + 3):
            #print("CHECK Col",num,col,quadCol,index)
            if num == col[index]:
                return False
        
    return True

    

main()
