from __future__ import print_function,division
import DIMACS_reader



def get_sudokus(location):
    sudokus = []
    for l in location:
        with open(l) as file:
            s = file.read ()
            sudokus += s.split ('\n')

    print (sudokus)
    # for sudoku in sudokus:
    return 1

location = ["TXT/1000 sudokus.txt", "TXT/top91.sdk.txt", "TXT/damnhard.sdk.txt", "TXT/top95.sdk.txt", "TXT/top100.sdk.txt"]

get_sudokus(location)