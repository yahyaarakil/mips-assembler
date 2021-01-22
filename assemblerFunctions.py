import mipsDictionaries

#function that takes a list of instructions
#and returns a list of dictionaries each dictionary representing an instruction
#this streamlines the assembling process by removing importance of order of tokens
def parseInstructions(lines):
    #inner function that converts a single string (instruction) into a list of tokens
    #it uses a specific order
    #0: label, 1: instruction, 2: arg1, 3: arg2, 4: arg3, 5: line number of the instruction
    def differentiateLine(line, lineNumber):
        #removes comments
        line = line.split('#')[0]
        #removes the whitespace and splits into tokens
        tokens = (line.replace(',', ' ').replace('\n', '').replace(':', ' ').replace('(', ' ').replace(')', ' ')).split()
        #if line has no label it adds an empty token
        if tokens[0] in mipsDictionaries.instructions:
            tokens = [''] + tokens
        #if it has less than 3 arguments, fills the other slots with empty
        tokens += [''] * (5-len(tokens)) #fills the other 5 slots with ''
        #adds the line number of the line to the set of tokens, used for error reporting
        tokens += [lineNumber]
        #returns the line (instruction) as a list of tokens
        return tokens

    #takes an instruction as a list and if it was a pseudo instruction
    #resolves it into it's constituent instructions (as lists) based on the blueprint
    #provided in the mipsDictionaries
    def resolvePseudoInstructions(line):
        #if instruction was not recognized, stop execution and report error
        if mipsDictionaries.instructions.get(line[1], -1) == -1: #is NOT recognized
            raise Exception("instruction at line " + str(line[5]) +" is not recognized ")
        #if instruction given was not pseudo, return it as it is
        elif mipsDictionaries.instructions.get(line[1], 0) != 3: #is NOT pseudo
            return [line]
        #initialize new instructions
        instructionList = []
        #foreach new instruction
        for instruction in mipsDictionaries.pseudoRes(line[1], line[2], line[3], line[4]):
            #add the differentiated (tokenized) list of the instruction to the list of
            #resulting instructions
            instructionList.append(differentiateLine(instruction, "Pseudo"))
        instructionList[0][0] = line[0]#not working?
        #return list of new instructions
        return instructionList

    #takes an instruction (as a list) and resolves it into a dictionary
    def convertToBP(instruction):
        #create a dictionary
        instructionDic = {}
        #retreive the blueprint from the mipsDictionary
        bp = mipsDictionaries.instructions[instruction[1]]

        #filling the blueprint
        instructionDic["label"] = instruction[0]
        instructionDic["instruction"] = instruction[1]
        count = 2
        for reg in bp[2].split():
            instructionDic[reg] = instruction[count]
            count+=1
        instructionDic["line_number"] = instruction[5]
        #return instruction as dictionary, instead of list
        #helps streamline the process
        return instructionDic

    #begin instruction parsing using helper functions above
    #starting line
    lineNumber = 1
    newLines = []
    #foreach line
    for line in lines:
        #skip empty lines or comment lines
        if line != "":
            if  line[0]!='\n' and line[0] != '#' and line[0] != '\t' and not line.isspace():
                newLines.append(differentiateLine(line, lineNumber))
        lineNumber += 1
    #filtered lines
    lines = newLines
    pseudoResolvedLines = []
    #resolve pseudo instructions
    #then convert all the instructions into their respective blueprints
    for line in lines:
        for instruction in resolvePseudoInstructions(line):
            pseudoResolvedLines.append(convertToBP(instruction))
    #returns the parsed list of dictionaries of instructions
    return pseudoResolvedLines

#verify the size of the immediates, only for error checking
def verifyImmediates(lines):
    for instruction in lines:
        if "immediate" in instruction:
            if int(instruction["immediate"]) > (2**16):
                raise Exception("immediate is too large at line " + str(instruction["line_number"]))
        if "sa" in instruction:
            if int(instruction["sa"]) > 2**5:
                raise Exception("shift amount is too large at line " + str(instruction["line_number"]))

    return lines

#function that calculates the address of the labels so they can be 
#used in jumps and branches
def calculateLabelAddresses(lines, offset):
    #current address starts from the offset
    cursor = offset
    #dictionary of labels
    labels = {}
    #foreach instruction
    for instruction in lines:
        #if it has a label
        if instruction["label"] != "":
            #if the label was already defined
            if(instruction["label"] in labels):
                #break execution and report error
                raise Exception("Label occurs multiple times, must be unique!")
            #if not, add the label with its corresponding address value
            labels[instruction["label"]] = cursor
        #increment the current instruciton address
        cursor+=4
    #return a dictionary of labels
    return labels

#uses the blueprint do resolve the labels and registers
#from decimal to 2's complement into their respective slots
def resolveLabelsAndRegisters(lines, labels, pc):
    newLines = []
    #creates copy of the old list, so it won't be destructive conversion
    for instruction in lines:
        newLines.append(dict(instruction))
    #foreach line (instruction dictionary)
    for newLine in newLines:
        #increment the current address
        pc+=4
        try:
            if "rs" in newLine:
                newLine["rs"] = mipsDictionaries.registers[newLine["rs"]]
            if "rt" in newLine:
                newLine["rt"] = mipsDictionaries.registers[newLine["rt"]]
            if "rd" in newLine:
                newLine["rd"] = mipsDictionaries.registers[newLine["rd"]]
        except Exception:
            #reports error
            raise Exception("Invalid register at line "+str(newLine["line_number"]))
        #if a label is specified in a branch but does not resolve to an address
        if  "offset" in newLine:
            if not newLine["offset"] in labels:
                raise Exception("Label "+ newLine["offset"] + " not found at line " + str(newLine["line_number"]))
            newLine["offset"] = str((int(labels[newLine["offset"]])-pc)//4)
        #if a label is specified in a jump but does not resolve to an address
        if "dest" in newLine:
            if not newLine["dest"] in labels:
                raise Exception("Label "+ newLine["dest"] + " not found at line " + str(newLine["line_number"]))
            newLine["dest"] = str(((int(labels[newLine["dest"]]))//4))
    return newLines

#assembles the instructions from their blueprint form
#to the corresponding binary representation
#purely mechanically
def assemble(lines):
    #inner function that converts a decimal to 2's complement
    def toBinary(numberString, length):
        def flip(c): 
            return '1' if (c == '0') else '0'
        if int (numberString) < 0:
            bin = ('{0:b}'.format(int(numberString)).zfill(length)).replace('-', '')
            n = len(bin)  
            ones = "" 
            twos = "" 
            for i in range(n): 
                ones += flip(bin[i])
            ones = list(ones.strip("")) 
            twos = list(ones) 
            for i in range(n - 1, -1, -1): 
            
                if (ones[i] == '1'): 
                    twos[i] = '0'
                else:          
                    twos[i] = '1'
                    break
        
            i -= 1 
            if (i == -1): 
                twos.insert(0, '1')
            return "1"*(length-len(twos))+"".join(twos)
        return '{0:b}'.format(int(numberString)).zfill(length)

    #list of instructions, copied to not be destructive
    binaryInstructions = []

    #foreach instruction
    for instruction in lines:
        #start converting into binary
        #retreive the assembly blueprint
        instructionBP = mipsDictionaries.instructions[instruction["instruction"]]
        #start editing the blueprint
        assembled = str(instructionBP[0])
        #retreive the correct opcode
        assembled = assembled.replace("opcode ", instructionBP[1])

        #replace each register and shift amount with it's binary representation
        assembled = assembled.replace("rs ", toBinary(instruction.get("rs", '0'), 5))
        assembled = assembled.replace("rt ", toBinary(instruction.get("rt", '0'), 5))
        assembled = assembled.replace("rd ", toBinary(instruction.get("rd", '0'), 5))
        assembled = assembled.replace("sa ", toBinary(instruction.get("sa", '0'), 5))

        #if it has a function slot
        if "function" in assembled:
            assembled = assembled.replace("function", instructionBP[3])

        #if it has an immediate slot
        if "immediate" in instruction:
            assembled = assembled.replace("immediate", toBinary(instruction["immediate"], 16))
        #or if it has an offset slot, branches
        elif "offset" in instruction:
            assembled = assembled.replace("immediate", toBinary(instruction["offset"], 16))
        #or if it has a dest slot, jumps
        elif "dest" in instruction:
            assembled = assembled.replace("target", toBinary(instruction["dest"], 26))

        #adds the new representation to the new list
        binaryInstructions.append(assembled)
    #return the binary representation
    return binaryInstructions

#converts each binary instruction into it's hexadecimal form
def toHexInstructions(lines):
    return ["0x"+("{}".format(hex(int(instruction, 2))).replace('0x', '').zfill(8)) for instruction in lines]

#the full procedure calls all of the functions above in the correct order
#takes the list of strings (instructions)
#returns a list of strings (hex instructions)
#if verbose is set to true, it will also print each step
def fullProcedure(lines, offset, verbose):
    lines = parseInstructions(lines)
    if verbose:
        for line in lines:
            print(str(line))
    lines = verifyImmediates(lines)
    labels = calculateLabelAddresses(lines, offset)
    if verbose:
        for line in labels:
            print(str(line)+": "+str(labels[line]))
    lines = resolveLabelsAndRegisters(lines, labels, offset)
    if verbose:
        for line in lines:
            print(str(line))
    lines = assemble(lines)
    if verbose:
        for line in lines:
            print(str(line))
    lines = toHexInstructions(lines)
    if verbose:
        for line in lines:
            print(str(line))
    return lines