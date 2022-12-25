# NIP_CA2_onemax
This is a teamwork.
## Goals
Design a generational evolutionary algorithm which solves the 1-MAX problem of size 15 in at least 95 runs out of 100, converging
in less than 1000 generations but taking as many generations as possible to converge.

# OneMax.py

## General overview

This module first generates the parameters in the inside EA through the outside EA and then solves the One Max problem through
the inside EA. The mean of looping times and success rates for the inside EA are passed as feedback to the outside EA, which
evolves the parameters of the inside EA.

The file includes the OneMax.py script.

## How to use
The script has three main functions.

### EA_in_EA()
This function use the EA in EA to solve the problem, and will return 'result', which contains optimal parameters combinations to  the problem.

### result_test()
To run this, change the parameters in the function. Then you can test the perfomence of the parameters combination.

### small_scale
The script takes no command line arguments.  
This function will search the best parameters combination around the combination you have got in function EA_in_EA().

# modified_main_function_.py
## General overview
This file is the basic code to use EA to solve 1-MAX problem from the team.  
Some updates are added in this file to test function's performence.

## latest update
Function "population_fitness", "weakest_tournament", "roulette_wheel_replacement", "limited_crossover" were added.  
Population size and chromosome length were set as global variable.  
roulette_wheel_replacement needs to be reqair.  
