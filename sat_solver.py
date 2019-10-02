import sys
import time

import DIMACS_reader
import heuristics
import verifier


# TODO: Experiments and Statistics

def is_tautology(clause):
    for literal in clause:
        if -literal in clause:
            return True
    return False


def remove_tautologies(clauses):
    # return list((clause for clause in clauses if not is_clause_tautology(clause)))
    return list(filter(lambda clause: not is_tautology(clause), clauses))


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


def sat_solver(clauses, literals, get_random_literal):
    if clauses is None:
        return None

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
    literal = get_random_literal(clauses)

    literals[abs(literal)] = literal > 0
    solution = sat_solver(bcp(clauses, literal), literals, get_random_literal)
    if solution is None:
        literals[abs(literal)] = literal < 0
        solution = sat_solver(bcp(clauses, -literal), literals, get_random_literal)

    return solution


def solve_sat(clauses, method_to_get_random_literal):
    start = time.time()
    # check for tautologies just once at the beginning
    clauses = remove_tautologies(clauses)

    # call the solver
    solution = sat_solver(clauses, {}, method_to_get_random_literal)
    runtime = time.time() - start

    return sorted([x for x in solution.keys() if solution[x] is True]), runtime


if __name__ == '__main__':
    # SAT -Sn inputfile
    args = sys.argv()
    method = args[0]
    inputfile = args[1]

    clauses, size = DIMACS_reader.get_rules(inputfile)
    solution, time = solve_sat(clauses, heuristics.get_random_literal_method(method))

    if solution:
        if verifier.verify(solution, clauses):
            print("solution found in", time, "\n", "solution is:", sorted(solution))
        else:
            print("solution for file", inputfile, "is wrong: \n", sorted(solution))
    else:
        print("no solution found for input", inputfile, "with heuristic method", method)
