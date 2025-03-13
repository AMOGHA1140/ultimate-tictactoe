### tictactoe.py 
This file contains the basic logic for board representation and different operations on it. 
It can be optimized with a bit representation of the board, which will be written and uploaded later

### runner.py
Main file to run. this contains the pygame logic to display the game, allow 2 people to play against each other or play against AI

### mcts.py 
Contains the logic and implementation of Monte Carlo Search Tree. The code is extremely unoptimized, performing only about ~50 searches per second. this NEEDS to increase. 
the code has to be able to perform atleast ~2500 per second to be viable to be used newly for each state

Furthermore, new file has to be written to make use of past searched states, basically memoization. 

### random_ai.py
Performs random moves. not an AI tbh
