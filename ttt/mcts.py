import numpy as np
import time
import random
import tictactoe1 as ttt

class Node:

    def __init__(self, state:ttt.State, parent=None, action=None):

        self.state = state
        self.action = action
        self.parent = parent
        
        self.children = []
        self.xwins = 0
        self.owins = 0
        self.draws = 0
        self.total_visits = 0

        self.untried_actions = ttt.actions(state)

    def is_terminal_node(self):
        return ttt.terminal(self.state)

    def expand(self):

        action = self.untried_actions.pop()

        child_state = ttt.result(self.state, action)
        child_node = Node(child_state, self, action)

        self.children.append(child_node)
        return child_node
    
    def is_fully_expanded(self):
        return len(self.untried_actions) == 0
    
    def rollout_policy(self, possible_actions):
        # print(possible_actions)
        return random.choice(possible_actions)
    
    def rollout(self):
        
        current_rollout_state = self.state

        while not ttt.terminal(current_rollout_state):
            possible_moves = ttt.actions(current_rollout_state)
            if len(possible_moves)==0:
                raise ValueError(f"x: {current_rollout_state.x_bits}, o: {current_rollout_state.o_bits}, {current_rollout_state.valid_action}")

            action = self.rollout_policy(possible_moves)
            current_rollout_state = ttt.result(current_rollout_state, action)
        
        utility_value = ttt.utility(current_rollout_state)
        return utility_value

    def backpropagate(self, xwin, owin, draw):

        if any(i not in {0, 1} for i in (xwin, owin, draw)):
            raise ValueError
        if xwin+owin + draw !=1:
            raise ValueError
        
        self.total_visits += 1
        self.xwins += xwin
        self.owins += owin
        self.draws += draw

        if self.parent:
            self.parent.backpropagate(xwin, owin, draw)

    @property
    def q(self):
        next_to_move = ttt.player(self.state)
        if next_to_move == ttt.O:
            return self.xwins - self.owins
        else:
            return self.owins - self.xwins
        
    def uct(self, child, c=1.4):
        if child.total_visits == 0:
            return float('inf')
        score = child.q / child.total_visits + c * np.sqrt(np.log(self.total_visits) / child.total_visits)
        
        return score
    
    def best_child(self, c=1.4):

        choice_weights = [self.uct(child, c) for child in self.children]

        return self.children[np.argmax(choice_weights)]
    

        
        
class MCTS:

    def __init__(self, root: Node):
        self.root = root

    def tree_policy(self):

        current_node = self.root

        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        
        return current_node

    def best_child(self, simulation_number=None, simulation_time=None):

        if not simulation_number and not simulation_time:
            raise BaseException

        if simulation_number:
            start = time.time()
            for i in range(simulation_number):
                # print(f"Simulation: {i}-{len(self.root.children)}-{len(self.root.untried_actions)}")

                v = self.tree_policy()
                utility_value = v.rollout()
                v.backpropagate(xwin=(utility_value==1), owin=(utility_value==-1), draw=(utility_value==0))

            best_child = self.root.best_child(c=0)
            ai_win_percent = best_child
            print(f"20k simulations done: Time taken- {time.time()-start},")# AI-wins {}% of times")
            return best_child
        
        else:
            start = time.time()
            counter = 0

            while time.time() - start  < simulation_time:
                # print(f"Simulation: {counter}-{len(self.root.children)}-{len(self.root.untried_actions)}")
                counter+=1
                v = self.tree_policy()
                utility_value = v.rollout()
                v.backpropagate(xwin=(utility_value==1), owin=(utility_value==-1), draw=(utility_value==0))
            
            return self.root.best_child(c=0)


        




def best_move(state, simulation_count=100, simulation_time=10):
    root = Node(state)
    mcts = MCTS(root)
    best_child = mcts.best_child(simulation_number=20000)
    
    return best_child.action
    

