# 0 = R type
# 1 = I type
# 2 = J type
# 3 = pseudo

instructions = {
    #R type
    "add": 0,
    "slt": 0,

    #I type
    "addi": 1,
    "bne": 1,
    "lw": 1,

    #J type
    "j": 2,

    #Pseudo
    "blt": 3,
}

pseudoInstructionResolution = {
    "blt": ("slt $at, A, B", "bne $at, $zero, LABEL"),
}

opcode = {
    "add": "000000",
    "slt": "000000",

    "addi": "001000",
    "bne": "000101",
    "lw": "100011",

    "j": "000010",
}

RFunction = {
    "add": "100000",
    "slt": "101010",
}

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