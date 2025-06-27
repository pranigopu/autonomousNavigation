import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Create a figure and axis
fig, ax = plt.subplots()
xdata, ydata = [], []

# Initialise the agents' positions:
num_agents = 2
positions = np.random.rand(num_agents, 2) * 10  # Random initial positions within a 10x10 grid

# Scatter plot for agent positions:
scat = ax.scatter(xdata, ydata)

# Update function for animation:
def update(frame):
    global positions
    xdata, ydata = positions.T
    scat.set_offsets(positions)
    
    # Update agent positions randomly:
    movement = np.random.uniform(-0.5, 0.5, size=positions.shape)
    positions += movement
    positions = np.clip(positions, 0, 10) # Keep agents within the bounded area

    return scat,

# Set up plot boundaries:
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Create the animation:
ani = animation.FuncAnimation(fig, update, frames=200, interval=100, blit=True)

plt.show()
