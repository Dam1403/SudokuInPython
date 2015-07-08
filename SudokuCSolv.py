#https://www.sudokuoftheday.com/techniques/

"""
Douglas May

"""
import SudokuBoard
import boardReduce

def main():
    board = SudokuBoard.SudokuBoard()
    printBanner()                                                                                 
    print("Version 0.35 \nCreated By Douglas May\n\n")
    inType = input("User input or File input?(USER/FILE): ")
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
    else:
        print("Invalid Answer")
        return
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




def solve(board):
    penMarks = createPenMarks(board)
    for i in range(0,81):
        boardReduce.singlePosition(board,penMarks)
        boardReduce.candidateLine(board,penMarks)
        resolveBoard(board,penMarks)
    #displayPenMarks(penMarks)

    
  
#User Board editing subShell!!!

def createPenMarks(board=None):
    penMarks = dict()# FEED INTO VISIONS
    if board == None:
        #None Case Here
        pass
    for i in range(0,9):
        for j in range(0,9):
            if board.getCoords(i,j) == 'X':
                penMarks[(i,j)] = ['1','2','3','4','5','6','7','8','9']
            else:
                penMarks[(i,j)] = None
    return penMarks
            #EMPTY TILES?
            
def displayPenMarks(penMarks):
    for i in range(0,9):
        print("Row",i,end=":")
        for j in range(0,9):
            print(penMarks[(i,j)],end="")
        print("")
"""
Single Candidate:
https://www.sudokuoftheday.com/techniques/single-candidate/

This technique is very easy –
especially if you’re using pencilmarks to store what candidates
are still possible within each cell.

If you’ve managed to rule out all other possibilities for a particular cell
(by examining the surrounding column, row and box),
so there’s only one number left that could possibly fit there –
you can fill in that number.



"""
def resolveBoard(board,penMarks):
    Done = False
    #while not Done:
    #   Done = True
    #OPTOMIZATION
    #This function cannot see if it generates resolvable positions
    #Call Basic penReduce Functions Here
    for i in range(0,9):
        for j in range(0,9):
            marks = penMarks[(i,j)]
            if marks == None:
                continue
            if len(marks) == 1:
                board.setCoords(i,j,penMarks[(i,j)][0])
                penMarks[(i,j)] = None
                #Done = False
            
                
def printBanner():
    print("                                                                      ,-.----.            \n"\
    "  .--.--.                                        ,-.                  \    /  \           \n"\
    " /  /    '.                   ,---,          ,--/ /|                  |   :    \          \n"\
    "|  :  /`. /         ,--,    ,---.'|  ,---. ,--. :/ |         ,--,     |   |  .\ :         \n"\
    ";  |  |--`        ,'_ /|    |   | : '   ,'\:  : ' /        ,'_ /|     .   :  |: |         \n"\
    "|  :  ;_     .--. |  | :    |   | |/   /   |  '  /    .--. |  | :     |   |   \ :   .--,  \n"\
    " \  \    `.,'_ /| :  . |  ,--.__| .   ; ,. '  |  :  ,'_ /| :  . |     |   : .   / /_ ./|  \n"\
    "  `----.   |  ' | |  . . /   ,'   '   | |: |  |   \ |  ' | |  . .     ;   | |`-, ' , ' :  \n"\
    "  __ \  \  |  | ' |  | |.   '  /  '   | .; '  : |. \|  | ' |  | |     |   | ; /___/ \: |  \n"\
    " /  /`--'  :  | : ;  ; |'   ; |:  |   :    |  | ' \ :  | : ;  ; |     :   ' |  .  \  ' |  \n"\
    "'--'.     /'  :  `--'   |   | '/  '\   \  /'  : |--''  :  `--'   \___ :   : :   \  ;   :  \n"\
    "  `--'---' :  ,      .-.|   :    :| `----' ;  |,'   :  ,      .-./  .\|   | :    \  \  ;  \n"\
    "            `--`----'    \   \  /          '--'      `--`----'   \  ; `---'.|     :  \  \ \n"\
    "                          `----'                                  `--\"  `---`      \  ' ; \n"\
    "                                                                                    `--`  \n"\
    )

    
        
main()    
