import numpy

import DIMACS_reader

global max_lenght
global min_lenght


def get_sudokus(location):
    sudokus = DIMACS_reader.get_games(location)
    # sud_list = []
    # lenghts = []
    # for sudoku in sudokus:
    #     numbers = [int(str(x)[2]) for x in sudoku]
    #     count, lenght = get_count(numbers)
    #     print(lenght)
    #     sud_list.append(numbers)
    #     lenghts.append(len(numbers))
    # max_lenght = max(lenghts)
    # min_lenght = min(lenghts)

    return [get_smoothness(sudoku) for sudoku in sudokus]


def get_count(sud):
    # count the occurrencies
    counter = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    for num in sud:
        counter[num] += 1
    return counter, len(sud)


# def get_distance(avg, occurrancies):
#     # count the distance from the average occurrence
#     counter = {1: 0,2: 0,3: 0,4: 0,5: 0,6: 0,7: 0,8: 0,9: 0}
#     for x, occ in enumerate(occurrancies):
#         counter[x+1] = abs(avg - occ)
#     return counter
#

def get_smoothness(sudoku):
    # get a list of variables as partial initial solution of the puzzle
    # returns the average occurrence of clues, the std, and the distance from the average for every number

    numbers = [literal[0] % 10 for literal in sudoku]
    count, lenght = get_count(numbers)
    return numpy.std(list(count.values()))

# location = "TXT/sudoku_examples/Hard.txt"
# var = get_sudokus(location)
#
# print()
