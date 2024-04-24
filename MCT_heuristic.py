import random
from copy import deepcopy
from math import log, sqrt
import numpy as np


class MCTSNode:
    def __init__(self, grid, move=None, parent=None):
        self.grid = grid
        self.parent = parent
        self.move = move  # parent move
        self.children = []
        self.visits = 0
        self.total_score = 0  # Total score from all simulations

    def is_fully_expanded(self):
        return len(self.children) == len(self.grid.get_possible_moves())

    def expand(self):
        possible_moves = ["left", "right", "up", "down"]
        moves_scores = []
        for move in possible_moves:
            new_grid = deepcopy(self.grid)
            getattr(new_grid, f"shift_{move}")()

            if new_grid.grid_change(self.grid):  # Ensure the move changes the grid
                moves_scores.append((move, new_grid.calculate_snake_score(), new_grid))

        # Sort moves based on snake scores, highest first
        moves_scores.sort(key=lambda x: x[1], reverse=True)

        # Expand nodes based on sorted moves
        for move, score, new_grid in moves_scores:
            new_node = MCTSNode(new_grid, move, self)
            self.children.append(new_node)


    def select_child(self):
        best_score = float("-inf")
        best_children = []

        for child in self.children:
            if child.visits > 0:
                base_score = child.total_score / child.visits  # Average result from simulations
                snake_score = child.grid.calculate_snake_score()  # Calculate heauristic score
                combined_score =  snake_score * 0.1 + base_score # Combine scores, adjust weighting

                exploit = combined_score
                explore = sqrt(2 * log(self.visits) / child.visits)
                score = exploit + explore

                if score > best_score:
                    best_score = score
                    best_children = [child]
                elif score == best_score:
                    best_children.append(child)
            else:
                return child  

        return random.choice(best_children)

    def backpropagate(self, result):
        """
        part where you update the info
        """
        self.visits += 1
        self.total_score += result
        if self.parent:
            self.parent.backpropagate(result)


    def apply_move(self, grid, move):
        if move == 'left':
            grid.shift_left()
        elif move == 'right':
            grid.shift_right()
        elif move == 'up':
            grid.shift_up()
        elif move == 'down':
            grid.shift_down()


def apply_move(grid, move):
        if move == 'left':
            grid.shift_left()
        elif move == 'right':
            grid.shift_right()
        elif move == 'up':
            grid.shift_up()
        elif move == 'down':
            grid.shift_down()

def rollout(grid, num_simulations=10, max_depth=20):
    total_score = 0
    for _ in range(num_simulations):
        simulation_grid = deepcopy(grid)
        for _ in range(max_depth):
            if simulation_grid.is_gameover():
                break
            move = random.choice(["left", "right", "up", "down"])
            apply_move(grid, move)
        total_score += simulation_grid.get_score()
    average_score = total_score / num_simulations
    return average_score




def monte_carlo_tree_search(initial_grid, iterations=100, num_rollouts_per_node=5):
    root = MCTSNode(initial_grid)
    for _ in range(iterations):
        node = root
        while node.children:
            node = node.select_child()
        if not node.is_fully_expanded():
            node.expand()
        if node.children:
            node = random.choice(node.children)
        score = rollout(deepcopy(node.grid), num_rollouts_per_node, 30)
        node.backpropagate(score)

    if root.children:
        best_node = max(root.children, key=lambda x: x.visits)
        return best_node.move
    else:
        return None



# To use:
# initial_grid = Grid(4)
# initial_grid.start_game()
# best_move_direction = monte_carlo_tree_search(initial_grid)
# print("Best move direction:", best_move_direction)
