import sys
from assemblerFunctions import *

def setVerbose(i):
    if sys.argv[i].lower() == "true":
        return True
    elif sys.argv[i].lower() == "false":
        return False

if __name__ == "__main__":
    #parse arguments
    #if a file was passed in
    if len(sys.argv) > 1:
        offset = 4194304 #offset in decimal
        verbose = True
        if len(sys.argv) > 2:
            if sys.argv[2].isnumeric():
                offset = int(sys.argv[2])
            else: verbose = setVerbose(2)
            if len(sys.argv) > 3:
                verbose = setVerbose(3)
        #open the source file
        assemblyFile = open(sys.argv[1], "r")
        #read all lines
        lines = assemblyFile.readlines()
        #if it has the correct extension name
        if ".src" in sys.argv[1]:
            assembledFile = open(sys.argv[1].replace('.src', '.obj'), "w")
        else:
            assembledFile = open(sys.argv[1]+".obj", "w")
        #start the main procedure
        # try:
        lines = [i+'\n' for i in fullProcedure(lines, offset, verbose)]
        # #print errors
        # except Exception as e:
        #     print(e)
        #     exit(1)#exit
        #write the output object file
        assembledFile.writelines(lines)
        print("Assembled successfully, written to " + sys.argv[1].replace('.src', '.obj'))
    #if no file was passed in, it will start in interactive mode
    else:
        #it keeps track of all the lines entered so you can utilize labels
        lines = []
        print("Type EXIT to exit")
        try:
            answer = input(">>> ")
            #while you're not trying to exit
            while answer != "EXIT":
                try:
                    #append the input to the list of inputs
                    lines.append(answer)
                    #assemble the list of inputs
                    assembled = [i+'\n' for i in fullProcedure(lines, 0, False)]
                    #prints the last assembled instruction 
                    print(assembled[len(assembled) - 1])
                    #takes a new input
                    answer = input(">>> ")
                #if an error occurs
                except Exception as e:
                    #prints the error
                    print(e)
                    #removes the bad line from the list of inputs
                    lines.remove(lines[len(lines) - 1])
                    #reads a new input
                    answer = input(">>> ")
        except KeyboardInterrupt:
            print("Exiting!")