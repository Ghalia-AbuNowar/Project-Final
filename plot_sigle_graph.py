from collections import Counter
import csv
import matplotlib.pyplot as plt
import numpy as np

def read_results_from_csv(filename):
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        results = []
        for row in reader:
            trial_number = int(row[0])
            score = int(row[1])
            max_tile = int(row[2])
            results.append((score, max_tile))
    return results




# Load results from CSV files
results_basic = read_results_from_csv("results_basic.csv")
results_multi_simulation = read_results_from_csv("results_multi_simulation.csv")
results_multi_simulation_30 = read_results_from_csv("results_depth_limited_30.csv")
results_heuristic = read_results_from_csv("results_heuristic.csv")

# Extract scores and maximum tiles for plotting
scores_basic = [result[0] for result in results_basic]
max_tiles_basic = [result[1] for result in results_basic]


scores_multi_simulation = [result[0] for result in results_multi_simulation]
max_tiles_multi_simulation = [result[1] for result in results_multi_simulation]


scores_multi_30 = [result[0] for result in results_multi_simulation_30]
max_multi_30= [result[1] for result in results_multi_simulation_30]


scores_heuristic = [result[0] for result in results_heuristic]
max_heuristic = [result[1] for result in results_heuristic]



total_basic = len(scores_basic)
total_multi = len(scores_multi_simulation)
total_multi_30 = len(scores_multi_30)
total_heuristic = len(scores_heuristic)

weights_basic = np.ones_like(scores_basic) / total_basic
weights_multi = np.ones_like(scores_multi_simulation) / total_multi
weights_multi_30 = np.ones_like(scores_multi_30) / total_multi_30
weights_heuristic = np.ones_like(scores_heuristic) / total_heuristic

# print(weights_multi)

# Calculate statistics for each dataset
mean_basic = np.mean(scores_basic)
std_basic = np.std(scores_basic)
mean_multi = np.mean(scores_multi_simulation)
std_multi = np.std(scores_multi_simulation)
mean_multi_30 = np.mean(scores_multi_30)
std_multi_30 = np.std(scores_multi_30)
mean_heuristic = np.mean(scores_heuristic)
std_heuristic = np.std(scores_heuristic)




# Histogram settings
bins = 20
alpha = 0.75
colors = ['blue', 'green', 'red', 'purple']
titles = ['Standard MCTS', 'Multi-Simulation MCTS', 'Depth limited MCTS', 'Heuristic guided MCTS']
weights =[weights_basic, weights_multi, weights_multi_30, weights_heuristic]
scores = [scores_basic, scores_multi_simulation, scores_multi_30, scores_heuristic]
means = [mean_basic, mean_multi, mean_multi_30, mean_heuristic]
stds = [std_basic, std_multi, std_multi_30, std_heuristic]

# Plot histograms for each configuration
for i in range(4):
    plt.figure(figsize=(8, 5))
    plt.hist(scores[i], bins=bins, weights=weights[i], alpha=alpha, color=colors[i])
    plt.title(f'Histogram of Scores for {titles[i]}')
    plt.xlabel('Score')
    plt.ylabel('Probability')
    plt.grid(True)
    # Annotate with mean and std
    plt.axvline(means[i], color='k', linestyle='dashed', linewidth=1)
    plt.text(means[i] * 1.05, plt.ylim()[1] * 0.9, f'Mean: {means[i]:.2f}\nSD: {stds[i]:.2f}', color='k')
    # plt.show()
    plt.savefig(titles[i] + '.png')



    



colors = ['blue', 'green', 'red', 'purple']
titles = ['Max Tile Standard MCTS', 'Max Tile Multi-Simulation MCTS', 'Max Tile Depth limited MCTS', 'Max Tile Heuristic guided MCTS']
max_tile = [max_tiles_basic, max_tiles_multi_simulation, max_multi_30, max_heuristic]

for i in range(4):
    frequency_basic = Counter(max_tile[i])

    # Separate the data into labels and values for plotting
    labels, values = zip(*frequency_basic.items())
    values = list(values)
    print(values)
    print(labels)
    
    for j in range(len(values)):
        values[j] = values[j]/100


   
    plt.figure(figsize=(8, 5))
    plt.xticks(labels, labels=[str(x) for x in labels])
    plt.bar(labels, values, width=200,  color=colors[i]) 
    plt.title(f'Distribution of Tiles for {titles[i]}')
    plt.xlabel('Tile Value')
    plt.ylabel('Probability')
    plt.grid(True)
    
    # plt.show()
    plt.savefig(titles[i] + '.png')

