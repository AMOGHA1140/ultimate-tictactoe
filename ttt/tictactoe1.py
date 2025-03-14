import numpy as np
from functools import lru_cache

X = 'X'
O = 'O'
EMPTY = None

class myInt(int):

    def __init__(self):
        super().__init__()


class State:

    def __init__(self, x_bits=0, o_bits=0, valid_mini_board=9):
        
        self.x_bits = x_bits
        self.o_bits = o_bits
        self.valid_action = valid_mini_board

    def __getitem__(self, indices):
        """
        Accessing as state[R, C] returns a mini_board at (R, C) as a bit-state

        accessing as state[R, C, r, c], however, returns X, O or EMPTY depending on position
        """
        if not isinstance(indices, tuple):
            raise IndexError(f"State can't be accessed with index: {indices}")
        
        if len(indices) == 2:
            R, C = indices
            return get_mini_boards(self, 3*R+C)
        
        elif len(indices) == 4:
            R, C, r, c = indices
            mask = (1<< (80 - get_position_from_RCrc(R, C, r, c)))

            if self.x_bits & mask:
                return X
            elif self.o_bits & mask:
                return O
            else:
                return None
        else:
            raise ValueError(f"Invalid index: {indices}")
    


def initial_state():
    """
    returns empty state
    """
    return State()

def is_state_valid(state:State):
    """
    Checks if the current state is valid or not
    """
    x_bits, o_bits = state.x_bits, state.o_bits

    # if x_bits &y_bits !=0, it means some bits are overlapping for them, which is illegal
    return not (x_bits&o_bits)

def player(state:State):
    """
    Returns the player who has the turn
    """

    # x_bits, o_bits = state.x_bits, state.o_bits

    total_moves = (state.x_bits | state.o_bits).bit_count()

    return X if total_moves%2==0 else O



def legal_action(state:State, action):
    """
    checks if the requested action can be made. If yes, then returns the state after performing the action
    """
    if isinstance(action, tuple):
        action = get_position_from_RCrc(*action)
    

    x_bit, o_bit = state.x_bits, state.o_bits

    #this checks if the square to be moved on is empty or not
    if (state.x_bits | state.o_bits) & (1 << (80-action)):
        return False
    
    #if the mini board you want to move on, is terminated, its illegal
    if state.valid_action==9 and mini_board_terminal(get_mini_boards(state, action//9)):
        return False
    
    if state.valid_action!=9 and state.valid_action!=action//9:
        # print("waw3")

        return False
    
    return True   


def result(state:State, action):
    """
    Performs the given action on given state and results return

    action is just the position where you want to move
    """
    if not legal_action(state, action):
        raise ValueError(f"Illegal action: {action}, x-bit={state.x_bits}, o-bits={state.o_bits}, valid_action_board={state.valid_action}")

    if isinstance(action, tuple):
        if len(action) != 4:
            raise ValueError(f"action is not 4 element tuple: {action}")
        action = get_position_from_RCrc(*action)
    


    x_bit, o_bit = state.x_bits, state.o_bits

    if player(state)==X:
        x_bit = x_bit | (1 << (80-action))
    else:
        o_bit = o_bit | (1 << (80-action))
    

    R, C, r, c = getRCrc_from_position(action)
    new_state = State(x_bit, o_bit)

    if mini_board_terminal(get_mini_boards(new_state, 3*r+c)):
        new_state.valid_action=9
    else:
        new_state.valid_action = 3*r+c

    return new_state






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
    """
    Parameters
    -----------------
    mini_board: 2-element tuple of (x_bits, o_bits)

    """



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

@lru_cache(maxsize=100_000)
def get_mini_boards(state:State, board_number=None):

    x_bits, o_bits = state.x_bits, state.o_bits

    # if board number if given, then return just that mini-board
    if board_number!=None:
        x_bits = x_bits >> 9 * (8-board_number)
        o_bits = o_bits >> 9 * (8 - board_number)
        mask = 0b111111111
        return x_bits&mask, o_bits&mask

    mini_boards = []

    for _ in range(9):
        mini_boards.insert(0, (0b111111111&x_bits, 0b111111111&o_bits))
        x_bits = x_bits >> 9
        o_bits = o_bits >> 9
    
    return mini_boards

def create_board_abstraction(state:State):
    
    mini_boards = get_mini_boards(state)

    x_bits = o_bits = 0

    for i, board in enumerate(mini_boards):
        winner = mini_board_winner(board)
        if winner==X:
            x_bits = x_bits | (1<<(8-i))
        elif winner == O:
            o_bits = o_bits | (1<< (8-i))
    
    return (x_bits, o_bits)


def terminal(state:State):
    """
    return True if the game has ended, False otherwise
    """

    board_abstraction = create_board_abstraction(state)

    # print(f"x-{bin(board_abstraction[0])}, y-{bin(board_abstraction[1])}")
    
    if mini_board_terminal(board_abstraction):
        return True
    
    all_full = True

    for mb in get_mini_boards(state):
        x, o = mb
        if not mini_board_terminal((x, o)):
            all_full = False
            break
    return all_full


def utility(state:State):
    """
    Returns 1 if X won the entire game, -1 if O won, 0 otherwise
    """
    #this is not completely same as previous version as it doesn't use score
    
    board_abstraction = create_board_abstraction(state)    
    return mini_board_utility(board_abstraction)
    
def winner(state:State):
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
    return position//27, (position%27)//9, position%27%9//3, position%27%9%3

def get_position_from_RCrc(R, C, r, c):
    return 27*R+9*C+3*r+c

def is_position_empty(state:State, position):

    return not (state.x_bits | state.o_bits) & (1 << (80-position))



def actions(state:State):

    x_bits = state.x_bits
    o_bits = state.o_bits
    occupied =  state.x_bits | state.o_bits

    valid_actions = []
    MASK = 0b111111111


    if state.valid_action == 9:
        for mb_index in range(9):
            
            

            shift = 9 * (8-mb_index)
            mb_x = (x_bits >> shift) & MASK
            mb_o = (o_bits >> shift) & MASK

            if mini_board_terminal((mb_x, mb_o)):
                continue
            
            empty_cells = ~(mb_o | mb_x) & MASK

            while empty_cells:

                lsb = empty_cells & -empty_cells
                action = mb_index*9 + (9-lsb.bit_length())
                valid_actions.append(action)
                empty_cells = empty_cells ^ lsb


    else:

        
        occupied = (occupied >> 9 * (8-state.valid_action)) & MASK
        empty =  (~occupied) & MASK

        while empty:
            lsb = empty & -empty
            mini_board_position = 8 - (lsb.bit_length() - 1)
            valid_actions.append(state.valid_action*9 + mini_board_position)

            empty = empty ^ lsb
    
    
    return valid_actions

