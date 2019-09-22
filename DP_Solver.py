import DIMACS_reader
from sympy import *
import random

sudokus_file = "TXT/4x4.txt"
# location_sudoku = "sudoku-example .txt"
location_rules = "sudoku-rules-4x4.txt"


# TODO: Literals initialisazion: to get them from the clauses set
# TODO: check with 4x4 sudokus and 16x16 sudokus
# TODO: Heursistics and Backtracking implementation
# TODO: Experiments and Statistics


def bcp(clauses, literal):
    simplified_clauses = []
    for clause in clauses:
        if literal in clause:
            continue
        elif -literal in clause:
            new_clause = [x for x in clause if x != -literal]
            if not new_clause:
                return None
            simplified_clauses.append(new_clause)
        else:
            simplified_clauses.append(clause)
    if len(simplified_clauses) == 0:
        return []
    return simplified_clauses


def unit_propagation(clauses):
    literals = dict()
    # filter clauses if length of clause is 1
    unit_clauses = [c[0] for c in clauses if len(c) == 1]

    while len(unit_clauses) > 0:
        literal = int(unit_clauses[0])

        # call the bcp for unit_clauses simplification
        clauses = bcp(clauses, literal)
        unit_clauses = [c[0] for c in clauses if len(c) == 1]

        # contraddiction check
        for unit in unit_clauses:
            if -unit in unit_clauses:
                return None

        # set x in literals equal to True or False
        literals[abs(literal)] = literal > 0

    return literals, clauses


def dp_solver(clauses, literals):
    unit_literals, clauses = unit_propagation(clauses)
    literals.update(unit_literals)

    if clauses is None:
        return None
    if not clauses:
        return literals

    # splitting
    literal = clauses[0][0]
    literals[literal] = True
    solution = dp_solver(bcp(clauses, literal), literals)
    if solution is None:
        literals[literal] = False
        solution = dp_solver(bcp(clauses, -literal), literals)
    return solution


def is_tautology(clause):
    for literal in clause:
        if -literal in clause:
            return True
    return False


def remove_tautologies(clauses):
    # return list((clause for clause in clauses if not is_clause_tautology(clause)))
    return list(filter(lambda clause: not is_tautology(clause), clauses))


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
            count[index - 1] = count[index - 1] + 1

        if not filter(lambda item: item != 1, count):
            print("invalid solution for row: ", i)
            return

        count = [0] * 9
        for index in matrix[:][i]:
            count[index - 1] = count[index - 1] + 1

        if not filter(lambda item: item != 1, count):
            print("invalid solution for column: ", i)
            return

        count = [0] * 9
        for index in flatten(matrix[int(i / 3):int(i / 3) + 3][(i % 3): (i % 3) + 3]):
            count[index - 1] = count[index - 1] + 1

        if not filter(lambda item: item != 1, count):
            print("invalid solution for block: ", int(i / 3), i % 3)
            return
    print("Solution is correct")


def main(clauses):
    # dictionary containing for each literals (as key value) a boolean value
    literals = dict()

    # check for tautologies just once at the beginning
    clauses = remove_tautologies(clauses)

    # call the solver
    literals = dp_solver(clauses, literals)
    if literals:
        verify_solution(literals)
    else:
        print("no solution for this problem")


if __name__ == '__main__':
    rules, size = DIMACS_reader.get_rules(location_rules)
    games = DIMACS_reader.transform(sudokus_file)

    # to check, only one game is played at time, but needed to do a loop for testing all the games
    # choose a game in games. For example the first one (games[0])
    clauses = DIMACS_reader.get_clauses(games[0], rules)

    main(clauses)
