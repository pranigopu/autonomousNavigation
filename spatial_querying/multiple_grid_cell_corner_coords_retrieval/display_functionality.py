import numpy as np
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt

#================================================
def display_corner_coords(positions, corner_coords):
    data = {"Cell": [], "P1": [], "P2": [], "P3": [], "P4": []}
    for i, coords in enumerate(corner_coords):
        data["Cell"].append(positions[i])
        coords = coords.reshape(4, 2).tolist() # The reshaping is done just in case; it is not always necessary
        for i in range(4):
            data[f"P{i + 1}"].append(coords[i])
    display(pd.DataFrame(data=data))

#================================================
def plot_corner_coords(positions, corner_coords, cell_width, cell_length, env_width_in_cells=8, env_length_in_cells=8, annotate_corners=False):
    _, ax = plt.subplots(figsize=(8, 6))

    # Plot each grid cell and its corner labels:
    for (position, coords) in zip(positions, corner_coords):
        # Reshape to 2D coordinates for plotting:
        corners = coords.reshape(4, 2)
        polygon = plt.Polygon(corners, edgecolor='blue', fill=False)
        ax.add_patch(polygon)

        # Annotate the corners:
        if annotate_corners:
            for i, (x, y) in enumerate(corners):
                ax.text(x, y, f"P{i + 1}", fontsize=10, ha='center', color='darkred')
        
        # Center label for the cell:
        center_x = position[1] * cell_width + cell_width / 2
        center_y = position[0] * cell_length + cell_length / 2
        ax.text(center_x, center_y, f"{position}", ha='center', va='center', color='black')

    # Grid and axis labels:
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_aspect('equal', 'box')

    env_width = cell_width * env_width_in_cells
    env_length = cell_length * env_length_in_cells
    ax.set_xticks(np.arange(0, env_width, cell_width))
    ax.set_yticks(np.arange(0, env_length, cell_length))
    ax.set_xlim(0, env_width)
    ax.set_ylim(0, env_length)
    ax.grid()
    plt.title("Grid Cell Visualisation with Corner Labels")
    plt.show()