# A SAT Solver for the game of Sudoku

This is the final project for the Knowledge Representation course at the Vrije University of Amsterdam - 2019.

## Instructions

Run on command line `py sat_solver.py -Sn filename`, where n is the heuristic method (1 is random, 2 is JW, 3 is MOM) and filename is the address for the input file for SAT problem encoded in `DIMACS CNF` format.
****

## Introduction
This paper describes the implementation of a Boolean Satisfiability Solver, which is specifically designed to process and solve Sudokus of any size and difficulty. Sudokus are logic-based, combinatorial number-placement puzzles, that can be presented as Constraint Satisfaction Problems (CSP), but we can also encode them as SAT problems: each puzzle is encoded into Conjunctive Normal Form (CNF), where the puzzle rules and the initial clues given are translated into a propositional formula composed by a finite set of variables. Each variable essentially indicates if a specific number is present or not in a specific cell of the sudoku grid; therefore, every variable can assume only `{TRUE, FALSE}` boolean values. An SAT Solver would then provide generic combinational reasoning to find a Satisfying Assignment for the given boolean formula. In our implementation, we followed the procedure of Davis-Putnam-Logemann-Loveland (DPLL). This is a systematic algorithm for complete solution methods, where literals are selected from the propositional input formula and recursively assigned with a boolean value to search for a final satisfying assignment. 
A simple DPLL algorithm is complete, meaning that for every problem given, it will always return either a satisfying assignment of the set of literals, or prove that the problem is unsatisfiable. Some of the limitations of this algorithm are heavy memory usage and the requirement of a long time to explore the whole tree of combinations. To overcome those limitations we used some heuristic methods to improve the performance of our solver. 
Finally, we present the experiment conducted, to test the hypothesis of a possible correlation between the difficulty of sudokus  and the distribution of the values in the initial clues given. 

## Methods

The SAT Solver is implemented in Python 3. First, we started with the variables involved in our problem and how to store and update them. In order to solve a puzzle, the SAT solver needs to be fed with both sudoku rules and the initial givens. Then we need to combine the constraints coming from the initial clues and the ones coming from the game’s rules. The final expression is composed of a sequence of clauses according to the CNF format. In our Solver, we arranged each clause (union of variables) as a list of DIMACS variables, where: (explain that `-111` is `no 1` in `row 1` `column 1`). The expression was then put in a list, where each cell corresponds to a clause, considering that each clause is linked with a disjunction, which means that if every item (clause) in the list is true, the SAT Solver has found a solution for our sudoku puzzle. 

## Solver Design
Our code is split into several *.py files based on the functionality to be able to maintain the codebase easier. The first file is DIMACS_reader which handles reading given input files and converts data into CNF clauses format. The main function of interest is get_rules which gets a filename containing CNF formatted input and converts its content into a list of clauses. get_games works in a similar fashion but its purpose is to read partial sudoku solutions formatted into a “dotted” representation. 

`sat_solver` is the main file where SAT solving  algorithm is implemented. `sat_solver` expects two arguments to run successfully, the first argument defines what kind of heuristic method going to be used and the second argument gives the filename for clauses formatted in `DIMACS CNF` format. It reads files using the `DIMACS_reader` functions. Once we have clauses following pseudo code is executed to find a solution that satisfies all given clauses: 

<img width="303" alt="Screenshot 2023-06-29 at 11 28 32" src="https://github.com/simothejudge/Sudoku-Project/assets/37406249/51ba6808-4a2f-4bcf-be1e-9662a1e1f3a7">

`sat_solver` runs recursively until clauses are empty or a contradiction is found. At first, it calls `unit_propogation` method which removes all clauses from clauses if the clause consists of only one literal, and then calls BCP to remove every clause from clauses if the clause contains a literal or simplify clause if not literal is in the clause. sat_solver continues removing unit literals until no further simplification can be done. After that, it gets a random literal with the help of a heuristics file to assign True/False values which causes a new split in the possible solution tree  and calls itself for the next level.

Heuristics file implements different algorithms to randomly select a literal for splitting. The main idea about heuristic algorithms is they weigh literals on certain criteria and choose one of them randomly having the highest weight. We implemented four different heuristic approaches. DLCS counts a number of literal occurrences in the clauses ignoring if they are positive or negative literal. DLIS counts literals as well but differentiates positive and negative values of literal. JW also takes into account the length of the clause's literals and gives more weight if the clause is shorter. Which tries to create unit literals for further steps. MOM works similarly to JW but it uses a function that can be configured and the importance of shorter clauses can be increased or decreased, based on the value of `k`. For our `sat_solver` we used JW and MOM approaches. Reasoning why we chose these two is explained in detail in the next section. 

`sudoku_solver` is just a helper file for us to easily read sudoku rules and partial sudoku solutions from different files and calls `sat_solver` with the combination of clauses generated from two files to solve the sudoku problem. 

## Heuristics
In the heuristics section, we chose JW and MOM methods as our heuristics  by comparing test data results of 100 different sudokus on different heuristic methods. Table *1.a* shows the data of average numbers of backtracks, unit propagations, boolean constraint propagations (simplification calls), splits, depths of backtrack trees, and time performances.  It is clear on the graph that the random split method gives the best average time performance meanwhile JW heuristic gives the best cost for the other measurements. Since we needed to choose 2 heuristic methods we took the MOM method as it has the best performance on time and costs that comes after a random split and JW heuristic method.

|                 | Backt.      | unit          |bcp          | split       | depth         | time          | 
| :---            |    :----:   |    :----:     |    :----:   | :----:      |    :----:     |   :----:      |
| **Rand**        | 9.56        | 66.93         | 643.16      | 583.86      | 57.65         | 349.47        |
| **DLCS**        | 251.27      | 1,377.4       | 6,823.6     | 6,064.4     | 1,290.3       | 4,168.9       |
| **DLIS**        | 237.95      | 4.59          | 125.53      | 122.30      | 3.81          | 54.36         |
| **JW**          | 7.41        | 2.67          | 17.11       | 28.23       | 2.76          | 11.93         |
| **MOM**         | 108.98      | 0.82          | 1.80        | 1.74        | 1.03          | 1.38          |

In our experimentation, we observed that heuristics do not perform better than random selection on sudoku problems. However, in general SAT problems, heuristic approaches outperform random selection. We ensured this by processing a generic SAT problem with more variables and more unique constraints than normal sudoku ones.


## Experiment Hypothesis
In solving sudokus manually, people are always wondering how to rate a given puzzle and what factors influence the complexity of the game. After some research, we came to the conclusion that there are different rating systems to evaluate hardness and that they are not based only on one single factor, but they take into account different sudokus characteristics. In particular, we investigated the characteristics of the initial clues: firstly, we found out that the minimum number of clues a sudoku with a unique solution can have is 17, while the maximum is 40. Additionally, we discovered that sudokus are generally symmetrical in the distribution of givens on the grid; but this is a purely aesthetic factor, there is no logic behind it. Furthermore, we noticed that there is actually some evidence of a positive correlation between the number of givens and hardness. Usually, “many initial clues” would translate into “easier” sudokus for people; this is a general trend but it would be wrong to rate difficulty only based on the number of givens, as it is more related to the difficulty of the techniques that a given puzzle will require during the solving process. Of course, we can’t get rid of subjectivity here, as some techniques are harder than others only for certain people, and for others, it might be the exact opposite. What captured our attention regarding this, was that we couldn’t understand how and if hardness was related in any way to the specific values given as initial clues. We know that in the initial grid not every number from 1 to 9 needs to be present, but certainly at least 8 of those numbers do need to be there; for example, if two numbers are not in the initial clues, those two values are basically interchangeable on the board, and this would lead us having a sudoku with more than one solution. Keeping this in mind, we wondered if a different “distribution” of values in the initial clues would be better for a human to solve the sudoku or not; when we first start solving a puzzle, the first thing that we usually look at is the clue with the highest occurrence, so that we can try to find all the nine positions for that number. This would leave us with not much more information about the relative positions of the other numbers of course, but we would also have fewer empty cells to fill. So we wondered if having clues with high occurrences actually makes the sudoku easier or not, and if there was any kind of correlation between the two factors. For humans, we were not able to come to a relevant conclusion, because it depends on the strategy that one finds the easiest for him/her. What about an automatic solver? Is there a correlation between each clue occurrence and the puzzle's difficulty?

## Experiment Design
In designing our experiment we faced two big questions: 
**How to define difficulty for our SAT Solver?**
**How to evaluate the “smoothness” of occurrences of each sudoku?**
We considered a total of 150 sudokus, grouping them into three sets of 50 based on the human-perceived difficulty (Hard, Intermediate, Easy). For this purpose we used an online sudoku grader, that would rate the puzzle considering the strategies that a human would need to follow to solve it manually. Since we cannot make the assumption that hard-for-human sudokus are also hard-for-machine, we repeated the experiment also considering the whole 150 sudokus at once. The sudokus were processed and solved by our SAT Solver, using the JW Heuristic, which had shown the best performance results with respect to the other variable selection methods. To capture the concept of hardness without losing the relevant information of the number of initial clues, we built a “Hardness Index”, combining for each sudoku the processing time, the number of splits, and the number of initial givens. The hardness formula came out to be: 
<img width="228" alt="Screenshot 2023-06-29 at 11 46 51" src="https://github.com/simothejudge/Sudoku-Project/assets/37406249/6688e5cb-985e-4688-81b9-b0cf8af3f1c3">

Where we first normalized the variables’ values through the unity-based normalization (Min-Max Feature Scaling), and then we assigned each variable its proper weight. 
When talking about smoothness, we refer to how clues are distributed in the value range [1-9]. For example, given 27-clue sudoku, “smooth” distribution of clues is considered to be:
 `{1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6,7,7,7,8,8,8,9,9,9}`
while a “non-smooth” distribution (considering the constraint of uniqueness) would be:
`{1,1,1,1,1,2,2,3,3,3,5,5,5,5,5,6,7,7,8,8,8,9,9,9,9,9,9}`
As we can notice, in the second set of clues there is one number (4) missing,  more occurrences of fewer numbers, and fewer occurrences of the remaining. We need to keep into account that the number of occurrences for each clue value is strictly related to the total number of clues given for the sudoku; registering “peaks” or occurrences values for each number is not a good idea, because for 17-clue sudoku, the fact that the number 2 appears three times can already be considered as a peak. We decided to assign to each sudoku a smoothness value. Our `smoothness.py` file processed 150 sudokus, registering in a dictionary the initial occurrences of every number from 1 to 9, calculating the average occurrence of a clue in the sudoku, and consequently the standard deviation from that average. The standard deviation found  is a reliable measure for smoothness because it is strictly related to the average value of occurrences for the specific sudoku processed, and basically tells us how much each clue’s occurrence differs from r the average occurrence. In our two examples, the data collected would be: 
`Count 1 = {1:3, 2:3, 3:3, 4.3, 5:3, 6.3, 7:3, 8:3, 9:3}`
`Avg1 = 3 	Std1 = 0`
`Count2 = {1.5, 2:2, 3:3, 4:0, 5:5, 6:1, 7:2, 8:3, 9:6}`
`Avg2 = 2.89	Std2 = 1.83`

## Experiment Results
After collecting the data and calculating the smoothness and the hardness values, we computed a correlation analysis, to evaluate if the two variables are somehow linked. Considering smoothness as a casual variable X and hardness as a casual variable Y, the sample correlation coefficient r is given by: 
<img width="101" alt="Screenshot 2023-06-29 at 11 48 46" src="https://github.com/simothejudge/Sudoku-Project/assets/37406249/80b7d98e-acb6-4914-b697-a32aee169e1f">
Where `Cov` is the covariance between x and y and it’s given by: 
<img width="138" alt="Screenshot 2023-06-29 at 11 49 24" src="https://github.com/simothejudge/Sudoku-Project/assets/37406249/aeac4be9-5ae8-486c-91b4-138cdedcef91">

In Table 2 the results of the correlation analysis are presented. As we can notice, the `r-value` is only `0.3575`. Two variables are considered relevantly correlated when the `r-value` is `>0.4` or `<-0.4`. So we can conclude that there is a slightly positive correlation between smoothness and hardness, but it is not strong enough to confirm our hypothesis. The correlation is for sure related to the fact that, in measuring the hardness, we took into account the number of initial clues. The graph below shows a polynomial trend in the scatter chart, but as said, our data cannot be considered relevant.

|                 | Smoothness         | Hardness         |
| :---            |    :----:          |    :----:        |
| **Average**     | 1.239314944        | 0.3347791138     |
| **Stand. Dev.** | 0.2361055451       | 0.07001666784    |
| **Variance**    | 0.05574582842      | 0.004902333775   |
|                 | **Covariance**     | **r-value**      |
|                 | **0.005909481926** | **0.3574717969** |

## Conclusions
From the experiment, we cannot conclude that there is a strong correlation between the complexity of sudoku and its initial clues. That being said, we need to address that the 150 sudokus that we used as basic samples, were generated randomly by an online generator, and, because of time and effort limitations, it was not possible to build an adequate database of sudokus, composed of more diverse and variable puzzles. As a matter of fact, we could notice that the value of the standard deviation for each sudoku varies between [0.4-1.4], not a large range of values; this means that most of the sudokus processed have a “uniform distribution” of values occurrences. It would be interesting to repeat the experiment with a more specific dataset, where the smoothness can assume values between a wider range. This would be possible by finding a way to build sudokus starting from a list of clues that we want the sudoku to have, but, so far, no such generator was ever implemented.

<img width="732" alt="Screenshot 2023-06-29 at 11 57 20" src="https://github.com/simothejudge/Sudoku-Project/assets/37406249/76d644ae-9aeb-4287-a4aa-ec44905fbc42">

## References

- H. Simonis - Sudoku as a constraint problem. In CP Workshop on Modeling and Reformulating Constraint Satisfaction Problems, pages 13–27, October 2005. 
- A.C.Stuart - Sudoku Creation and Grading, January 2012
- I. Lynce, J. Ouaknine - Sudoku as a SAT Problem, October 2015
- G. McGuire, B. Tugeman, G. Civario - There is no 16-Clue Sudoku: Solving the Sudoku Minimum Number of Clues Problem, January 2012
- Mathematics of Sudokus, https://en.wikipedia.org/wiki/Mathematics_of_Sudoku
- Introduction to Correlation and Regression Analysis - http://sphweb.bumc.bu.edu/otlt/MPH-Modules/BS/BS704_Multivariable/BS704_Multivariable5.html
- F. van Harmelen, V. Lifschitz and B. Porter - Handbook of Knowledge Representation, Foundations of Artificial Intelligence 3, Chapter 2, 2008
















