

#implementing DLCS and DLIS
# functions are called from Split(), receiving the clauses and making calculations out of it and give back the literal and its value

# First Heuristic:

def OccurenciesCounter(clauses):
    count = {}
    for clause in clauses:
        for lit in clause:
            if abs(lit) not in count.keys():
                count[abs(lit)] = 1
            else:
                count[abs(lit)] += 1
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


def DLCS(clauses):
    counter = OccurenciesCounter(clauses)
    return max(counter, key = counter.get)

def DLIS(clauses):
    counter = PosNegCounter(clauses)
    value = max(counter, key = counter.get)
    print(value)
    return values

"""
def main():


if __name__ == '__main__':
    main()
"""
