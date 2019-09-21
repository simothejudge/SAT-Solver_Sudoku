"""For reading in DIMACS file format
www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/satformat.ps

Source: (to mention the reference)
"""

from __future__ import print_function,division

import re


def transformline(line):
    n = len(line)
    size = int (n ** (1 / 2))
    sudoku = ""
    for i in range(0, n):
        if line [i] != '.':
            value = line[i]
            row = hex(int((i / size))+1)
            col = hex((i % size)+1)
            sudoku+=str(row)[2:].upper()+str(col)[2:].upper()+str(value)+" 0"+'\n'
    return sudoku


def transform(location):
    sudokus = []
    with open(location) as loc:
        page = loc.read()
        lines = page.split ('\n')
        for line in lines:
            sudokus.append(transformline(line))
    return sudokus

def load(s):
    clauses = []

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
                assert isinstance(line.rstrip('\n').split, object)
                nums = line.rstrip('\n').split(' ')
                list = []
                for lit in nums:
                    if lit != '':
                        if int(lit) == 0:
                            continue
                        num = int(lit)
                        list.append(num)
                if len(list) > 0:
                    clauses.append(list)
            else:
                infos = line.rstrip('\n').split(' ')
                variables = int(infos[2])
    return clauses, variables


def load_file(loc1, loc2):
    """Loads a boolean expression from a file."""
    nvar = 0
    sudokus = transform(loc1)
    with open(loc2) as l:
        s = l.read()
    f, size = load(s)
    if size !=0:
        nvar = size
    clauses = []
    for sudoku in sudokus:
        clauses.append(sudoku+f)
    return clauses, nvar

"""
to test only the DIMACS reader: 

location_sudoku = "sudoku-example (1).txt"
location_rules = "sudoku-rules.txt"
f = load_file(location_sudoku, location_rules)
print (f)
"""
sudokus = transform("TXT/4x4.txt")


