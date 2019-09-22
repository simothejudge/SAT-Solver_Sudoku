"""For reading in DIMACS file format
www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/satformat.ps
Source: (to mention the reference)
"""
#TODO: first call get_rules(f), then get a list of games from transform(f), then call the get_clauses to combine them

from __future__ import print_function,division

import re
import string


def transformline(line):
    #transfroms each sudoku line into a dimacs format string
    n = len(line)
    size = int (n ** (1 / 2))
    sudoku = ""
    for i in range(0, n):
        if line[i] != '.':
            if line[i] is int:
                value = int(line[i])
            else:
                value = translate(line[i])
            row = int((i / size))+1
            col = (i % size)+1
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
    while len(lines) > 0:
        line = lines.pop(0)

        # Only deal with lines that aren't comments
        if not pComment.match(line):
            m = pStats.match(line)
            if not m:
                clauses = get_list(line)
            else:
                infos = line.rstrip('\n').split(' ')
                variables = int(infos[2])
    return clauses, variables


def get_list(line):
    #returns the clauses from a string
    clauses = []
    assert isinstance (line.rstrip ('\n').split,object)
    nums = line.rstrip ('\n').split (' ')
    list = []
    for lit in nums:
        if lit != '':
            if int(lit) == 0:
                continue
            num = int (lit)
            list.append (num)
    if len (list) > 0:
        clauses.append (list)
    return clauses


# function to get the rules of the sudoku as a list of clauses and the number of maximum variables expected (size)
def get_rules(f):
    with open(f) as file:
        s = file.read()
    clauses, size = load(s)
    return clauses , size

# function to read the example.txt and get the list of initial constraints
def get_game(f):
    with open (f) as file:
        s = file.read ()
    partial = load(s)
    return partial

#function to combine into the clauses of constraints both the partial initial solution (a string) and the sudoku rules (a list of list)
def get_clauses(partial, rules):
    first_clauses = get_list(partial)
    return first_clauses + rules




