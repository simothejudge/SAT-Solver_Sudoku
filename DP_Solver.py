"""
What functions we need?
    check

"""
import DIMACS_reader
from sympy import *
import random


location_sudoku = "sudoku-example (1).txt"
location_rules = "sudoku-rules.txt"

#TODO: TRY AND RUN ON SUDOKU TRIAL





def DP_solver(clauses, literals, var, value):

    if var != None and value!= None:
        literals[var] == value

    #check unit clauses
    unit_clauses = [c[0] for c in clauses if len(c) == 1]
    while len(unit_clauses)>0:
        #print(unit_clauses)
        x = int(unit_clauses[0])

        # call the bcp for unit_clauses simplification
        clauses = bcp(clauses, x)
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        for unit in unit_clauses:
            if -unit in unit_clauses:
                return False, None #validation for contraddictions

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

    vars = [v for v in literals.keys () if literals [v] == None]
    # print (vars)
    l = random.choice(vars)
    if DP_solver(clauses,literals, l, True):
        return True, literals
    elif DP_solver(clauses,literals, l, False):
        return True, literals
    else:
        return False, None
    

    """
            for clause in clauses:
                if x in clause:
                    print (x, " contained in clause: ", clause, " --> removing clause")
                    clauses.remove(clause)
                if -x in clause:
                    print( x,  "contained in clause: ", clause, " --> removing ", -x, " from this clause")
                    new_clause = clause
                    new_clause.remove(-x)
                    print("new clause: ", new_clause)
                    clauses.remove(clause)
                    clauses.append(new_clause)
                    if len(new_clause) == 1:
                        print("adding another unit clause to unit_clauses", new_clause[0])
                        unit_clauses.append(new_clause[0])
    """

"""
def check_unit(clauses):
    unit_clauses = [c for c in clauses if len(c) == 1]
    for clause in unit_clauses:
        x = int(clause)
        if x > 0:
            literals[x] = True
        else:
            literals[x] = False

            #assign true to literals list
            #call DP_solver over the new literals and
    #cont = 0
    #while clauses not empty do:

     #   cont+=1

"""


def bcp(clauses, literal):
    new_clauses = []
    for clause in clauses:
        if (literal not in clause) & (-literal not in clause):
            new_clauses.append(clause)
        elif -literal in clause:
            new_clause = [x for x in clause if x != -literal]
            new_clauses.append(new_clause)
    if new_clauses == []:
        return -1
    return new_clauses


def checkTaut(clauses, literals):
    for x in literals:
        for clause in clauses:
            if x in clause and -x in clause:
                #print("found a taut")
                clauses.remove(clause)
    return clauses


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
        print ("found a solution: ")
        solution = [x for x in new_literals.keys() if new_literals[x] == True]
        mat = [[]]
        for cell in solution:
            mat[cell[0]][cell[2]] = cell[2]
        print(mat)
    else:
        print("no solution for this sudoku")
    # Print result
    # if solution == false:
        #print ("Problem UNSATISFIABLE")


if __name__ == '__main__':
    main()
