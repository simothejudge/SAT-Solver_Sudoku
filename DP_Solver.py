
import DIMACS_reader
from sympy import *
import random

sudokus_file = "TXT/4x4.txt"
#location_sudoku = "sudoku-example .txt"
location_rules = "sudoku-rules-4x4.txt"

#TODO: Literals initialisazion: to get them from the clauses set
#TODO: check with 4x4 sudokus and 16x16 sudokus
#TODO: Heursistics and Backtracking implementation
#TODO: Experiments and Statistics


def unit_propagation(clauses):
    unit_literals = dict()
    unit_clauses = list(filter(lambda clause: len(clause) == 1, clauses))
    for clause in unit_clauses:
        clauses.remove(clause)
    return dict((clause[0], True) for clause in unit_clauses), clauses
    #
    # while len(unit_clauses) > 0:
    #     literal = int(unit_clauses[0])
    #
    #     # call the bcp for unit_clauses simplification
    #     clauses = bcp(clauses, literal)
    #     unit_clauses = [c[0] for c in clauses if len(c) == 1]
    #
    #     # contradiction check
    #     for unit in unit_clauses:
    #         if -unit in unit_clauses:
    #             return False, None
    #
    #     # set x in literals equal to True or False
    #     if literal > 0:
    #         literals[literal] = True
    #         # print(x, literals[x])
    #     elif literal < 0:
    #         literals[-literal] = False
    #
    # # print(clauses)
    # if clauses == -1:
    #     return False, None
    # if clauses == []:
    #     return True, literals

def Split(clauses,literals):

    vars = [v for v in literals.keys () if literals[v] == None]
    # print (vars)
    l = random.choice(vars)
    if DP_solver(clauses,literals, l, True) :
        return True, literals
    elif DP_solver(clauses,literals, l, False):
        return True, literals
    else:
        return False, None


def DP_solver(clauses, literals, var, value):

    unit_propagation(clauses, literals)
    if var != None and value!= None:
        literals[var] = value
        if value == True:
            clauses = bcp(clauses, var)
        else:
            clauses = bcp(clauses, -var)

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


def is_tautology(clause):
    for literal in clause:
        if -literal in clause:
            return True
    return False


def remove_tautologies(clauses):
    # return list((clause for clause in clauses if not is_clause_tautology(clause)))
    return list(filter(lambda clause: not is_tautology(clause), clauses))


def main(clauses):
    literals = dict()  #dictionary containing for each literals (as key value) a boolean value

    #check for tautologies just once at the beginning
    clauses = remove_tautologies(clauses)

    #call the solver
    check, new_literals = DP_solver(clauses, literals, None, None)
    if check == True:
        verify_solution(literals)
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


def print_solution(literals):
    matrix = [[0 for x in range(9)] for x in range(9)]
    for key, value in literals.items():
        if value:
            matrix[int(key / 100) - 1][int((key % 100) / 10) - 1] = key % 10

    print('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in matrix]))
    return matrix


def verify_solution(literals):
    matrix = print_solution(literals)
    for i in range(9):
        count = [0] * 9
        for index in matrix[i][:]:
            count[index-1] = count[index-1]+1

        if not filter(lambda item: item != 1, count):
            print("invalid solution for row: ", i)
            return

        count = [0] * 9
        for index in matrix[:][i]:
            count[index-1] = count[index-1]+1

        if not filter(lambda item: item != 1, count):
            print("invalid solution for column: ", i)
            return

        count = [0] * 9
        for index in flatten(matrix[int(i / 3):int(i / 3)+3][(i % 3): (i % 3)+3]):
            count[index-1] = count[index-1] + 1

        if not filter(lambda item: item != 1, count):
            print("invalid solution for block: ", int(i / 3), i % 3)
            return
    print("Solution is correct")


if __name__ == '__main__':
    main()
