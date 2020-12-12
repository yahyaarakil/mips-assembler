import sys
from assemblerFunctions import *

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'VERIFY':
            print(verifyDictionaries())
            exit(0)

        offset = 0
        if len(sys.argv) > 2:
            if sys.argv[2].isnumeric():
                offset = int(sys.argv[2])

        assemblyFile = open(sys.argv[1], "r")
        lines = assemblyFile.readlines()#read all lines
        lines = [i+'\n' for i in fullProcedure(lines, offset)]
        assembledFile = open(sys.argv[1].replace('.src', '.obj'), "w")
        assembledFile.writelines(lines)
        print("Assembled successfully, written to " + sys.argv[1].replace('.src', '.obj'))
    else:
        while(True):
            print(fullProcedure([input(">>> ")], 0))
