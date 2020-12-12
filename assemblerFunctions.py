import mipsDictionaries
import re
#label, instruction, register or label, register or immediate, register or continue immediate

#RUN 1, split instructions into format, and resolve pseudoinstructions into real ones
def formatAndResolveInstructions(lines):
    def differentiateLine(line):
        if('(' in line):
            tokens = line.replace(',', '').replace('\n', '').replace(':', '').replace('(', ' ').replace(')', '').split()
            temp = tokens[2]
            tokens[2] = tokens[3]
            tokens[3] = temp
        else:
            tokens = line.replace(',', '').replace('\n', '').replace(':', '').split()

        #if has no label
        if tokens[0] in mipsDictionaries.instructions:
            tokens = [""] + tokens
        while(len(tokens) < 5):
            tokens = tokens + [""]
        return tokens

    def resolvePseudoInstructions(line):
        if mipsDictionaries.instructions[line[1]] != 3: #3 is NOT pseudo
            return line
        instructionList = []
        instructions = mipsDictionaries.pseudoInstructionResolution[line[1]]
        for instruction in instructions:
            instructionList.append(instruction.replace("LABEL", line[4]).replace('A', line[2]).replace('B', line[3]))
        return instructionList

    lines = [differentiateLine(i) for i in lines]
    pseudoResolvedLines = []
    for line in lines:
        if mipsDictionaries.instructions[line[1]] != 3: #3 is NOT pseudo
            pseudoResolvedLines.append(line)
        else:
            for instruction in resolvePseudoInstructions(line):
                pseudoResolvedLines.append(differentiateLine(instruction))

    return pseudoResolvedLines


#RUN 2, calculate label addresses
def calculateLabelAddresses(lines, offset):
    cursor = offset
    labels = {}
    for instruction in lines:
        if instruction[0]: #if it has a label
            if(instruction[0] in labels):
                raise Exception("Label occurs multiple times, must be unique!")
            labels[instruction[0]] = cursor
            cursor+=4
    return labels

#RUN 3, replace labels with addresses and registers with values
#DESTRUCTIVE!
def resolveLabelsAndRegisters(lines, labels, registers):
    for instructionIndex in range(len(lines)):
        for tokenIndex in range(len(lines[instructionIndex])):
            if tokenIndex == 0 or tokenIndex == 1:
                continue
            if lines[instructionIndex][tokenIndex] == '' or\
            lines[instructionIndex][tokenIndex].isnumeric():
                continue
            if lines[instructionIndex][tokenIndex][0] == '$':
                lines[instructionIndex][tokenIndex] = registers.get(
                    lines[instructionIndex][tokenIndex],
                    "UNRESOLVED_REGISTER"
                )
            else:
                lines[instructionIndex][tokenIndex] = labels.get(
                    lines[instructionIndex][tokenIndex],
                    "UNRESOLVED_LABEL"
                )
    return lines

#RUN 4, convert instructions to binary
def toBinaryInstructions(lines):
    def toBinary(numberString, length):
        return '{0:b}'.format(int(numberString)).zfill(length)

    binaryInstruction = []
    for instruction in lines:
        instructionType = mipsDictionaries.instructions[instruction[1]]
        if instructionType == 0: #if R
            binaryInstruction.append(
                mipsDictionaries.opcode[instruction[1]] +\
                toBinary(instruction[3], 5) +\
                toBinary(instruction[4], 5) +\
                toBinary(instruction[2], 5) +\
                "00000" +\
                mipsDictionaries.RFunction[instruction[1]]
            )
        elif instructionType == 1: #if I
            binaryInstruction.append(
                mipsDictionaries.opcode[instruction[1]] +\
                toBinary(instruction[3], 5) +\
                toBinary(instruction[2], 5) +\
                toBinary(instruction[4], 16)
            )
        else: #is J
            binaryInstruction.append(
                mipsDictionaries.opcode[instruction[1]] +\
                toBinary(instruction[2], 26)
            )
    return binaryInstruction

#RUN 5, to hex
def toHexInstructions(lines):
    return ["{}".format(hex(int(instruction, 2))) for instruction in lines]

def fullProcedure(lines, offset):
    lines = formatAndResolveInstructions(lines)#RUN 1
    labels = calculateLabelAddresses(lines, offset)#RUN 2
    lines = resolveLabelsAndRegisters(lines, labels, mipsDictionaries.registers)#RUN 3
    lines = toBinaryInstructions(lines)#RUN 4
    lines = toHexInstructions(lines)#RUN 5
    return lines