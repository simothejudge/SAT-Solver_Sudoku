# Sudoku-Project

Similar work: https://github.com/marcmelis/dpll-sat/blob/master/solvers/original_dpll.py

**DP_Solver.py**

    main()
    
    unit_propagation(clauses)
        
    Split(clauses, literals)
    
    bcp(clauses, literals)
    
    is_tautology(clause)
    
    remove_tautologies(clauses)
    
    DP_solver()
    
    verify_solution()
    
    print_solution()
    
**DIMACS_reader.py**
    
    get_rules()
    
    get_game()
    
    get_clauses()
    
    get_list()
    
    load()
    
    tranform()
    
    transformline()
    
    translate()

**Heuristics.py**

Splitting Optimization --> Variable Selection
- Dynamic Largest Combined Sum: (most frequent)
    pos = occourrencies of lit
    neg = occourrencies of lit'
    pick lit: max{pos+neg} --> max{occourrencies}
    
    needed: to count general occourrencies of each literal in the clauses list
    
- Dynamic Largest Individual Sum: (most frequent in pos or negs)
    pos = occourrencies of lit
    neg = occourrencies of lit'
    pick lit: max{pos or neg}
    
    needed count pos and negs, take the highest number, 
        if pos>negs --> lit == True 
        else --> lit == False
        
- Jeroslow-Wang:
    lamda = number of literals in a clause containing lit
    for every lit J(lit) = sum(2^(-|lamda|))
    pick lit: max{J(lit)} OR 
                max {J(lit)+J(lit')} and set lit = True if J(lit)>J(lit')
                
- Maximum Occourrencies in Clauses of Minimum Size: MOM
    preference is given to literlas with: 
        large number of occourrencies
        lit in small clauses
     get all the smallest clauses 
    among them, f°(x) = count the occourrencies of lit 
    pick x: max{ [f°(x)+f°(x')]*2^k + f°(x)*f°(x') }
 
  
****HYPOTHESIS:**** 
- hard sudokus for people are also hard for computer (based on the process time)
- difficulty and size relationship? quadratically, exponential, log?
- how much the scheme of clues given affect the sudokus resolution? Is a more spread solution 


IDEA: for every sudoku played, we get the number of values given at first, the actual values, 
the "hardness" (how to define it? splitting and backtracking and process time), 
get the smooth/jumpy distributiuon of initial values (maybe establishing an evaluation for smoothness, 
like no more than 3 appearances of the value for 25 lenght clues) and we see if there is a correlation

    