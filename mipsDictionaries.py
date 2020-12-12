# 0 = R type
# 1 = I type
# 2 = J type
# 3 = pseudo

#determine instruction type
instructions = {
    "NAME": "instructions",

    #R type
    "add": 0,
    "and": 0,
    "slt": 0,
    "nor": 0,
    "or": 0,
    "sra": 0,
    "srl": 0,
    "xor": 0,

    #I type
    "addi": 1,
    "bne": 1,
    "lw": 1,
    "andi": 1,
    "beq": 1,
    "lb": 1,
    "lbu": 1,
    "lh": 1,
    "lhu": 1,
    "ori": 1,
    "sb": 1,
    "slti": 1,
    "sh": 1,
    "sw": 1,
    "xori": 1,

    #J type
    "j": 2,
    "jal": 2,

    #Pseudo
    "blt": 3,
}

#resolution pattern
pseudoInstructionResolution = {
    "NAME": "pseudo instruction resolution",

    "blt": ("slt $at, A, B", "bne $at, $zero, LABEL"), #resolves into 2 real instructions
}

#determine opcode
opcode = {
    "NAME": "opcode",

    "add": "000000",
    "slt": "000000",
    "and": "000000",
    "nor": "000000",
    "or": "000000",
    "sra": "000000",
    "srl": "000000",
    "xor": "000000",

    "addi": "001000",
    "bne": "000101",
    "lw": "100011",
    "andi": "001100",
    "beq": "000100",
    "lb": "100000",
    "lbu": "100100",
    "lh": "100001",
    "lhu": "100101",
    "ori": "001101",
    "sb": "101000",
    "slti": "001010",
    "sh": "101001",
    "sw": "101011",
    "xori": "001110",

    "j": "000010",
    "jal": "000011",
}

#for R type, determine function
RFunction = {
    "NAME": "R function",

    "add": "100000",
    "and": "100100",
    "slt": "101010",
    "nor": "100111",
    "or": "100101",
    "sra": "000011",
    "srl": "000010",
    "xor": "100110",
}

#registers
registers = {
    "$zero": 0,
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