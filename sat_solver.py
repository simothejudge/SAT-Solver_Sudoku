import sys
import time

import DIMACS_reader
import final_output_printer
import heuristics
import verifier

stats = {"bcp": 0, "unit": 0, "depth": 0, "split": 0, "recursive_call": 0, "time": 0.0}
heuristics_methods = {"-S1": "random", "-S2": "JW", "-S3": "MOM"}


def is_tautology(clause):
    for literal in clause:
        if -literal in clause:
            return True
    return False


def remove_tautologies(clauses):
    return [clause for clause in clauses if not is_tautology(clause)]


def bcp(clauses, literal):
    stats["bcp"] = stats.get("bcp", 0) + 1
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
    stats["unit"] = stats.get("unit", 0) + 1
    literals = {}
    # filter clauses if length of clause is 1
    unit_literals = [clause[0] for clause in clauses if len(clause) == 1]

    # for every unit in the list of unit_literals we simplify the clauses and set literals to true
    for literal in unit_literals:
        # contradiction check
        if -literal in unit_literals:
            return None, None

        # call the bcp for unit_literals simplification
        clauses = bcp(clauses, literal)
        if clauses is None:
            return None, None

        # set literal in literals equal to True or False
        literals[abs(literal)] = literal > 0
    return literals, clauses


def sat_solver(clauses, literals, heuristic_method, level):
    stats["recursive_call"] = stats.get("recursive_call", 0) + 1
    if clauses is None:
        return None

    if level > stats.get("depth", -1):
        stats["depth"] = level

    while True:
        unit_literals, clauses = unit_propagation(clauses)

        if clauses is None:
            return None

        if not unit_literals:
            break

        literals.update(unit_literals)

    if not clauses:
        return literals

    # SPLITTING
    literal = heuristics.get_split_literal(clauses, heuristic_method)

    literals[abs(literal)] = literal > 0

    stats["split"] = stats.get("split", 0) + 1
    solution = sat_solver(bcp(clauses, literal), literals.copy(), heuristic_method, level + 1)
    if solution is None:
        literals[abs(literal)] = literal < 0
        solution = sat_solver(bcp(clauses, -literal), literals, heuristic_method, level + 1)

    return solution


def solve_sat(clauses, heuristic_method):
    stats.clear()
    stats.update({"bcp": 0, "unit": 0, "depth": 0, "split": 0, "recursive_call": 0, "time": 0.0})
    start = time.time()
    # check for tautologies just once at the beginning
    clauses = remove_tautologies(clauses)

    # call the solver
    solution = sat_solver(clauses, {}, heuristic_method, 0)
    stats["time"] = time.time() - start

    return solution, stats


if __name__ == '__main__':
    # SAT -Sn inputfile

    method = sys.argv[1]
    inputfile = sys.argv[2]

    clauses, size = DIMACS_reader.get_rules(inputfile)
    solution, stats = solve_sat(clauses, heuristics_methods[method])

    solution = sorted([x for x in solution.keys() if solution[x] is True])
    final_output_printer.output_printer(clauses, solution, inputfile + ".out")
    if solution:
        if verifier.verify(solution, clauses):
            print("solution found for", inputfile, "in", stats["time"], "seconds.\n",
                  "solution is:", solution, "\n stats:", stats)
        else:
            print("solution for", inputfile, "is wrong: \n", solution)
    else:
        print("no solution found for", inputfile, "with heuristic method", method)
