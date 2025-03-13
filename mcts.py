import numpy as np
import random
import copy
import tictactoe as ttt


class Node:
    
    def __init__(self, state, parent=None, action=None):
        
        self.state = state
        self.action = action
        self.children_nodes = []
        self.parent = parent

        self.xwins = 0
        self.draws = 0
        self.owins = 0
        self.total_visits = 0
        
        self.untried_actions = ttt.actions(state)

    def is_terminal_node(self):
        return ttt.terminal(self.state)
    
    def expand(self):

        action = self.untried_actions.pop()

        child_state = ttt.result(self.state, action)
        child_node = Node(child_state, self, action)
        
        self.children_nodes.append(child_node) 
        return child_node

    def is_fully_expanded(self):
        return len(self.untried_actions)==0

    def rollout_policy(self, possible_actions):
        return random.choice(possible_actions)

    def rollout(self):

        current_rollout_state = self.state
        while not ttt.terminal(current_rollout_state):
            possible_moves = ttt.actions(current_rollout_state)
            action = self.rollout_policy(possible_moves)
            current_rollout_state = ttt.result(current_rollout_state, action)
        
        utility_value = ttt.utility(current_rollout_state)
        return utility_value


    def backpropagate(self, xwin, owin, draw):

        if any(i not in {0, 1} for i in (xwin, owin, draw)):
            raise ValueError(f"xwin: {xwin}, owin: {owin}, draw: {draw} - Values mismatch")
        if xwin+owin+draw != 1:
            raise ValueError(f"xwin, owin, draw don't sum to 1, xwin: {xwin}, owin: {owin}, draw: {draw}")
        
        self.total_visits += 1
        self.xwins += xwin
        self.owins += owin
        self.draws += draw

        if self.parent:
            self.parent.backpropagate(xwin, owin, draw)

    @property
    def q(self):
        next_to_move = ttt.player(self.state)
        if next_to_move==ttt.X:
            return self.xwins - self.owins
        else:
            return self.owins - self.xwins

    def uct(self, child, c=1.4):
        if child.total_visits == 0:
            return float('inf')
        score = child.q / child.total_visits + c * np.sqrt(np.log(self.total_visits) / child.total_visits)

        return score


    def best_child(self, c=1.4):
        # print(len(self.children_nodes))
        choice_weights = [self.uct(child, c) for child in self.children_nodes]
        # print(choice_weights)
        if len(choice_weights)<9:
            print(choice_weights, "\n", [c.action for c in self.children_nodes])
        return self.children_nodes[np.argmax(choice_weights)]
    

class MCTS:

    def __init__(self, root:Node):
        self.root = root

    def tree_policy(self):
        
        current_node = self.root

        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_child(self, simulation_number):
        
        for i in range(simulation_number):
            print(f"Simulation: {i}-{len(self.root.children_nodes)}-{len(self.root.untried_actions)}")
            v = self.tree_policy()
            utility_value = v.rollout()
            v.backpropagate(xwin=(utility_value==1), owin=(utility_value==-1), draw=(utility_value==0))

        print([c.action for c in self.root.children_nodes])
        return self.root.best_child(c=0)


def best_move(state, simulation_count=100):
    root = Node(state)
    mcts = MCTS(root)
    best_child = mcts.best_child(simulation_number=simulation_count)
    
    return best_child.action
    

