import random


# counts each occurring variable for one
def existence_counter(clauses):
    return dict((abs(literal), 1)
                for clause in clauses
                for literal in clause)


# counts how many times each variable(either positive or negative) occurs in clauses
def occurrences_counter(clauses):
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
def positive_negative_counter(clauses):
    count = {}
    for clause in clauses:
        for literal in clause:
            if literal not in count:
                count[literal] = 1
            else:
                count[literal] += 1
    return count


# counts literals based on the weights of clauses. Larger the clause, less weight for the literal.
def weighted_counter(clauses):
    sum = {}
    for clause in clauses:
        length_of_clause = len(clause)
        for literal in clause:
            if literal not in sum:
                sum[literal] = 2 ** (-length_of_clause)
    return sum


# TODO: function MOM needs to be checked, and try to call it
def mom_counter(clauses):
    k = 1  # parameter to be set
    shortest_len = len(min(clauses, key=len))
    shortest_clauses = [c for c in clauses if len(c) == shortest_len]
    PNcounter = occurrences_counter(shortest_clauses)
    MomValue = {}
    for lit in PNcounter.keys():
        positive_count = PNcounter.get(lit, 0)
        negative_count = PNcounter.get(-lit, 0)
        MomValue[lit] = (positive_count + negative_count) * 2 ** k + (positive_count * negative_count)
    return MomValue


def weight_literals(clauses, method="random"):
    if method is "DLCS":
        return occurrences_counter(clauses)
    elif method is "DLIS":
        return positive_negative_counter(clauses)
    elif method is "JW":
        return weighted_counter(clauses)
    elif method is "MOM":
        return mom_counter(clauses)
    else:
        return existence_counter(clauses)


# returns a random literal from clauses based on heuristic method provided for splitting purposes
# heuristic method just decide how to weight the literals. After weighting literals rest of the process is the same.
# We randomly select from the literals with the highest weight.
def get_split_literal(clauses, heuristic_method="random"):
    literal_weights = weight_literals(clauses, heuristic_method)
    max_weight = max(literal_weights.values())
    return random.choice([x for x in literal_weights.keys() if literal_weights[x] == max_weight])
