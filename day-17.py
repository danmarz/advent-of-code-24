#### Part 1
from collections import defaultdict

data = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

data = """Register A: 52884621
Register B: 0
Register C: 0

Program: 2,4,1,3,7,5,4,7,0,3,1,5,5,5,3,0"""

# Parse input data
rA = int(data.splitlines()[0].split(": ")[1])
rB = int(data.splitlines()[1].split(": ")[1])
rC = int(data.splitlines()[2].split(": ")[1])
program = [int(i) for i in data.splitlines()[4].split(": ")[1].split(",")]

# Initialize combo operands mapping
combo_operands = defaultdict(int)
combo_operands.update({0: 0, 1: 1, 2: 2, 3: 3})

instruction_pointer = 0
output = []

# Execution loop
while instruction_pointer < len(program):
    combo_operands[4], combo_operands[5], combo_operands[6] = rA, rB, rC
    opcode, operand = program[instruction_pointer], program[instruction_pointer + 1]

    if opcode == 0:  # adv
        rA = rA // (2 ** combo_operands[operand])
    elif opcode == 1:  # bxl
        rB ^= operand
    elif opcode == 2:  # bst
        rB = combo_operands[operand] % 8
    elif opcode == 3:  # jnz
        if rA != 0:
            instruction_pointer = operand
            continue
    elif opcode == 4:  # bxc
        rB ^= rC
    elif opcode == 5:  # out
        output.append(combo_operands[operand] % 8)
    elif opcode == 6:  # bdv
        rB = rA // (2 ** combo_operands[operand])
    elif opcode == 7:  # cdv
        rC = rA // (2 ** combo_operands[operand])

    instruction_pointer += 2

# Print output as comma-separated values
print(",".join(map(str, output)))

#### Part 2
data = """Register A: 52884621
Register B: 0
Register C: 0

Program: 2,4,1,3,7,5,4,7,0,3,1,5,5,5,3,0"""

import time, re


def load():
    return list(map(int, re.findall(r"\d+", data)))


def run_program(a, b, c, program):
    ip, out, l = 0, [], len(program)
    while ip < l:
        opcode, literal = program[ip : ip + 2]
        # print(f"opcode: {opcode}, literal: {literal}, program: {program}")
        combo = (
            literal
            if literal < 4
            else ([a, b, c][literal - 4] if 0 <= literal - 4 < len([a, b, c]) else 0)
        )
        ip += 2

        match opcode:
            case 0:
                a = a // 2**combo
            case 1:
                b ^= literal
            case 2:
                b = combo % 8
            case 3 if a != 0:
                ip = literal
            case 4:
                b ^= c
            case 5:
                out.append(combo % 8)
            case 6:
                b = a // 2**combo
            case 7:
                c = a // 2**combo
    return out


def find_a(program, a, b, c, prg_pos):
    if abs(prg_pos) > len(program):
        return a
    for i in range(8):
        first_digit_out = run_program(a * 8 + i, b, c, program)[0]
        if first_digit_out == program[prg_pos]:
            e = find_a(program, a * 8 + i, b, c, prg_pos - 1)
            if e:
                return e


def solve(p):
    a, b, c, *program = p
    part1 = run_program(a, b, c, program)
    part2 = find_a(program, 0, b, c, -1)
    return part1, part2


time_start = time.perf_counter()
print(f"Solution: {solve(load())}")
print(f"Solved in {time.perf_counter()-time_start:.5f} Sec.")
