from .core_functionality import *
import matplotlib.pyplot as plt

#================================================
# RANDOMISED RECTANGLE GENERATION
# NOTE: We are dealing only with rectangles for now

#------------------------------------
def rotate_rectangle(corners:np.ndarray, angle:float, center:np.ndarray) -> np.ndarray:
    '''Rotate rectangle corners around a center by a given angle (in radians).'''
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]])
    return np.dot(corners - center, rotation_matrix.T) + center

#------------------------------------
def generate_rectangle(center, width, length, angle=0):
    '''Generate rectangle given center, width, length, and rotation.'''
    half_width = width / 2
    half_length = length / 2

    # Define the rectangle corners before rotation:
    corners = np.array([
        [-half_width, -half_length],
        [half_width, -half_length],
        [half_width, half_length],
        [-half_width, half_length]]) + center

    # Apply rotation if needed:
    if angle != 0:
        corners = rotate_rectangle(corners, np.radians(angle), center)

    # Return the generated rectangle's corners:
    return corners

#================================================
# TEST CASES

# Generate k*k test cases:
k = 4
np.random.seed(42)
fig, axes = plt.subplots(k, k, figsize=(15, 15))

for i in range(k*k):
    # Random rectangle properties:
    center1 = np.random.uniform(2, 8, 2)
    center2 = np.random.uniform(2, 8, 2)
    width1, length1 = np.random.uniform(1, 4), np.random.uniform(1, 4)
    width2, length2 = np.random.uniform(1, 4), np.random.uniform(1, 4)
    angle1, angle2 = np.random.uniform(0, 180), np.random.uniform(0, 180)

    # Generate rectangles
    fig1 = generate_rectangle(center1, width1, length1, angle1)
    fig2 = generate_rectangle(center2, width2, length2, angle2)

    # Check for overlap:
    overlap = detect_overlap(fig1, fig2)

    # Plot rectangles:
    ax = axes[i // k, i % k]
    ax.plot(*np.append(fig1, [fig1[0]], axis=0).T, 'b', label="fig1")
    ax.plot(*np.append(fig2, [fig2[0]], axis=0).T, 'r', label="fig2")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')

    # Title indicating overlap status:
    ax.set_title(f"Overlap: {'Yes' if overlap else 'No'}")

plt.tight_layout()
plt.show()
