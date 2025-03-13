import numpy as np
import random
import tictactoe as ttt

def ai_move(state):
    actions = ttt.actions(state)
    return random.sample(actions, k=1)[0]
