import sys
from assemblerFunctions import *

if __name__ == "__main__":
    if len(sys.argv) > 1:
        offset = 0
        if len(sys.argv) > 2:
            if sys.argv[2].isnumeric():
                offset = int(sys.argv[2])

        assemblyFile = open(sys.argv[1], "r")
        assembledFile = open(sys.argv[1].replace('.src', '.obj'), "w")
        lines = assemblyFile.readlines()#read all lines
        lines = fullProcedure(lines, offset)
        lines = [i+'\n' for i in lines]
        assembledFile.writelines(lines)
        print("Assembled successfully, written to " + sys.argv[1].replace('.src', '.obj'))
    else:
        while(True):
            line = input(">>> ")
            assembled = fullProcedure([line], 0)
            print(assembled)
