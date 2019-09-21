"""For reading in DIMACS file format
www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/satformat.ps

Source: (to mention the reference)
"""

from __future__ import print_function,division

import re


def transform(location):
    sudokus = []
    with open(location) as loc:
        page = loc.read()
        lines = page.split ('\n')

        n = enumerate(lines[0])
        size = n**(1/2)
        for line in lines:
            col = 1
            row = 1
            while row <= size:
                char = line[col-1]
                if col<=size:
                    col += 1
                else:
                    col=1
                    row+=1
                if char =! '.':



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
    with open(loc1) as l1:
        with open(loc2) as l2:
            s1 = l1.read()
            s2 = l2.read()
    f1, size = load(s1)
    if size !=0 :
        nvar = size
    f2, size = load(s2)
    if size !=0 :
        nvar = size
    return (f1+f2), nvar

"""
to test only the DIMACS reader: 

location_sudoku = "sudoku-example (1).txt"
location_rules = "sudoku-rules.txt"
f = load_file(location_sudoku, location_rules)
print (f)
"""
sudokus = transform("TXT/4x4.txt")


