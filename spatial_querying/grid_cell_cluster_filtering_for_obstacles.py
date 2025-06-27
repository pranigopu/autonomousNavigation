import numpy as np

#================================================
# MAIN FUNCTION: QUERY OBSTACLES FROM A GIVEN CLUSTER AND GET THEIR POSITIONS

def query_obstacles(grid: np.ndarray, i_1: int, i_2: int, j_1: int, j_2: int) -> np.ndarray:
    '''
    Queries the specified cluster of a grid to find positions with
    obstacles ('X').
    
    ---

    PARAMETERS:
    - `grid` (np.ndarray): 2D array representing the obstacle grid
    - `i_1` (int): Start row index (inclusive)
    - `i_2` (int): End row index (exclusive)
    - `j_1` (int): Start column index (inclusive)
    - `j_2` (int): End column index (exclusive)
    
    RETURNS:
    - (np.ndarray): Array of positions where obstacles are present
    '''

    # Extract the subgrid (cluster of cells based on row and column ranges):
    subgrid = grid[i_1:i_2, j_1:j_2]
    
    # Find the positions where the obstacles ('X') are located:
    obstacle_positions = np.argwhere(subgrid == 'X')
    
    # Convert local indices back to global indices based on the slices:
    obstacle_positions[:, 0] += i_1
    obstacle_positions[:, 1] += j_1
    
    return obstacle_positions

#================================================
# VISUALISATION

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def visualise_grid(grid: np.ndarray, i_1: int, i_2: int, j_1: int, j_2: int, obstacles: np.ndarray):
    '''
    Visualises the grid and highlights the chosen cluster and obstacles
    within the cluster.

    ---

    PARAMETERS:
    - `grid` (np.ndarray): 2D array representing the obstacle grid
    - `i_1` (int): Start of the range for i (inclusive)
    - `i_2` (int): End of the range for i (exclusive)
    - `j_1` (int): Start of the range for j (inclusive)
    - `j_2` (int): End of the range for j (exclusive)
    - `obstacles` (np.ndarray): Positions of obstacles within cluster
    '''

    _, ax = plt.subplots(figsize=(8, 6))

    # Plot full grid with 'X' as obstacles and '.' as free space:
    ax.imshow(grid == 'X', cmap="Blues", interpolation="none", origin="upper")
    
    # Show the cluster region by highlighting the slice:
    cluster_rect = patches.Rectangle(
        (j_1 - 0.5, i_1 - 0.5), j_2 - j_1, i_2 - i_1,
        linewidth=5, edgecolor="orange", facecolor="none", linestyle="--")
    ax.add_patch(cluster_rect)
    
    # Mark obstacles within the cluster:
    for pos in obstacles:
        ax.text(pos[1], pos[0], 'X', ha='center', va='center', color='red', fontsize=12, weight='bold')

    # Set axis labels and grid lines:
    ax.set_xticks(np.arange(-0.5, grid.shape[1], 1))
    ax.set_yticks(np.arange(-0.5, grid.shape[0], 1))
    ax.set_xticklabels(np.arange(0, grid.shape[1] + 0.5, 1))
    ax.set_yticklabels(np.arange(0, grid.shape[0] + 0.5, 1))
    ax.set_xlabel("Columns")
    ax.set_ylabel("Rows")
    ax.set_aspect("equal")
    ax.grid(True, which="both", linestyle='-', linewidth=1, color="black")
    
    plt.title("Grid Visualisation with Cluster and Obstacles")
    plt.show()

#================================================
# TEST CASES

# Defining the obstacle grid:
grid = np.array([
    ['.', '.', 'X', '.', '.', '.'],
    ['X', '.', '.', 'X', '.', '.'],
    ['.', 'X', '.', '.', '.', 'X'],
    ['.', '.', '.', '.', 'X', '.'],
    ['.', '.', 'X', '.', '.', '.']])

# Printing the obstacle grid for reference:
print("\nObstacle Grid:\n")
for row in grid:
    print(' '.join(row))

#------------------------------------
# TEST CASE 1: Obstacles Found

print(f"\n{'-'*48}\nTEST CASE 1: Obstacles Found\n")

# Querying the obstacles in a cluster (for this example):
obstacles = query_obstacles(grid, 1, 4, 2, 5)

# Printing the indices retrieved (for reference):
print(f"\nObstacle Positions (size = {obstacles.size}):\n{obstacles}\n")

# Visualising the grid, cluster, and obstacles:
visualise_grid(grid, 1, 4, 2, 5, obstacles)

#------------------------------------
# TEST CASE 2: No Obstacles Found

print(f"\n{'-'*48}\nTEST CASE 2: No Obstacles Found\n")

obstacles = query_obstacles(grid, 2, 4, 2, 4)

# Printing the indices retrieved (for reference):
print(f"\nObstacle Positions (size = {obstacles.size}):\n{obstacles}\n")

# Visualising the grid, cluster, and obstacles:
visualise_grid(grid, 2, 4, 2, 4, obstacles)