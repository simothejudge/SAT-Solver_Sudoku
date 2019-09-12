"""For reading in DIMACS file format
www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/satformat.ps

Source: (to mention the reference)
TODO: add a reader for the first line, to get the size of the variable array
"""

from __future__ import print_function, division

import re
import sympy
from sympy.core import Symbol
from sympy.logic.boolalg import And, Or



def load(s):
    """Loads a boolean expression from a string.
    Examples
    ========
    >>> from sympy.logic.utilities.dimacs import load
    >>> load('1')
    cnf_1
    >>> load('1 2')
    cnf_1 | cnf_2
    >>> load('1 \\n 2')
    cnf_1 & cnf_2
    >>> load('1 2 \\n 3')
    cnf_3 & (cnf_1 | cnf_2)
    """
    clauses = []

    lines = s.split('\n')

    pComment = re.compile(r'c.*')
    pStats = re.compile(r'p\s*cnf\s*(\d*)\s*(\d*)')

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

    return clauses


def load_file(loc1, loc2):
    """Loads a boolean expression from a file."""
    with open(loc1) as l1:
        with open(loc2) as l2:
            s1 = l1.read()
            s2 = l2.read()
    f1 = load(s1)
    f2 = load(s2)
    return (f1+f2)

"""
location_sudoku = "sudoku-example (1).txt"
location_rules = "sudoku-rules.txt"
f = load_file(location_sudoku, location_rules)
print (f)
"""


