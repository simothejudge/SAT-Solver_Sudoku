"""
What functions we need?
    check

"""
import DIMACS_reader
from sympy import *

location_sudoku = "sudoku-example (1).txt"
location_rules = "sudoku-rules.txt"

#TODO: TRY AND RUN ON SUDOKU TRIAL

def DP_solver(clauses, literals):
    #check unit clauses
    unit_clauses = [c for c in clauses if len(c) == 1]
    if unit_clauses is not {}:
        for unit in unit_clauses:
            x = int(unit)
            print ("unit clause= ", x)
            if x > 0:
                literals[x] = True
            else:
                literals[x] = False
            for clause in clauses:
                if x in clause:
                    print ("x contained in clause: ", clause, " --> removing clause")
                    clauses.remove(clause)
                if -x in clause:
                    print("-x contained in clause: ", clause, " --> removing -x from this clause")
                    new_clause = clause.remove(-x)
                    print("new clause: ", new_clause)
                    clauses[clause] = new_clause
    return True






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


        



def checkTaut(clauses, literals):
    for x in literals: #literals is a list or a dic? to check
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

    #literals = {111:None, 112:None, 113:None, 114:None, 115:None, 116:None, 117:None, 118:None, 119:None, 121:None}
    #TODO: get the size of literals from DIMACS, and declaire the dict list of keys value (111, 112, ... 999) literals[x]='' take out all the variables containing 0
    #clauses = [[111], [113], [111, 112, 113, 114, 115, 116, 117, 118, 119], [-111, -112], [-111, -113], [-111, 111]]


    #solution, literals = DP_solver(clauses, literals)
    # if solution == false:
        #print ("Problem UNSATISFIABLE")

    # call for recursive function (DP_solver)


if __name__ == '__main__':
    main()
