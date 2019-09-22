"""For reading in DIMACS file format
www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/satformat.ps
Source: (to mention the reference)
"""
# TODO: first call get_rules(f), then get a list of games from transform(f), then call the get_clauses to combine them

from __future__ import print_function,division

import re
import string


def transformline(line):
    # transforms each sudoku line into a dimacs format string
    n = len(line)
    size = int(n ** (1 / 2))
    sudoku = ""

    for i in range(0, n):
        if line[i] != '.':
            if line[i].isdigit():
                value = int(line[i])
            else:
                value = translate(line[i])
            row = int((i / size))+1
            col = (i % size)+1
            if size <= 9:
                dimacs = "".join([str(row), str(col), str(value)])
            else:
                dimacs = row*(size+1)**2+col*(size+1)+value
            sudoku += str(dimacs)+" 0"+'\n'
    return sudoku


def translate(char):
    # assigns letters to values for dimacs translation
    for alfa, cont in enumerate(string.ascii_uppercase):
        if char == alfa:
            return cont+10
    return -1


def transform(location):
    #transforms the file with sudokus into a list of strings in dimacs format
    sudokus = []
    with open(location) as loc:
        page = loc.read()
        lines = page.split ('\n')
        for line in lines:
            sudokus.append(transformline(line))
    return sudokus


def load(s):
    # gets the file of rules and puts it in a list of clauses
    lines = s.split('\n')
    pComment = re.compile(r'c.*')
    pStats = re.compile(r'p\s*cnf\s*(\d*)\s*(\d*)')
    variables = 0
    clauses = []
    while len(lines) > 0:
        line = lines.pop(0)

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


def get_rules(f):
    # function to get the rules of the sudoku as a list of clauses and the number of maximum variables expected (size)
    with open(f) as file:
        s = file.read()
    clauses, size = load(s)
    return clauses, size


def get_game(f):
    # function to read the example.txt and get the list of initial constraints
    with open(f) as file:
        s = file.read ()
    partial = load(s)
    return partial


def get_clauses(partial, rules):
    # function to combine into the clauses of constraints both
    # the partial initial solution (a string) and the sudoku rules (a list of list)
    partial = partial.replace("0\n", "")
    first_clauses = get_list(partial)
    if '' in first_clauses:
        first_clauses = first_clauses.remove('')

    return list(([clause] for clause in first_clauses)) + rules




