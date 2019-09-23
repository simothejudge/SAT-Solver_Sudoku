

#implementing DLCS and DLIS
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
            else:
                sum[lit] += JValue
    return sum


def DLCS(clauses):
    counter = OccurenciesCounter(clauses)
    max_freq = max(counter.values())
    return [x for x in counter.keys() if counter[x] == max_freq]

def DLIS(clauses):
    counter = PosNegCounter(clauses)
    max_freq = max (counter.values ())
    return [x for x in counter.keys () if counter [x] == max_freq]

def JW(clauses):
    weighted_counter = weightedCounter(clauses)
    return max(weighted_counter, key = weighted_counter.get)

def MOM(clauses):
    k = 1 #parameter to be set
    shortest_clauses = min(clauses, key = len)
    PNcounter = PosNegCounter(shortest_clauses)
    MomValue = {}
    for lit in PNcounter.keys():
        function = (PNcounter[lit]+PNcounter[-lit])*2**k + (PNcounter[lit] * PNcounter[-lit])
        MomValue[lit] = function
    return max(MomValue, key = MomValue.get)


"""
def main():


if __name__ == '__main__':
    main()
"""
