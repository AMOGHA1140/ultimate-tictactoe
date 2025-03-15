Originally, I created the game in the folder `tictactoe`, but it was performing ~50 searches per second, which was far from optimal. I decided to change the way I was representing board and went with using bit-wise repesenation, which increased the searches to ~500 per second

Both folder contain the same structure of files, 

`tictactoe.py` - Code around the structue of board and to perform operations on it, like getting legal actions possible, making a move etc

`runner1.py` - The main file to run. it contains code written to display a pygame interface for the game, to play against another human or with AI

`mcts.py` - for performing Monte Carlo Tree Search. 

`random_ai.py` - just performs a random move out of the available moves. not really an AI
