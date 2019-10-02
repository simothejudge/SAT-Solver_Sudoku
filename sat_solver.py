import sys
import time

import DIMACS_reader
import heuristics
import verifier

stats = {"bcp": 0, "unit": 0, "depth": 0, "split": 0, "recursive_call": 0, "time": 0.0}
heuristics_methods = {"-S1": "random", "-S2": "DLCS", "-S3": "DLIS", "-S4": "JW", "-S5": "MOM"}

def is_tautology(clause):
    for literal in clause:
        if -literal in clause:
            return True
    return False


def remove_tautologies(clauses):
    # return list((clause for clause in clauses if not is_clause_tautology(clause)))
    return list(filter(lambda clause: not is_tautology(clause), clauses))


def bcp(clauses, literal):
    stats["bcp"] += 1
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
    stats["unit"] += 1
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


def sat_solver(clauses, literals, heuristic_method, level):
    stats["recursive_call"] += 1
    if clauses is None:
        return None

    if level > stats["depth"]:
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
    stats["split"] += 1
    solution = sat_solver(bcp(clauses, literal), literals.copy(), heuristic_method, level + 1)
    if solution is None:
        literals[abs(literal)] = literal < 0
        solution = sat_solver(bcp(clauses, -literal), literals, heuristic_method, level + 1)

    return solution


def solve_sat(clauses, heuristic_method):
    start = time.time()
    # check for tautologies just once at the beginning
    clauses = remove_tautologies(clauses)

    # call the solver
    solution = sat_solver(clauses, {}, heuristic_method, 0)
    stats["time"] = time.time() - start

    return sorted([x for x in solution.keys() if solution[x] is True]), stats


if __name__ == '__main__':
    # SAT -Sn inputfile

    method = sys.argv[1]
    inputfile = sys.argv[2]

    clauses, size = DIMACS_reader.get_rules(inputfile)
    solution, stats = solve_sat(clauses, heuristics_methods[method])

    if solution:
        if verifier.verify(solution, clauses):
            print("solution found in", stats["time"], "\n", "solution is:", sorted(solution))
        else:
            print("solution for file", inputfile, "is wrong: \n", sorted(solution))
    else:
        print("no solution found for input", inputfile, "with heuristic method", method)
