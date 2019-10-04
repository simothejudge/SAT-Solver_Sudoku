import numpy

import DIMACS_reader
import final_output_printer
import sat_solver
import smoothness
import verifier

# 4x4
# sudoku_games = "TXT/sudoku_examples/4x4.txt"
# sudoku_games = "TXT/sudoku_examples/3sudoku"
# sudoku_games = "TXT/sudoku_examples/top100.sdk.txt"
# sudoku_games = "TXT/sudoku_examples/1000 sudokus.txt"  # RANDOM: average time: 2.639570 with a std of  2.227594
sudoku_files = ["TXT/sudoku_examples/ForHeurCheck.txt",
                "TXT/sudoku_examples/1000 sudokus.txt",
                "TXT/sudoku_examples/Easy.txt",
                "TXT/sudoku_examples/Intermediate.txt",
                "TXT/sudoku_examples/Hard.txt"]


sudoku_rules = {4: "TXT/sudoku_rules/sudoku-rules-4x4.txt",
                9: "TXT/sudoku_rules/sudoku-rules.txt",
                16: "TXT/sudoku_rules/sudoku-rules-16x16.txt"}


# This file reads sudoku rules and partial solutions from different files and create one list of clauses and uses
# sat_solver to solve the sudoku. If there are more than one sudoku provided in partial_games file it solves all of them
# and calculates mean/std time for all solutions.
def solve_sudokus(sudoku_rules, partial_games, method):
    rules, size = DIMACS_reader.get_rules(sudoku_rules[9])
    sudokus = DIMACS_reader.get_games(partial_games)

    times = []
    all_stats = []
    print("using heuristic method: ", method)
    for sudoku in sudokus:
        clauses = sudoku + rules
        solution, stats = sat_solver.solve_sat(clauses, method)
        solution = sorted([x for x in solution.keys() if solution[x] is True])
        stats["smoothness"] = smoothness.get_smoothness(sudoku)
        if solution:
            if verifier.verify(solution, clauses):
                times.append(stats["time"])
                print("solution found for sudoku", sudokus.index(sudoku), "in", stats["time"], "seconds.\n",
                      "solution is: ", solution, "\n stats:", stats)
            else:
                print("solution for sudoku", sudokus.index(sudoku), "is wrong: \n", solution)
        else:
            stats["solution"] = False
            print("no solution found for sudoku", sudokus.index(sudoku))
        all_stats.append(stats.copy())
    print(len(times), "/", len(sudokus), "solved on average", numpy.mean(times), "seconds with a std of",
          numpy.std(times))
    return all_stats


if __name__ == '__main__':
    rules = sudoku_rules
    files = sudoku_files[3:4]

    stats = {}
    for file in files:
        for method in ["MOM"]:
            stats = solve_sudokus(rules, file, method)
            final_output_printer.print_stats(file + "1_" + method + ".out", stats)
