from __future__ import print_function,division
import DIMACS_reader

global max_lenght


def get_sudokus(location):
    sudokus = []
    for l in location:
        with open(l) as file:
            s = file.read()
            sudokus += s.split('\n')


    sud_list=[]
    lenghts = []
    for sudoku in sudokus:
        numbers = [int(x) for x in sudoku if x.isdigit() ]
        count, lenght = get_count(numbers)
        print(count, lenght)
        sud_list.append(numbers)
        lenghts.append(len(numbers))
    max_lenght = max(lenghts)
    del sudokus
    print ("max lenght: "+max_lenght)
    return 1


def get_count(sud):

    counter = {1: 0,2: 0,3: 0,4: 0,5: 0,6: 0,7: 0,8: 0,9: 0}
    for num in sud:
        if num in counter:
            counter[num] += 1
        else:
            counter[num] = 1
    return counter, len(sud)

def group_lenght ():
    location = ["TXT/top2365.sdk.txt",
                "TXT/1000 sudokus.txt",
                "TXT/top91.sdk.txt",
                "TXT/damnhard.sdk.txt",
                "TXT/top95.sdk.txt",
                "TXT/top100.sdk.txt"]

    get_sudokus(location)
