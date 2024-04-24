import numpy as np
from logic import *
import MCT_basic
import MCT_mult_Sim
import MCT_depth_limited
import MCT_heuristic
import matplotlib.pyplot as plt
import csv


def save_results_to_csv(results, filename="results.csv"):
    # Open the file in write mode
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["Trial Number", "Score", "Max Tile"])
        # Write the data
        for i, (score, max_tile) in enumerate(results):
            writer.writerow([i, score, max_tile])


def run_multiple_trials(number_of_trials, gride_size, mct):
    results = []
    for i in range(number_of_trials):
        score, max_tile = run_single_game(gride_size, mct)
        results.append((score, max_tile))
        print(f"Trial {i} completed with Score: {score}, Max Tile: {max_tile}")
        print("-----------------------------------")
    return results


def run_single_game(grid_size, mct):
    game_grid = Grid(grid_size)
    game_grid.start_game()
    # print(game_grid)
    while game_grid.is_gameover() is False:
        best_move = mct(game_grid, iterations=20)
        getattr(game_grid, f"shift_{best_move}")()
        # print(game_grid)
        # print(str(best_move))

        # game_grid.update_grid()

    return game_grid.get_score(), game_grid.get_max_value()


label = ["Single Simulation", "Multiple simulations"]
number_of_trials = 50  # Adjust the number of trials as needed
grid_size = 4





results = run_multiple_trials(
    number_of_trials, grid_size, MCT_heuristic.monte_carlo_tree_search
)

save_results_to_csv(results, "results_heuristic.csv")

