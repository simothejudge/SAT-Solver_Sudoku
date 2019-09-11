"""
What functions we need?
    check

"""
import DIMACS_reader

location_sudoku = "sudoku-example (1).txt"
location_rules = "sudoku-rules.txt"


"""
def DP_solver(clauses, literals):
    if clauses :

    else
        return


def UnitPropagate(clauses, literals):
    while # clauses is not empty && clauses has a unit clause :
        do:


"""

def main():
    clauses = DIMACS_reader.load_file(location_sudoku, location_rules)


if __name__ == '__main__':
    main()
