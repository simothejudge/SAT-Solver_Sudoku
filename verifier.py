import math

from sympy import flatten


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


# checks if given sudoku solution is correct
def verify_sudoku(solution):
    matrix = print_sudoku(solution)
    size = len(matrix)
    for i in range(size - 1):
        count = [0] * size
        for index in matrix[i][:]:
            count[index - 1] = count[index - 1] + 1

        if not filter(lambda item: item != 1, count):
            print("invalid solution for row: ", i)
            return

        count = [0] * size
        for index in matrix[:][i]:
            count[index - 1] = count[index - 1] + 1

        if not filter(lambda item: item != 1, count):
            print("invalid solution for column: ", i)
            return

        count = [0] * size
        block_size = int(size ** (1 / 2))
        for index in flatten(matrix[int(i / block_size):int(i / block_size) + block_size - 1][
                             (i % block_size): (i % block_size) + block_size - 1]):
            count[index - 1] = count[index - 1] + 1

        if not filter(lambda item: item != 1, count):
            print("invalid solution for block: ", int(i / block_size), i % block_size)
            return
    print("Solution is correct")


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
