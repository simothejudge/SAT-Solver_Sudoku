import numpy

import DIMACS_reader

global max_lenght
global min_lenght


def get_sudokus(location):
    sudokus = DIMACS_reader.get_games(location)
    return [get_smoothness(sudoku) for sudoku in sudokus]


def get_count(sud):
    # count the occurrencies
    counter = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    for num in sud:
        counter[num] += 1
    return counter, len(sud)


def get_smoothness(sudoku):
    # get a list of variables as partial initial solution of the puzzle
    # returns the average occurrence of clues, the std, and the distance from the average for every number
    numbers = [literal[0] % 10 for literal in sudoku]
    count, lenght = get_count(numbers)
    return numpy.std(list(count.values()))
