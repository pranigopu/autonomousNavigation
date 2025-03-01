from .core_functionality import *
import matplotlib.pyplot as plt

#================================================
# VISUALISATION

def plot_rectangles(ax, rect1, rect2, title):
    '''Plot rectangles and display the overlap result.'''
    ax.plot(*np.append(rect1, [rect1[0]], axis=0).T, label="Rect 1")
    ax.plot(*np.append(rect2, [rect2[0]], axis=0).T, label="Rect 2")

    ax.legend()
    ax.axis('equal')
    ax.set_title(title)

#================================================
# TEST CASES
# NOTE: We are only dealing with rectangles/quadrilaterals here

#------------------------------------
# Define test cases with varying placements and rotations:
test_cases = [
    # Standard rectangles with overlap:
    (np.array([[1, 1], [4, 1], [4, 3], [1, 3]]),
     np.array([[2, 2], [5, 2], [5, 4], [2, 4]])),
    
    # Non-overlapping rectangles:
    (np.array([[1, 1], [3, 1], [3, 2], [1, 2]]),
     np.array([[5, 5], [7, 5], [7, 6], [5, 6]])),
    
    # Rotated rectangles with overlap:
    (np.array([[2, 2], [4, 1], [5, 3], [3, 4]]),
     np.array([[3, 2], [6, 2], [5, 5], [2, 4]])),
    
    # Touching corners:
    (np.array([[1, 1], [3, 1], [3, 3], [1, 3]]),
     np.array([[3, 3], [5, 3], [5, 5], [3, 5]])),
    
    # Large overlap:
    (np.array([[0, 0], [6, 0], [6, 4], [0, 4]]),
     np.array([[2, 1], [5, 1], [5, 3], [2, 3]]))]

#------------------------------------
# Plotting the test cases
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes = axes.flatten()

for idx, (rect1, rect2) in enumerate(test_cases):
    result = detect_overlap(rect1, rect2)
    title = f"Test {idx + 1}: {'Overlap' if result else 'No Overlap'}"
    plot_rectangles(axes[idx], rect1, rect2, title)

#------------------------------------
# Remove any unused axes:
for ax in axes[len(test_cases):]:
    ax.axis('off')

#------------------------------------
plt.tight_layout()
plt.show()
