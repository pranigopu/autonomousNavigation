from .core_functionality import *
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

#================================================
# TEST CASE
# NOTE: We shall be dealing with only rectangles here

#------------------------------------
# Generate random rectangles:
np.random.seed(0)
num_rectangles = 100
rectangles = []
for i in range(num_rectangles):
    center = np.random.rand(2) * 100
    width, height = np.random.rand(2) * 20 + 5
    angle = np.random.rand() * 360  # Random rotation
    rect = []
    for dx, dy in [(-width/2, -height/2), (width/2, -height/2),
                    (width/2, height/2), (-width/2, height/2)]:
        # Rotate and translate the rectangle points
        x = center[0] + dx * np.cos(np.radians(angle)) - dy * np.sin(np.radians(angle))
        y = center[1] + dx * np.sin(np.radians(angle)) + dy * np.cos(np.radians(angle))
        rect.append([x, y])
    rectangles.append((f"R{i}", np.array(rect)))

#------------------------------------
# Target rectangle (centered at [50, 50] with size [15, 25]):
target_corners = np.array([[42.5, 37.5], [57.5, 37.5], [57.5, 62.5], [42.5, 62.5]])

#------------------------------------
# Find overlapping rectangles:
overlapping_labels = detect_overlapping_figs(rectangles, target_corners)

#------------------------------------
# Visualisation
_, ax = plt.subplots(figsize=(10, 10))

# Plot all rectangles:
for label, rect in rectangles:
    polygon = Polygon(rect, closed=True, edgecolor='blue', fill=False, linewidth=1)
    ax.add_patch(polygon)
    # Annotate each rectangle:
    center = np.mean(rect, axis=0)
    ax.text(center[0], center[1], label, fontsize=8, ha='center')

# Highlight overlapping rectangles:
for label in overlapping_labels:
    rect = next(r[1] for r in rectangles if r[0] == label)
    polygon = Polygon(rect, closed=True, edgecolor='red', fill=False, linewidth=2)
    ax.add_patch(polygon)

# Plot the target rectangle:
polygon = Polygon(target_corners, closed=True, edgecolor='green', fill=False, linewidth=2)
ax.add_patch(polygon)
ax.text(50, 50, "Target", color='green', fontsize=12, ha='center')

plt.xlim(0, 100)
plt.ylim(0, 100)
plt.gca().set_aspect('equal', adjustable='box')
plt.title("Rectangle Overlap Visualization (Red = Overlapping, Green = Target)")
plt.show()

overlapping_labels
