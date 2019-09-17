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
        else
        return False



        
def UnitPropagate(clauses, literals):
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
    #TODO: get the size of literals from DIMACS, and declaire the dict list of keys value (111, 112, ... 999) literals[x]=''
    clauses = [[168], [175], [225], [231], [318], [419], [444], [465], [493], [689], [692], [727], [732], [828], [886], [956], [961], [973], [111, 112, 113, 114, 115, 116, 117, 118, 119], [-111, -112], [-111, -113], [-111, 111]]
    clauses = checkTaut(clauses, literals)
    print (clauses)
    #solution, literals = DP_solver(clauses, literals)
    # if solution == false:
        #print ("Problem UNSATISFIABLE")

    # call for recursive function (DP_solver)


if __name__ == '__main__':
    main()
