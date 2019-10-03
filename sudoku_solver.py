import numpy

import DIMACS_reader
import final_output_printer
import heuristics
import sat_solver
import verifier

# 4x4
# sudoku_games = "TXT/sudoku_examples/4x4.txt"
# sudoku_games = "TXT/sudoku_examples/3sudoku"
# sudoku_games = "TXT/sudoku_examples/ForHeurCheck.txt"
sudoku_games = "TXT/sudoku_examples/1000 sudokus.txt"  # RANDOM: average time: 2.639570 with a std of  2.227594

sudoku_rules = {4: "TXT/sudoku_rules/sudoku-rules-4x4.txt",
                9: "TXT/sudoku_rules/sudoku-rules.txt",
                16: "TXT/sudoku_rules/sudoku-rules-16x16.txt"}


# This file reads sudoku rules and partial solutions from different files and create one list of clauses and uses
# sat_solver to solve the sudoku. If there are more than one sudoku provided in partial_games file it solves all of them
# and calculates mean/std time for all solutions.
def solve_sudokus(sudoku_rules, partial_games, method):
    rules, size = DIMACS_reader.get_rules(sudoku_rules[9])
    games = DIMACS_reader.transform(partial_games)

    times = []
    all_stats = []
    print("using heuristic method: ", method)
    for game in games:
        print("solving sudoku ", games.index(game), "/", len(games))
        clauses = DIMACS_reader.get_clauses(game, rules)
        solution, stats = sat_solver.solve_sat(clauses, method)
        if solution:
            if verifier.verify(solution, clauses):
                times.append(stats["time"])
                # print("solution found for game", games.index(game), "in", stats["time"], "seconds.\n",
                #       "solution is: ", sorted(solution), "\n stats:", stats)
            # else:
            # print("solution for game", games.index(game), "is wrong: \n", sorted(solution))

        else:
            stats["solution"] = False
            # print("no solution found for game", games.index(game))
        all_stats.append(stats.copy())
    return all_stats
    # print("solved", len(times), "sudokus out of", len(games),
    #       " sudokus on average", numpy.mean(times), "seconds with a std of", numpy.std(times))


def method():
    return "DLCS"
    # return "DLIS"
    # return "JW"
    # return "MOM"
    # return "random"


if __name__ == '__main__':
    rules = sudoku_rules
    games = sudoku_games

    stats = {}
    for method in ["random", "DLCS", "DLIS", "JW", "MOM"]:
        stats = solve_sudokus(rules, games, method)
        final_output_printer.print_stats(sudoku_games + "_" + method + ".out", stats)
