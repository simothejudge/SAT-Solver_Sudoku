import random
import time

import numpy

import DIMACS_reader
import heuristics
import verifier

# 4x4
# sudokus_file = "TXT/4x4.txt"
# location_rules = "sudoku-rules-4x4.txt"

# 9x9
# sudokus_file = "TXT/3sudoku"
# sudokus_file = "TXT/ForHeurCheck.txt"

sudokus_file = "TXT/top100.sdk.txt"
# RANDOM: average time: 2.6395707511901856  with a std of  2.2275945704814886
#

# location_rules = "TXT/satproblem"
location_rules = "sudoku-rules.txt"

# 16x16
# sudokus_file = "TXT/16x16.txt"
# location_rules = "sudoku-rules-16x16.txt"

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
        # for every unit in teh list of unit_clauses we simplify the clauses and set literals to true
        literal = clause[0]

        # contradiction check
        if [-literal] in unit_clauses:
            return None, None

        # call the bcp for unit_clauses simplification
        clauses = bcp(clauses, literal)
        if clauses is None:
            return None, None

        # set literal in literals equal to True or False
        if literal > 0:
            literals[abs(literal)] = True
        else:
            literals[abs(literal)] = False

        # literals[abs(literal)] = literal > 0
        # unit_clauses = list (clause for clause in clauses if len (clause) == 1)

    return literals, clauses


def dp_solver(clauses, literals):

    start = time.time()
    if clauses is None:
        return None

    while True:
        unit_literals, clauses = unit_propagation(clauses)

        if clauses is None:
            return None

        if not unit_literals:
            break

        literals.update(unit_literals)

    duration = time.time() - start

    if not clauses:
        return literals

    # SPLITTING
    start = time.time ()
    literal = heuristics.get_random_literal(clauses, "DLCS")

    literals[abs(literal)] = literal > 0
    solution = dp_solver(bcp(clauses, literal), literals)
    if solution is None:
        literals[abs(literal)] = literal < 0
        solution = dp_solver(bcp(clauses, -literal), literals)

    duration = time.time () - start
    return solution


def is_tautology(clause):
    for literal in clause:
        if -literal in clause:
            return True
    return False


def remove_tautologies(clauses):
    # return list((clause for clause in clauses if not is_clause_tautology(clause)))
    return list(filter(lambda clause: not is_tautology(clause), clauses))


def main(clauses):
    # dictionary containing for each literals (as key value) a boolean value
    literals = dict()

    # check for tautologies just once at the beginning
    clauses = remove_tautologies(clauses)

    start = time.time()

    # call the solver
    literals = dp_solver(clauses, literals)

    # process time for the recursive algorithm
    process_time = time.time() - start
    print("----------------------------------------------")
    print("DP_Solver Process time: " + str(process_time))

    if literals:
        solution = [x for x in literals.keys() if literals[x] is True]
        print(numpy.sort(solution), "length: ", len(solution))
        verifier.verify(solution, clauses)
        # verify_solution(literals)
        return 1
    else:
        print("no solution for this problem")
        return 0


if __name__ == '__main__':

    rules, size = DIMACS_reader.get_rules(location_rules)
    games = DIMACS_reader.transform(sudokus_file)

    #global variables
    total_time = 0

    times = []


    # start = time.time()
    # solution = main(rules)
    # runtime = time.time() - start

    # if solution:
    #     total_time += runtime
    #     times.append(runtime)

    for game in games:
        clauses = DIMACS_reader.get_clauses(game, rules)

        # statistics variables for every game
        splits_counter = 0
        backtracks_counter = 0
        tautologies = 0
        uc_simplified_counter = 0 #unit clauses simplified on average
        split_simplified_counter = 0

        start = time.time()
        solution = main(clauses)
        runtime = time.time() - start

        if solution:
            total_time += runtime
            times.append(runtime)
        else:
            print("no solution for game :", games.index(game))

    # print("solved", len(times), " games on average time:", numpy.mean(times))
    print("solved", len(times), " puzzle out of ", len(games),
          " games on average time:", numpy.mean(times), " with a std of ", numpy.std(times))
