import random


# counts each occurring variable for one
def __existence_counter(clauses):
    return dict((abs(literal), 1)
                for clause in clauses
                for literal in clause)


# counts how many times each variable(either positive or negative) occurs in clauses
def __occurrences_counter(clauses):
    count = {}
    for clause in clauses:
        for literal in clause:
            literal = abs(literal)
            if literal not in count:
                count[literal] = 1
            else:
                count[literal] += 1
    return count


# counts how many times each literal(positive and negative values separately) occurs in clauses
def __positive_negative_counter(clauses):
    count = {}
    for clause in clauses:
        for literal in clause:
            if literal not in count:
                count[literal] = 1
            else:
                count[literal] += 1
    return count


# counts literals based on the weights of clauses. Larger the clause, less weight for the literal.
def __weighted_counter(clauses):
    sum = {}
    for clause in clauses:
        length_of_clause = len(clause)
        for literal in clause:
            if literal not in sum:
                sum[literal] = 2 ** (-length_of_clause)
    return sum


# TODO: function MOM needs to be checked, and try to call it
def __mom_counter(clauses):
    k = 1  # parameter to be set
    shortest_len = min(clauses, key=len)
    shortest_clauses = [c for c in clauses if len(clauses) == shortest_len]
    PNcounter = __positive_negative_counter(shortest_clauses)
    MomValue = {}
    for lit in PNcounter.keys():
        function = (PNcounter[lit] + PNcounter[-lit]) * 2 ** k + (PNcounter[lit] * PNcounter[-lit])
        MomValue[lit] = function
    return MomValue


def __count_literals(clauses, method="random"):
    if method is "DLCS":
        return __occurrences_counter(clauses)
    elif method is "DLIS":
        return __positive_negative_counter(clauses)
    elif method is "JW":
        return __weighted_counter(clauses)
    elif method is "MOM":
        return __mom_counter(clauses)
    else:
        return __existence_counter(clauses)


def __get_random_literal(clauses, counter_method="random"):
    counter = __count_literals(clauses, counter_method)
    max_freq = max(counter.values())
    return random.choice([x for x in counter.keys() if counter[x] == max_freq])


def get_random_literal_method(method="random"):
    return lambda c: __get_random_literal(c, method)
