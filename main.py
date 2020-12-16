import sys
from assemblerFunctions import *

def setVerbose(i):
    if sys.argv[i].lower() == "true":
        return True
    elif sys.argv[i].lower() == "false":
        verbose = False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        offset = 0
        verbose = False
        if len(sys.argv) > 2:
            if sys.argv[2].isnumeric():
                offset = int(sys.argv[2])
            else: verbose = setVerbose(2)
            if len(sys.argv) > 3:
                verbose = setVerbose(3)

        assemblyFile = open(sys.argv[1], "r")
        lines = assemblyFile.readlines()#read all lines
        assembledFile = open(sys.argv[1].replace('.src', '.obj'), "w")
        try:
            lines = [i+'\n' for i in fullProcedure(lines, offset, True)]
        except Exception as e:
            print(e)
            exit(1)
        assembledFile.writelines(lines)
        print("Assembled successfully, written to " + sys.argv[1].replace('.src', '.obj'))
    else:
        while(True):
            print(fullProcedure([input(">>> ")], 0))