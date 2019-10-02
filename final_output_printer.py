import DIMACS_reader


def input_file():
    filename = "a"

    return filename;


def truth_table(clauses, solution):
    truthtable = dict()
    if not solution:
        return None
    for clause in clauses:
        for literal in clause:
            truthtable[abs(literal)] = abs(literal) in solution
    return truthtable


def output_printer(clauses, solution, output_file_name):
    truthtable = truth_table(clauses, solution)

    with open(output_file_name + '.out', "w") as file:
        if truthtable:
            for i in truthtable:
                if truthtable[i]:
                    file.write(str(i) + " 0\n")
                else:
                    file.write(str(-i) + " 0\n")
    file.close()
