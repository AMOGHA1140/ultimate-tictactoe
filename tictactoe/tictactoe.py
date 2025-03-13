"""
I want to go through and explain the main logic for state, action, board representation and the logic for my code here. 

mini-board -> represents the smaller 3x3 boards in the grid


board -> will be a numpy-4D array to represent the 81 squares. Say the index is (R, C, r, c). (R, C) represents the mini-board, and (r, c) represents the square within the mini-board

state -> it is a tuple of 2 elements. 1st element consists the board, the 2nd consists of the valid mini-board position (R, C) where you can move next. 0 <= R, C <= 2
if the value is `0`, then moving on any mini-board is allowed


"""



import numpy as np
import copy

X = 'X'
O = 'O'
EMPTY = None

def initial_state():
    """
    Returns the initial state of the board. 
    State is a combination of the board and the possible action mini-boards

    """

    #Represents a single 3x3 board
    mini_board = [[EMPTY for _ in range(3)] for __ in range(3)]

    board = [[mini_board for _ in range(3)] for __ in range(3)]
    board = np.array(board)
    
    return [board, 0]
    
def player(state) -> str:
    """
    returns the player who has the next move on the board
    """
    board = state[0]
    copy = board.flatten()
    X_count = np.count_nonzero(copy==X)
    O_count = np.count_nonzero(copy==O)
    
    if O_count == X_count:
        return X
    else:
        return O
    
def legal_action(state, action, on_click=False):
    """
    Returns weather an action on a state is legal or not

    Action is a 4-element tuple, first 2 elements representing move on big-board
    and the latter 2 on the mini-board
    state[1] will be a 2-element tuple representing valie mini-board to move in, or zero if moving anywhere is allowed
    """
    
    #if the square is not empty, then you can't make a move there
    if state[0][action] != EMPTY:
        return False
    
    
    if state[1] ==0 and mini_board_terminal(state[0][action[:2]], on_click=on_click):
        return False

    if state[1] != 0 and state[1] != action[:2]:
        return False

    

    return True
    # if state[1] is zero, then moving anywhere on the board is valid
    # otherwise, (R, C) should be same as (R, C, r, c)[:2]

def result(state, action, on_click=False):
    """
    checks if the requested action can be made. If yes, then returns the state after performing the action
    """

    if not legal_action(state, action, on_click):
        raise ValueError(f"Action not legal. allowed: {state[1]}. Move made: {action}")
    
    state = copy.deepcopy(state)
    
    current_player = player(state)
    
    state[0][action] = current_player

    #if the mini-board where the next move can be played, is over, then next move can be played anywhere
    if mini_board_terminal(state[0][action[2:]]):
        state[1] = 0
    else:
        state[1] = action[2:]

    return state

def mini_board_utility(mini_board):
    """
    mini_board: the 3x3 mini-board

    returns 1 if X has won, -1 if O won, 0 otherwise, only for 3x3 board
    """

    if mini_board.shape != (3,3):
        raise ValueError("mini_board should be a 3x3 numpy.ndarray")
    

    #checking if it matches as 3 in a row
    for row in mini_board:
        if all([element==X for element in row]):
            return 1
        if all([element==O for element in row]):
            return -1

    #checking if it matches as 3 in a column
    for i in range(3):
        if all([mini_board[j][i]==X for j in range(3)]):
            return 1
        if all([mini_board[j][i]==O for j in range(3)]):
            return -1
    
    #checking if it matches as 3 in a diagonal
    if all([mini_board[i][i]==X for i in range(3)]) or all([mini_board[i][2-i]==X for i in range(3)]):
        return 1
    if all([mini_board[i][i]==O for i in range(3)]) or all([mini_board[i][2-i]==O for i in range(3)]):
        return -1
    
    #if nothing matches, return 0 for draw
    return 0
   
def mini_board_terminal(mini_board:np.ndarray, on_click=False):
    """
    return True if the game had ended for the mini_board, False otherwise
    """

    utility_value = mini_board_utility(mini_board)

    if utility_value==1 or utility_value==-1:
        return True
    

    if np.count_nonzero(mini_board.flatten()==EMPTY)>0:
        return False
    
    return True


def mini_board_winner(mini_board:np.ndarray):
    """
    `mini_board`: the 3x3 mini-board
    return X if X has won, O is O has won, None otherwise
    """

    utility_value = mini_board_utility(mini_board)

    if utility_value==1:
        return X
    elif utility_value== -1:
        return O
    
    return None

def actions(state):
    """
    `state`: state of the game consisting of the board and the valid mini-board to move in

    returns a list all possible actions that can be taken in current state
    """

    if state[1] == 0:

        empty_indices = np.argwhere(state[0]==EMPTY).tolist()
        answer =  [tuple(i) for i in empty_indices]
    
    else:
        R, C = state[1]

        empty_indices = np.argwhere(state[0][R, C]==EMPTY).tolist()

        answer = [(R, C, *idx) for idx in empty_indices]
    
    return [idx for idx in answer if legal_action(state, idx)]

def utility(state):

    """
    Returns 1 if X won the entire game, -1 if O won, 0 otherwise
    """
    board = state[0]

    board_abstraction = [[mini_board_winner(board[R][C]) for C in range(3)] for R in range(3)]

    for row in board_abstraction:
        if all([element==X for element in row]):
            return 1
        if all([element==O for element in row]):
            return -1

    #checking if it matches as 3 in a column
    for i in range(3):
        if all([board_abstraction[j][i]==X for j in range(3)]):
            return 1
        if all([board_abstraction[j][i]==O for j in range(3)]):
            return -1
    
    #checking if it matches as 3 in a diagonal
    if all([board_abstraction[i][i]==X for i in range(3)]) or all([board_abstraction[i][2-i]==X for i in range(3)]):
        return 1
    if all([board_abstraction[i][i]==O for i in range(3)]) or all([board_abstraction[i][2-i]==O for i in range(3)]):
        return -1
    

    
    for R in range(3):
        for C in range(3):
            if not mini_board_terminal(board[R][C]):
                return 0

    board_abstraction = np.array(board_abstraction).flatten()
    score = np.count_nonzero(board_abstraction==X) - np.count_nonzero(board_abstraction==O)

    if score>0:
        return 1
    elif score==0:
        return 0
    else:
        return -1
    


   

def terminal(state):
    """
    Returns True if the entire game is over, False otherwise
    """
    
    utility_value = utility(state)

    if utility_value == 1 or utility_value == -1:
        return True
    
    board = state[0]


    #if even a single mini-board is not terminal, then the game is not over
    for R in board:
        for mini_board in R:
            if not mini_board_terminal(mini_board):
                return False
    
    return True

def winner(state):
    """
    returns the winner of the game
    """

    if not terminal(state):
        return None
    
    utility_value = utility(state)

    if utility_value==1:
        return X
    elif utility_value==-1:
        return O
    else:
        return None


# state = initial_state()
# state = result(state, (1, 1, 1, 1))
# 
# from pprint import pprint
# pprint((actions(state)))

    