"""
What functions we need?
    check

"""
import DIMACS_reader
from sympy import *

location_sudoku = "sudoku-example (1).txt"
location_rules = "sudoku-rules.txt"


"""
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
    
"""
def checkTaut(clauses):
    for clause in clauses:
        if clause == (111 | ~111) or clause == (~111 | 111):
            clauses.remove(clause)
    return clauses





def main():
    #clauses = DIMACS_reader.load_file(location_sudoku, location_rules)
    clauses = (168 & 175  & (~111 | ~112) & (~111 | ~113) & (~111 | ~114) & (111 | ~111))
    clauses2 = checkTaut(clauses)
    print (clauses2)
    # call for recursive function (DP_solver)


if __name__ == '__main__':
    main()
