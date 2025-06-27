import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

# NOTE: AABB = Axis-Aligned Bounding Box

#================================================
# VISUALISER

def plot_rectangle_with_aabb(corners):
    _, ax = plt.subplots()
    
    # Plot the original rectangle:
    polygon = Polygon(corners, closed=True, edgecolor='blue', fill=False, label="Original Rectangle")
    ax.add_patch(polygon)

    # Compute the AABB:
    x_coords, y_coords = zip(*corners)
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    # Plot the AABB:
    aabb = Rectangle(
        (min_x, min_y), max_x - min_x, max_y - min_y, 
        edgecolor='red', fill=False, linestyle='--', label="AABB")
    ax.add_patch(aabb)

    # Set plot limits and aspect ratio
    ax.set_xlim(min_x - 1, max_x + 1)
    ax.set_ylim(min_y - 1, max_y + 1)
    ax.set_aspect('equal', 'box')
    
    # Add legend and show plot
    plt.legend()
    plt.title("Rectangle and Axis-Aligned Bounding Box (AABB)")
    plt.show()

#================================================
# TEST CASE

# Define a rectangle with any orientation by specifying its vertices
# Example: 45-degree rotated rectangle centered at (2, 3)
width = 4
height = 2
center = np.array([2, 3])
angle_deg = 30  # Rotation in degrees

# Compute vertices of the rotated rectangle
angle_rad = np.radians(angle_deg)
rotation_matrix = np.array([
    [np.cos(angle_rad), -np.sin(angle_rad)],
    [np.sin(angle_rad), np.cos(angle_rad)]])

# Define rectangle corners before rotation (centered at origin):
base_corners = np.array(
    [[-width / 2, -height / 2],
     [width / 2, -height / 2],
     [width / 2, height / 2],
     [-width / 2, height / 2]])

# Rotate and shift to the center:
rotated_corners = np.dot(base_corners, rotation_matrix) + center

# Plot the rectangle and its axis-aligned bbox:
plot_rectangle_with_aabb(rotated_corners)
