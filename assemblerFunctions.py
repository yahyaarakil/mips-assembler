import mipsDictionaries

#label, instruction, register or label, register or immediate, register or continue immediate

def parseInstructions(lines):
    def differentiateLine(line, lineNumber):
        tokens = (line.replace(',', ' ').replace('\n', '').replace(':', ' ').replace('(', ' ').replace(')', ' ')).split()
        #if has no label
        if tokens[0] in mipsDictionaries.instructions:
            tokens = [''] + tokens
        tokens += [''] * (5-len(tokens)) #fills the other 5 slots with ''
        tokens += [lineNumber]
        return tokens

    def resolvePseudoInstructions(line):
        if mipsDictionaries.instructions.get(line[1], -1) == -1: #is NOT recognized
            raise Exception("instruction " + line[1] + " at line " + str(line[5]) +" is not recognized ")
        elif mipsDictionaries.instructions.get(line[1], 0) != 3: #is NOT pseudo
            return [line]
        instructionList = []
        for instruction in mipsDictionaries.pseudoRes(line[1], line[2], line[3], line[4]):
            instructionList.append(differentiateLine(instruction, "Pseudo"))
        return instructionList

    def convertToBP(instruction):
        instructionDic = {}
        bp = mipsDictionaries.instructions[instruction[1]]

        instructionDic["label"] = instruction[0]
        instructionDic["instruction"] = instruction[1]
        count = 2
        for reg in bp[2].split():
            instructionDic[reg] = instruction[count]
            count+=1
        instructionDic["line_number"] = instruction[5]

        return instructionDic

    lineNumber = 1
    newLines = []
    for line in lines:
        if line[0]!='\n' and line[0] != '#':
            newLines.append(differentiateLine(line, lineNumber))
        lineNumber += 1
    lines = newLines
    pseudoResolvedLines = []
    for line in lines:
        for instruction in resolvePseudoInstructions(line):
            pseudoResolvedLines.append(convertToBP(instruction))

    return pseudoResolvedLines


def calculateLabelAddresses(lines, offset):
    cursor = offset
    labels = {}
    for instruction in lines:
        if instruction["label"] != "": #if it has a label
            if(instruction["label"] in labels):
                raise Exception("Label occurs multiple times, must be unique!")
            labels[instruction["label"]] = cursor
        cursor+=4
    return labels

def resolveLabelsAndRegisters(lines, labels, pc):
    newLines = []
    for instruction in lines:
        newLines.append(dict(instruction))
    for newLine in newLines:
        pc+=4
        try:
            if newLine.get("rs", 0) != 0:
                newLine["rs"] = mipsDictionaries.registers[newLine["rs"]]
            if newLine.get("rt", 0) != 0:
                newLine["rt"] = mipsDictionaries.registers[newLine["rt"]]
            if newLine.get("rd", 0) != 0:
                newLine["rd"] = mipsDictionaries.registers[newLine["rd"]]
        except Exception:
            raise Exception("Invalid register at line "+str(newLine["line_number"]))
        if newLine.get("offset", 0) != 0:
            if labels.get(newLine["offset"], -1) == -1:
                raise Exception("Label "+ newLine["offset"] + " not found at line " + str(newLine["line_number"]))
            newLine["offset"] = str((int(labels[newLine["offset"]])-pc)//4)
        if newLine.get("dest", 0) != 0:
            if labels.get(newLine["dest"], -1) == -1:
                raise Exception("Label "+ newLine["dest"] + " not found at line " + str(newLine["line_number"]))
            newLine["dest"] = str(((int(labels[newLine["dest"]]))//4))
    return newLines

def assemble(lines):
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

    binaryInstructions = []

    for instruction in lines:
        instructionBP = mipsDictionaries.instructions[instruction["instruction"]]
        assembled = str(instructionBP[0])
        assembled = assembled.replace("opcode ", instructionBP[1])

        assembled = assembled.replace("rs ", toBinary(instruction.get("rs", '0'), 5))
        assembled = assembled.replace("rt ", toBinary(instruction.get("rt", '0'), 5))
        assembled = assembled.replace("rd ", toBinary(instruction.get("rd", '0'), 5))
        assembled = assembled.replace("sa ", toBinary(instruction.get("sa", '0'), 5))

        if "function" in assembled:
            assembled = assembled.replace("function", instructionBP[3])

        if "immediate" in instruction:
            assembled = assembled.replace("immediate", toBinary(instruction["immediate"], 16))
        elif "offset" in instruction:
            assembled = assembled.replace("immediate", toBinary(instruction["offset"], 16))
        elif "dest" in instruction:
            assembled = assembled.replace("target", toBinary(instruction["dest"], 26))

        binaryInstructions.append(assembled)
            
    return binaryInstructions

def toHexInstructions(lines):
    return ["0x"+("{}".format(hex(int(instruction, 2))).replace('0x', '').zfill(8)) for instruction in lines]

def fullProcedure(lines, offset, verbose):
    lines = parseInstructions(lines)
    if verbose:
        for line in lines:
            print(str(line))
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