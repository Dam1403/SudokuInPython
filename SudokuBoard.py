class SudokuBoard:

    __board = dict()
    __colBoard = dict()
    __quadMap = dict()
    __Rinferences = dict()#(rowNum: [List of possible constraints])
    __Cinferences = dict()#(colNum: [List of possible constraints])

    #Deciding Quadrants, The quadrants that decide a specific quadrant
    __decQuad = dict()
    

    def __init__(self):
        
        self.__board = [["X" for column in range(0,9)] for row in range(0,9)]
        self.__colBoard = [["X" for row in range(0,9)] for column in range(0,9)]
        self.__quadMap.update({\
            0:(0,0),\
            1:(0,3),\
            2:(0,6),\
            3:(3,0),\
            4:(3,3),\
            5:(3,6),\
            6:(6,0),\
            7:(6,3),\
            8:(6,6)})
        #012
        #345
        #678
        self.__decQuad.update({\
            0:(1,2,3,6),\
            1:(0,2,4,7),\
            2:(0,1,5,8),\
            3:(0,6,4,5),\
            4:(1,5,7,3),\
            5:(2,3,4,8),\
            6:(0,3,7,8),\
            7:(1,4,6,8),\
            8:(2,5,6,7)})

        # Inference initialization 1-9
        for index in range(0,9):
            self.__Rinferences[index] = []
            self.__Cinferences[index] = []

        
    #MulTIPLE DIMENSION VIews  
    def __str__(self):
        strBoard = ""
        for row in range(0,9):
            b = self.__board[row]
            strBoard += b[0] + " " +  b[1] + " " +  b[2] + "  " + \
                  b[3] + " " +  b[4] + " " +  b[5] + "  " + \
                  b[6] + " " +  b[7] + " " +  b[8] + "  \n"
            if row == 2 or row == 5 or row == 8:
                strBoard += '\n'
        return strBoard

    def exportBoard(self):
        boardList = []
        for row in range(0,9):
            for col in range(0,9):
                boardList += [self.__board[row][col]]
        return boardList


          
    #Create Alter Board initializations
    #ARRAY OF ELEMENTS
    #TOP DOWN LEFT TO RIGHT
    # Large Array of size 81
    def setBoard(self, board1DimList):
        #Validate Board
        index = 0
        for row in range(0,9):
            for entry in range(0,9):
                self.__board[row][entry] = str(board1DimList[index])
                self.__colBoard[entry][row] = str(board1DimList[index])
                index += 1
        
                
    #check if value is string
    def setCoords(self,row,column,value):
        self.__board[row][column] = value
        self.__colBoard[column][row] = value     
        return 

    def writeQuad(self,quadArray,quadNo):
        quad = []
        b = self.__board
        c = self.__colBoard
        quadR,quadC = self.getQuadCoords(quadNo)
        index = 0
        for i in range(0,3):
            for j in range(0,3): 
                self.setCoords(quadR + i,quadC + j,quadArray[index])
                index += 1
        return
    
                
    def getCoords(self,row,column):
        return self.__board[row][column]
                
    def getColumn(self,colNum):
        return self.__colBoard[colNum]

    def getRow(self,rowNum):
        return self.__board[rowNum]

    #quadrants go 0 through 8 Left to right top to bottom
    def getQuadrant(self,quadNo):  
        quad = []
        quadR,quadC = self.getQuadCoords(quadNo)
        for i in range(0,3):
            for j in range(0,3): 
                quad += [self.getCoords(quadR + i,quadC + j)]
        return quad

    #Takes (self,quadNo) OR (self,row,column)
    #returns (quadR,quadC)
    def getQuadCoords(self,quadNo,column=None):
        if column != None:
            row = quadNo
            for i in [0,1]:# Possible Wasted Loop
                if row != 0 and row != 3 and row != 6:
                    row -= 1
                if column != 0 and column != 3 and column != 6:
                    column -= 1
            return (row,column)       
        return self.__quadMap[quadNo]

    def getDecQuads(self,quadNo):
        return self.__decQuad[quadNo]
    

    #Within Quad 
    def mkInf(self,possLocs,num):
        pLen = len(possLocs)
        if pLen == 2:
            loc1R = possLocs[0][1]
            loc1C = possLocs[0][2]
            loc2R = possLocs[1][1]
            loc2C = possLocs[1][2]

            if loc1R == loc2R:
                #print(loc1R,num,"INFERENCEROW")
                self.__Rinferences[loc1R] = num
            if loc1C == loc2C:
                #print(loc1R,num,"INFERENCECOL")
                self.__Cinferences[loc1C] = num
                
        if pLen == 3:
            loc1R = possLocs[0][1]
            loc1C = possLocs[0][2]
            loc2R = possLocs[1][1]
            loc2C = possLocs[1][2]
            loc3R = possLocs[2][1]
            loc3C = possLocs[2][2]

            if loc1R == loc2R == loc3R:
                #print(loc1R,num,"INFERENCEROW")
                self.__Rinferences[loc1R] = num
            if loc1C == loc2C == loc3C:
                #print(loc1R,num,"INFERENCECOL")
                self.__Cinferences[loc1C] = num
        
    # get Inferences
    #"rowcol index, \"ROW\" or \"COL\""
    def getInf(self,index,rowOrcol):
        if rowOrcol == "ROW":
            return self.__Rinferences[index]#ANYTHING ELSE?
        return self.__Cinferences[index]
    
    # set Inferences
    #"rowcol index, \"ROW\" or \"COL\""
    def setInf(self,index,num,rowOrcol):
        if rowOrcol == "ROW":
            self.__Rinferences[index] += [num]
        self.__Cinferences[index] += [num]
            
    def dumpInf(self):
        self.Rinferences = {\
            0: [],\
            1: [],\
            2: [],\
            3: [],\
            4: [],\
            5: [],\
            6: [],\
            7: [],\
            8: []}
        
        self.Cinferences = {\
            0: [],\
            1: [],\
            2: [],\
            3: [],\
            4: [],\
            5: [],\
            6: [],\
            7: [],\
            8: []}
