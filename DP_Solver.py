
import DIMACS_reader
from sympy import *
import random


location_sudoku = "sudoku-example (1).txt"
location_rules = "sudoku-rules.txt"

#TODO: Problem of loop is solved, but still errors regarding types of objects (check clauses type cause it gives errors)
#   error:   unit_clauses = [c[0] for c in clauses if len(c) == 1]  --> TypeError: 'int' object is not iterable

#TODO: I added the call of bcp at the beginning, because I realized we simplify the clauses only when there are unit_clauses otherwise,
#   and not when we do the splitting. Not sure it is located in the right place

#TODO: Problems with the matrix design in the main (int object is not subscriptable)


def DP_solver(clauses, literals, var, value):

    if var != None and value!= None:
        literals[var] = value
        if value == True:
            clauses = bcp(clauses, var)
        else:
            clauses = bcp(clauses, -var)

    #check unit clauses
    unit_clauses = []
    if len(clauses) > 0:
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        #print(unit_clauses)
    while len(unit_clauses)>0:
        #print(unit_clauses)
        x = int(unit_clauses[0])
        #print("unit_var:", x)

        # call the bcp for unit_clauses simplification
        clauses = bcp(clauses, x)
        unit_clauses = [c[0] for c in clauses if len(c) == 1]

        # contraddiction check
        for unit in unit_clauses:
            if -unit in unit_clauses:
                return False, None

        # set x in literals equal to True or False
        if x > 0:
            literals [x] = True
            # print(x, literals[x])
        elif x < 0:
            literals [-x] = False

    #print(clauses)
    if clauses == -1:
        return False, None
    if clauses == []:
        return True, literals

    #splitting
    vars = [v for v in literals.keys () if literals[v] == None]
    # print (vars)
    l = random.choice(vars)
    if DP_solver(clauses,literals, l, True) :
        return True, literals
    elif DP_solver(clauses,literals, l, False):
        return True, literals
    else:
        return False, None


def bcp(clauses, literal):
    new_clauses = []
    for clause in clauses:
        if literal in clause:
            continue
        elif -literal in clause:
            new_clause = [x for x in clause if x != -literal]
            if(new_clause == []):
                return -1
            new_clauses.append(new_clause)
        else:
            new_clauses.append(clause)
    if len(new_clauses) == 0 :
        return []
    #print (new_clauses)
    return new_clauses


def checkTaut(clauses, literals):
    for x in literals:
        for clause in clauses:
            if x in clause and -x in clause:
                #print("found a taut")
                clauses.remove(clause)
    return clauses
"""
def print_sudoku(board):
    print("-"*37)
    for i, row in enumerate(board):
        print(("|" + " {}   {}   {} |"*3).format(*[x if x != 0 else " " for x in row]))
        if i == 8:
            print("-"*37)
        elif i % 3 == 2:
            print("|" + "---+"*8 + "---|")
        else:
            print("|" + "   +"*8 + "   |")
"""


def main():
    clauses, n_var = DIMACS_reader.load_file(location_sudoku, location_rules)
    literals = dict()  #dictionary containing for each literals (as key value) a boolean value that is initialized to None
    size = 0  # number of variables

    #initialisation of the literals
    for x in range(111, n_var+1):
        if '0' not in str(x):
            size += 1
            literals[x] = None

    #print (size, literals)

    #check for tautologies just once at the beginning
    clauses = checkTaut(clauses, literals)

    #call the solver
    check, new_literals = DP_solver(clauses, literals, None, None)
    if check == True:
        printSolution(literals)
        # print ("found a solution: ")
        # solution = [x for x in new_literals.keys() if new_literals[x] == True]
        #
        # board = [int(str(x)[2]) for x in solution]
        #
        # #print_sudoku(board)


    else:
        print("no solution for this sudoku")
    # Print result
    # if solution == false:
        #print ("Problem UNSATISFIABLE")


def printSolution(literals):
    matrix = [[0 for x in range(9)] for x in range(9)]
    for key, value in literals.items():
        if value:
            matrix[int(key / 100) - 1][int((key % 100) / 10) - 1] = key % 10

    print('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in matrix]))

if __name__ == '__main__':
    main()
