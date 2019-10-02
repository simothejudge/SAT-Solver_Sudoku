""" IMPORTANT: There shouldn't be two different functions or classes for solver.
    Sat solver should be able to solve all types of sat problems without defining
    the type of it, including SUDOKUS.
    We can remove this class and sat_solver class.
"""

import sys

import numpy

import DIMACS_reader
import heuristics
import sat_solver
import verifier

# 4x4
# sudokus_file = "TXT/4x4.txt"
# location_rules = "sudoku-rules-4x4.txt"

# 9x9
# sudokus_file = "TXT/3sudoku"
# sudokus_file = "TXT/ForHeurCheck.txt"

sudoku_partial_solutions = "TXT/1000 sudokus.txt"
# RANDOM: average time: 2.6395707511901856  with a std of  2.2275945704814886
#

# location_rules = "TXT/satproblem"
sudoku_rules = "sudoku-rules.txt"


# 16x16
# sudokus_file = "TXT/16x16.txt"
# location_rules = "sudoku-rules-16x16.txt"


def solve_sudokus(sudoku_rules, partial_games, method):
    rules, size = DIMACS_reader.get_rules(sudoku_rules)
    games = DIMACS_reader.transform(partial_games)

    total_time = 0
    times = []
    for game in games:
        clauses = DIMACS_reader.get_clauses(game, rules)
        solution, stats = sat_solver.solve_sat(clauses, heuristics.get_random_literal_method(method))

        if solution:
            time = stats["time"]
            total_time += time
            times.append(time)
            if verifier.verify(solution, clauses):
                print("solution found for game", games.index(game), "in", time, "seconds.\n",
                      "solution is: ", sorted(solution), "\n stats:", stats)
            else:
                print("solution for game", games.index(game), "is wrong: \n", sorted(solution))

        else:
            print("no solution found for game", games.index(game))

    print("solved", len(times), "puzzle out of", len(games),
          " games on average", numpy.mean(times), "seconds with a std of", numpy.std(times))


def method():
    return "DLCS"
    # return "DLIS"
    # return "JW"
    # return "MOM"
    # return "random"


if __name__ == '__main__':
    args = sys.argv()
    if args:
        rules = args[0]
        partial_solutions = args[1]
        method = args[2]
    else:
        rules = sudoku_rules
        partial_solutions = sudoku_partial_solutions
        method = method()

    solve_sudokus(rules, partial_solutions, method)
