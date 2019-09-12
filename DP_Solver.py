"""
What functions we need?
    check

"""
import DIMACS_reader
from sympy import *

location_sudoku = "sudoku-example (1).txt"
location_rules = "sudoku-rules.txt"



def DP_solver(clauses, literals):
    if clauses not empty:

    else:
        print ("Problem UNSATISFIABLE")
        return False
        
def UnitPropagate(clauses, literals):
    cont = 0
    while clauses not empty do:
        cont+=1

    print (cont)


def checkTaut(clauses, literals):
    for x in literals: #literals is a list or a dic? to check
        for clause in clauses:
            if x in clause and -x in clause:
                clauses.remove(clause)
    return clauses


def main():
    #clauses = DIMACS_reader.load_file(location_sudoku, location_rules)
    literals = [111, 112, 113, 114, 115, 116, 117]
    clauses = [[168], [175], [225], [231], [318], [419], [444], [465], [493], [689], [692], [727], [732], [828], [886], [956], [961], [973], [111, 112, 113, 114, 115, 116, 117, 118, 119], [-111, -112], [-111, -113], [-111, 111]]
    clauses = checkTaut(clauses, literals)
    print (clauses)
    # call for recursive function (DP_solver)


if __name__ == '__main__':
    main()
