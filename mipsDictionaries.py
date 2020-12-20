RInstruction = "opcode rs rt rd sa function"
IInstruction = "opcode rs rt immediate"
JInstruction = "opcode target"
Ropcode = "000000"

instructions = {
    #R type, Outblueprint, opcode, inblueprint, funct
    "add": (RInstruction, Ropcode, "rd rs rt ", "100000"),
    "addu": (RInstruction, Ropcode, "rd rs rt ", "100001"),
    "and": (RInstruction, Ropcode, "rd rs rt ", "100100"),
    "break": (RInstruction, Ropcode, "", "001101"),
    "div": (RInstruction, Ropcode, "rs rt ", "011010"),
    "divu": (RInstruction, Ropcode, "rs rt ", "011011"),
    "jalr": (RInstruction, Ropcode, "rd rs ", "001001"),
    "jr": (RInstruction, Ropcode, "rs ", "001000"),
    "mfhi": (RInstruction, Ropcode, "rd ", "010000"),
    "mflo": (RInstruction, Ropcode, "rd ", "001010"),
    "mthi": (RInstruction, Ropcode, "rs ", "010001"),
    "mtlo": (RInstruction, Ropcode, "rs ", "010011"),
    "mult": (RInstruction, Ropcode, "rs rt ", "011000"),
    "multu": (RInstruction, Ropcode, "rs rt ", "011001"),
    "nor": (RInstruction, Ropcode, "rd rs rt ", "100111"),
    "or": (RInstruction, Ropcode, "rd rs rt ", "100101"),
    "sll": (RInstruction, Ropcode, "rd rt sa ", "000000"),
    "sllv": (RInstruction, Ropcode, "rd rt sa ", "000100"),
    "slt": (RInstruction, Ropcode, "rd rs rt ", "101010"),
    "sltu": (RInstruction, Ropcode, "rd rs rt ", "101011"),
    "sra": (RInstruction, Ropcode, "rd rt sa ", "000011"),
    "srav": (RInstruction, Ropcode, "rd rt rs ", "000111"),
    "srl": (RInstruction, Ropcode, "rd rt sa ", "000010"),
    "srlv": (RInstruction, Ropcode, "rd rt rs ", "000110"),
    "sub": (RInstruction, Ropcode, "rd rs rt ", "100010"),
    "subu": (RInstruction, Ropcode, "rd rs rt ", "100011"),
    "syscall": (RInstruction, Ropcode, "", "001100"),
    "xor": (RInstruction, Ropcode, "rd rs rt ", "100110"),

    #I type, Outblueprint, opcode, inblueprint
    "addi": (IInstruction, "001000", "rt rs immediate "),
    "addiu": (IInstruction, "001001", "rt rs immediate "),
    "andi": (IInstruction, "001100", "rt rs immediate "),
    "beq": (IInstruction, "000100", "rt rs offset "),
    "bgez": (IInstruction, "000001", "rs 00001 offset "),
    "bgtz": (IInstruction, "000111", "rs 00000 offset "),
    "blez": (IInstruction, "000110", "rs 00000 offset "),
    "bltz": (IInstruction, "000001", "rs 00000 offset "),
    "bne": (IInstruction, "000101", "rs rt offset "),
    "lb": (IInstruction, "100000", "rt immediate rs "),
    "lbu": (IInstruction, "100100", "rt immediate rs "),
    "lh": (IInstruction, "100001", "rt immediate rs "),
    "lhu": (IInstruction, "100101", "rt immediate rs "),
    "lui": (IInstruction, "001111", "rt immediate "),
    "lw": (IInstruction, "100011", "rt immediate rs "),
    "lwcl": (IInstruction, "110001", "rt immediate rs "),
    "ori": (IInstruction, "001101", "rt rs immediate"),
    "sb": (IInstruction, "101000", "rt immediate rs "),
    "slti": (IInstruction, "001010", "rt rs immediate"),
    "sltiu": (IInstruction, "001011", "rt rs immediate"),
    "sh": (IInstruction, "101001", "rt immediate rs "),
    "sw": (IInstruction, "101011", "rt immediate rs "),
    "swcl": (IInstruction, "111001", "rt immediate rs "),
    "xori": (IInstruction, "001110", "rt rs immediate "),
    
    #J type, Outblueprint, opcode, inblueprint
    "j": (JInstruction, "000010", "dest "),
    "jal": (JInstruction, "000011", "dest "),

    #Pseudo
    "blt": 3,
    "ble": 3,
    "bgt": 3,
    "bge": 3,
    "li": 3,
    "abs": 3,
    "move": 3,
}

#if resolving to only ONE instruction you should use a LIST, cuz a tuple of one is not a tuple
def pseudoRes(pseudo, A, B, C):
    if pseudo == "blt":
        return("slt $at, " + A + ", " + B + "", "bne $at, $zero, " + C)
    elif pseudo == "ble":
        return ("slt $at, " + B + ", " + A, "beq $at, $zero, " + C)
    elif pseudo == "bgt":
        return ("slt $at, " + B + ", " + A, "bne $at, $zero, " + C)
    elif pseudo == "bge":
        return ("slt $at, " + A + ", " + B, "beq $at, $zero, " + C)
    elif pseudo == "li":
        return ("lui $at, "+int(hex(B)>>4, 16), "ori " + A + ", $at, "+int((hex(B)<<1), 16)>>1)
    elif pseudo == "abs":
        return ("addu " + A + ", " + B + ", $zero", "bgez " + B + ", 8", "sub " + A + ", " + B + ", $zero")
    elif pseudo == "move":
        return ["add " + A + ", " + B + ", $zero"]
   

#registers
registers = {
    "$zero": 0,
    "$0": 0,
    "$at": 1,

    "$v0": 2,
    "$v1": 3,

    "$a0": 4,
    "$a1": 5,
    "$a2": 6,
    "$a3": 7,

    "$t0": 8,
    "$t1": 9,
    "$t2": 10,
    "$t3": 11,
    "$t4": 12,
    "$t5": 13,
    "$t6": 14,
    "$t7": 15,

    "$s0": 16,
    "$s1": 17,
    "$s2": 18,
    "$s3": 19,
    "$s4": 20,
    "$s5": 21,
    "$s6": 22,
    "$s7": 23,

    "$t8": 24,
    "$t9": 25,

    "$k0": 26,
    "$k1": 27,

    "$gp": 28,
    "$sp": 29,
    "$fp": 30,
    "$ra": 31,
}

if __name__ == "__main__":
    for item in instructions.keys():
        print(item, end = "")
        if(instructions[item] == 3):
            print(": Pseduo instruction")
        else:
            if (instructions[item][0] == RInstruction):
                print(": R instruction")
            elif (instructions[item][0] == IInstruction):
                print(": I instruction")
            elif (instructions[item][0] == JInstruction):
                print(": J instruction")