from .core_functionality import *
import matplotlib.pyplot as plt

# NOTE: "Figure" denotes either a straight-edged polygon or a straight edge.

#================================================
# TEST CASE

#------------------------------------
# Example figure definitions (rectangles, in our case):
fig1_coords = np.array([[2, 2], [4, 3], [3, 5], [1, 4]])
fig2_coords = np.array([[3, 3], [5, 2], [6, 4], [4, 5]])

#------------------------------------
# Check overlap and plot:
overlap = detect_overlap(fig1_coords, fig2_coords)

#------------------------------------
# Plot the 2 figures and show whether they overlap:

#............
_, ax = plt.subplots()

#............
# Plot the first figure:
fig1 = np.vstack([fig1_coords, fig1_coords[0]])  # Close the figure
ax.plot(fig1[:, 0], fig1[:, 1], 'b', label="Figure 1")

#............
# Plot the second figure:
fig2 = np.vstack([fig2_coords, fig2_coords[0]])
ax.plot(fig2[:, 0], fig2[:, 1], 'r', label="Figure 2")

#............
# Indicate overlap status:
ax.set_title(f"Overlap: {'Yes' if overlap else 'No'}")

#............
ax.legend()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()