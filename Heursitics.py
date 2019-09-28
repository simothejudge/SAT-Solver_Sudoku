# functions are called from Split(), receiving the clauses and making calculations out of it and give back the literal and its value

# First Heuristic:

def OccurenciesCounter(clauses):
    count = {}
    for clause in clauses:
        for lit in clause:
            lit = abs(lit)
            if lit not in count.keys():
                count[lit] = 1
            else:
                count[lit] += 1
    return count

def PosNegCounter(clauses):
    #the count dictionary containes for each literal both the occourrences of lit and the occourrencies of lit'
    #depending on the sign of the returned literal the split will set pos or neg
    count = {}
    for clause in clauses:
        for lit in clause:
            if lit not in count.keys():
                count[lit] = 1
            else:
                count[lit] += 1
    return count

def weightedCounter(clauses):
    sum = {}
    for clause in clauses:
        lamda = len(clause)
        for lit in clause:
            JValue = 2**(-abs(lamda))
            if lit not in sum.keys():
                sum[lit] = JValue
    return sum

#TODO: process time for each sudoku too long, how come?
"""
def DLCS(clauses):
    counter = OccurenciesCounter(clauses)
    max_freq = max(counter.values())
    return [x for x in counter.keys() if counter[x] == max_freq]
"""

def DLCS(clauses):
    counter = OccurenciesCounter(clauses)
    max_freq = max(counter.values())
    return [x for x in counter.keys() if counter[x] == max_freq]


def DLIS(clauses):
    counter = PosNegCounter(clauses)
    max_freq = max(counter.values())
    return [x for x in counter.keys() if counter[x] == max_freq]


def JW(clauses):
    weighted_counter = weightedCounter(clauses)
    max_freq = max (weighted_counter.values())
    return [x for x in weighted_counter.keys () if weighted_counter[x] == max_freq]

#TODO: function MOM needs to be checked, and try to call it
def MOM(clauses):
    k = 1 #parameter to be set
    shortest_len = min(clauses, key=len)
    shortest_clauses = [c for c in clauses if len(clauses) == shortest_len]
    PNcounter = PosNegCounter(shortest_clauses)
    MomValue = {}
    for lit in PNcounter.keys():
        function = (PNcounter[lit]+PNcounter[-lit])*2**k + (PNcounter[lit] * PNcounter[-lit])
        MomValue[lit] = function
    max_value = max(MomValue.values())
    return [x for x in MomValue.keys () if MomValue[x] == max_value]

