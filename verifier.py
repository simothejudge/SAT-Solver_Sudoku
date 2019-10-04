import math

# checks if given solution satisfies all clauses
def verify(solution, clauses):
    for clause in clauses:
        satisfied = False
        for literal in clause:
            if literal > 0:
                if literal in solution:
                    satisfied = True
                    continue
            if literal < 0:
                if -literal not in solution:
                    satisfied = True
                    continue
        if not satisfied:
            print("solution doesn't satisfies clause: ", clause)
            return False
    return True

# prints given sudoku solution in 9x9 human readable matrix
def print_sudoku(solution):
    counter = 0
    for i in solution:
        if solution[i] is True:
            counter += 1
    size = int(math.sqrt(counter))

    if size < 10:
        base = 10
    else:
        base = 17

    matrix = [[0] * size] * size
    for key, value in solution.items():
        if key > 0 and value:
            matrix[int((key / base ** 2)) - 1][int(key / base) % base - 1] = key % base

    print('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in matrix]))
    return matrix
