import math
import time

from sympy import *

import DIMACS_reader
import numpy

# 4x4
# sudokus_file = "TXT/4x4.txt"
# location_rules = "sudoku-rules-4x4.txt"

# 9x9
# sudokus_file = "TXT/1000 sudokus.txt"
sudokus_file = "TXT/top100.sdk.txt"  # average time: 2.5473659467697143  with a std of  2.757161616124923
location_rules = "sudoku-rules.txt"


# 16x16
# sudokus_file = "TXT/16x16.txt"
# location_rules = "sudoku-rules-16x16.txt"


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
    unit_clauses = list(clause for clause in clauses if len(clause) == 1)

    for clause in unit_clauses:
        # to get the literal as a literal not as a clause
        literal = clause[0]

        if [-literal] in unit_clauses:
            return None, None

        # call the bcp for unit_clauses simplification
        clauses = bcp(clauses, literal)
        if clauses is None:
            return None, None

        # set literal in literals equal to True or False
        literals[abs(literal)] = literal > 0
    return literals, clauses


# def unit_propagation(clauses):
#     literals = dict()
#     # filter clauses if length of clause is 1
#     unit_clauses = [c[0] for c in clauses if len(c) == 1]
#
#     while len(unit_clauses) > 0:
#         literal = int(unit_clauses[0])
#
#         # call the bcp for unit_clauses simplification
#         clauses = bcp(clauses, literal)
#         unit_clauses = [c[0] for c in clauses if len(c) == 1]
#
#         # TODO: it enters in this contraddiction check: unit = 390, apparently unit_clauses containes -390,
#         # even if I checked in the clauses and there is no unit clause for -390, only for 390
#
#         # contradiction check
#         for unit in unit_clauses:
#             if -unit in unit_clauses:
#                 return None, None
#
#         # set x in literals equal to True or False
#         literals[abs(literal)] = literal > 0
#
#     return literals, clauses


def dp_solver(clauses, literals):
    if clauses is None:
        return None

    unit_literals, clauses = unit_propagation(clauses)

    if clauses is None:
        return None

    literals.update(unit_literals)

    if not clauses:
        return literals

    # splitting
    literal = clauses[0][0]  # TODO: can be improved to make it random
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
    counter = 0
    for i in literals:
        if literals[i] is True:
            counter += 1
    size = int(math.sqrt(counter))

    if size < 10:
        base = 10
    else:
        base = 17

    matrix = [[0 for x in range(size)] for x in range(size)]
    for key, value in literals.items():
        if key > 0 and value:
            matrix[int((key / base ** 2)) - 1][int(key / base) % base - 1] = key % base

    print('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in matrix]))
    return matrix


def verify_solution(literals):
    matrix = print_solution(literals)
    size = len(matrix)
    for i in range(size - 1):
        count = [0] * size
        for index in matrix[i][:]:
            count[index - 1] = count[index - 1] + 1

        if not filter(lambda item: item != 1, count):
            print("invalid solution for row: ", i)
            return

        count = [0] * size
        for index in matrix[:][i]:
            count[index - 1] = count[index - 1] + 1

        if not filter(lambda item: item != 1, count):
            print("invalid solution for column: ", i)
            return

        count = [0] * size
        block_size = int(size ** (1 / 2))
        for index in flatten(matrix[int(i / block_size):int(i / block_size) + block_size - 1][
                             (i % block_size): (i % block_size) + block_size - 1]):
            count[index - 1] = count[index - 1] + 1

        if not filter(lambda item: item != 1, count):
            print("invalid solution for block: ", int(i / block_size), i % block_size)
            return
    print("Solution is correct")


def main(clauses):
    # dictionary containing for each literals (as key value) a boolean value
    literals = dict()

    # check for tautologies just once at the beginning
    clauses = remove_tautologies(clauses)

    # call the solver
    literals = dp_solver(clauses, literals)
    return literals

    # if literals:
    #     # solution = [x for x in literals.keys() if literals[x] is True and x > 0]
    #     # print(solution)
    #     # verify_solution(literals)
    #     return 1
    # else:
    #     print("no solution for this problem")
    #     return 0


if __name__ == '__main__':

    rules, size = DIMACS_reader.get_rules(location_rules)
    games = DIMACS_reader.transform(sudokus_file)

    # to check, only one game is played at time, but needed to do a loop for testing all the games
    # choose a game in games. For example the first one (games[0])

    times = []
    total_time = 0
    for game in games:
        clauses = DIMACS_reader.get_clauses(game, rules)

        start = time.time()
        solution = main(clauses)
        runtime = time.time() - start

        if solution:
            total_time += runtime
            times.append(runtime)
        else:
            print("no solution for game :", games.index(game))

    print("solved", len(times), " puzzle out of ", len(games),
          " games on average time:", numpy.mean(times), " with a std of ", numpy.std(times))
