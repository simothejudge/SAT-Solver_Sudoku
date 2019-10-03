from __future__ import print_function,division
import matplotlib.pylab as plt
import numpy as np
global max_lenght
global min_lenght


def get_sudokus(location):
    sudokus = []
    for l in location:
        with open(l) as file:
            s = file.read()
            sudokus += s.split('\n')
    sud_list = []
    lenghts = []
    for sudoku in sudokus:
        smoothness = get_smoothness(sudoku)
    max_lenght = max(lenghts)
    min_lenght = min(lenghts)
    print ("Number of sudokus: ", len(sudokus))
    del sudokus
    print ("max lenght: ", max_lenght)
    print ("min lenght: ",min_lenght)
    return 1


def get_count(sud):
    # count the occurrencies
    counter = {1: 0,2: 0,3: 0,4: 0,5: 0,6: 0,7: 0,8: 0,9: 0}
    for num in sud:
        if num in counter:
            counter[num] += 1
        else:
            counter[num] = 1
    return counter, len(sud)

def get_distance(avg, occurrancies):
    # count the distance from the average occurrence
    counter = {1: 0,2: 0,3: 0,4: 0,5: 0,6: 0,7: 0,8: 0,9: 0}
    for x, occ in enumerate(occurrancies):
        counter[x+1] = abs(avg - occ)
    return counter


def get_smoothness(sudoku):
    #get a list of variables as partial initial solution of the puzzle
    #returns the average occurrence of clues, the std, and the distance from the average for every number
    numbers = np.array([int(str(x)[len(str(x))-1]) for x in sudoku])
    count,lenght = get_count (numbers)
    print (count,lenght)
    #sud_list.append (numbers)
    #lenghts.append (len (numbers))
    plt.plot(*zip(*sorted(count.items())))
    plt.show()
    occurrances = np.array([int(x) for x in count.values()])
    average_smooth = np.average(occurrances)
    std_smooth = np.std(occurrances)
    distances = get_distance(average_smooth, occurrances)
    print("average ", average_smooth, " stand dev: ", std_smooth)
    print(occurrances)
    print (distances)
    return average_smooth, std_smooth, distances


# location = ["TXT/sudoku_examples/Easy.txt",
#            "TXT/sudoku_examples/Intermediate.txt",
#            "TXT/sudoku_examples/Hard.txt", ]

#sudoku = [168, 175, 225, 231, 318, 419, 444, 465, 493, 689, 692, 727, 732, 828, 886, 956, 961, 973]

#get_smoothness(sudoku)
