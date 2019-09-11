# Sudoku-Project

Similar work: https://github.com/marcmelis/dpll-sat/blob/master/solvers/original_dpll.py

Reader loads 2 files : 
The sudoku initial puzzle (partial solution) in DIMACS → first elements of our constraints, all unit clauses
The sudoku rules in DIMACS

Variables: 
List of variables, with boolean values (T, F, unknown) VAR
List of constraint clauses CLAUSES

Tautology checking → only once at the beginning (outside the recursive algorithm)

DP function(VAR, CLAUSES): 

	SIMPLIFY:
	Check for unit clauses in CLAUSES
		Update CLAUSES, VAR
	Check for pure literal in CLAUSES
		Update CLAUSES, VAR
	
	SPLIT:
	First try: random assignment to VAR (then two heuristics..)
		Update CLAUSES
		If sat → recurse
		Else: backtrack
