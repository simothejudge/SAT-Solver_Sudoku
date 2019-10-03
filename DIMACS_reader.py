"""For reading in DIMACS file format
www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/satformat.ps
Source: (to mention the reference)
"""
import re
import string


def char_to_int(char):
    # assigns letters to values for dimacs translation
    for alfa, cont in enumerate(string.ascii_uppercase):
        if char == alfa:
            return cont + 10
    return -1


def read_sudoku(line):
    # reads a line of sudoku and converts it into a list clauses
    n = len(line)
    size = int(n ** (1 / 2))
    literals = []

    for i in range(0, n):
        if line[i] != '.':
            if line[i].isdigit():
                value = int(line[i])
            else:
                value = char_to_int(line[i])
            row = int((i / size)) + 1
            col = (i % size) + 1
            if size <= 9:
                literal = "".join([str(row), str(col), str(value)])
            else:
                literal = row * (size + 1) ** 2 + col * (size + 1) + value
            literals.append([int(literal)])
    return literals


def get_list(line):
    # returns the clauses from a string
    clause = []
    assert isinstance(line.rstrip('\n').split, object)
    nums = line.rstrip('\n').split(' ')
    for lit in nums:
        if lit != '':
            if int(lit) == 0:
                continue
            num = int(lit)
            clause.append(num)
    return clause


def get_rules(filename):
    # function to get the rules of the sudoku as a list of clauses and the number of maximum variables expected (size)
    with open(filename) as file:
        lines = file.read().split('\n')
        pComment = re.compile(r'c.*')
        pStats = re.compile(r'p\s*cnf\s*(\d*)\s*(\d*)')
        variables = 0
        clauses = []
        for line in lines:
            # Only deal with lines that aren't comments
            if not pComment.match(line):
                m = pStats.match(line)
                if not m:
                    clause = get_list(line)
                    if clause:
                        clauses.append(clause)
                else:
                    infos = line.rstrip('\n').split(' ')
                    variables = int(infos[2])
        return clauses, variables


def get_games(filename):
    # function to read the example.txt and get the list of initial constraints
    with open(filename) as file:
        lines = file.read().split('\n')
        return [read_sudoku(line) for line in lines]
