import numpy as np

X = 'X'
O = 'O'
EMPTY = None

def initial_state():
    """
    state is a 2-element tuple
    1st element is a list, containing x_pos and o_pos, basically containing the places on the board where X is, and where O is
    2nd is the current mini-board, where you should play, 0-8 represent the mini-board, 9 means everywhere on the board
    """
    return ([0, 0], 9)

def is_state_valid(state):
    """
    Checks if the current state is valid or not
    """
    x_bits, o_bits = state[0]

    # if x_bits &y_bits !=0, it means some bits are overlapping for them, which is illegal
    return not (x_bits&o_bits)

def player(state):
    """
    Returns the player who has the turn
    """

    x_bits, o_bits = state[0]

    total_moves = bin(x_bits | o_bits).count('1')

    return X if total_moves%2==0 else O



def legal_action(state, action):
    """
    checks if the requested action can be made. If yes, then returns the state after performing the action
    """

    x_bit, o_bit = state[0]

    #this checks if the square to be moved on is empty or not
    if (x_bit|o_bit) & (1 << (80-action))!=0:
        return False
    
    #if the mini board you want to move on, is terminated, its illegal
    if state[1]==9 and mini_board_terminal(get_mini_boards(state, action/9)):
        return False
    
    if state[1]!=9 and state[1]!=action/9:
        return False
    
    return True   


def result(state, action):
    """
    Performs the given action on given state and results return

    action is just the position where you want to move
    """

    x_bit, o_bit = state[0]

    if player(state)==X:
        x_bit = x_bit | (1 << (80-action))
    else:
        o_bit = o_bit | (1 << (80-action))
    
    return ([x_bit, o_bit], action/9)






def mini_board_utility(mini_board):
    """
    mini_board -> 2-element tuple, (x_bits, o_bits)
    """
    WIN_MASKS = [
        0b111000000, 0b000111000, 0b000000111, #checking along rows
        0b001001001, 0b010010010, 0b100100100, #checking along columns
        0b100010001, 0b001010100               #checking along diagonals
    ]

    x_bits, o_bits = mini_board

    for mask in WIN_MASKS:
        if (mask & x_bits) == mask:
            return 1
        if (mask & o_bits) == mask:
            return -1
    return 0


def mini_board_terminal(mini_board):

    utility_value = mini_board_utility(mini_board)

    if utility_value==1 or utility_value==-1:
        return True

    x_bits, o_bits = mini_board

    # if all possible moves played, game is over and is a draw
    if x_bits|o_bits==0b111111111:
        return True
    
    return False
    
def mini_board_winner(mini_board):
    """
    Returns the winner of the mini_board
    """

    utlity_value = mini_board_utility(mini_board)

    if utlity_value==1:
        return X
    elif utlity_value==-1:
        return O
    return None

def get_mini_boards(state, board_number=None):

    x_bits, o_bits = state[0]

    # if board number if given, then return just that mini-board
    if board_number:
        mask = 0b111111111 << 9 * (8-board_number)
        return x_bits&mask, o_bits&mask

    mini_boards = []

    for _ in range(9):
        mini_boards.insert(0, (0b111111111&x_bits, 0b111111111&o_bits))
        x_bits = x_bits >> 9
        o_bits = o_bits >> 9
    
    return mini_boards

def create_board_abstraction(state):
    
    mini_boards = get_mini_boards(state)

    x_bits = o_bits = 0

    for i, board in enumerate(mini_boards):
        winner = mini_board_winner(board)
        if winner==X:
            x_bits = x_bits | (1<<(8-i))
        elif winner == O:
            o_bits = o_bits | (1<< (8-i))
    
    return (x_bits, o_bits)


def terminal(state):
    """
    return True if the game has ended, False otherwise
    """

    board_abstraction = create_board_abstraction(state)

    return mini_board_terminal(board_abstraction)


def utility(state):
    """
    Returns 1 if X won the entire game, -1 if O won, 0 otherwise
    """
    #this is not completely same as previous version as it doesn't use score
    
    board_abstraction = create_board_abstraction(state)    
    return mini_board_utility(board_abstraction)
    
def winner(state):
    """
    return winner of the game
    """

    if not terminal(state):
        return None
    
    utility_value = utility(state)

    if utility_value==1:
        return X
    elif utility_value==-1:
        return O    
    
    return None
    
def getRCrc_from_position(position):
    position = np.base_repr(position, base=3)
    position =  '0'*(4-len(position))+position
    return [int(i) for i in position]




    



    

