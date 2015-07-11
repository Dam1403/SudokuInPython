import urllib.request
import Sudoku

from bs4 import BeautifulSoup



def pData(data):
        strBoard = ""
        for i in range(0,81):
            print(data[i],end=" ")
            if i//9 == 0:
                print("\n")
        return strBoard

r = urllib.request.urlopen("http://view.websudoku.com/?level=1")
soup = BeautifulSoup(str(r.read()), 'html.parser')

bData = []
for inp in soup.find_all('input'):
    
    sinp = str(inp)
    if 'id=\"f' in sinp:
        if 'readonly' in sinp:
            bData += [str(inp['value'])]
        else:
            bData += ['X']

print(pData(Sudoku.board_Src_External(bData)))


    
