from .display_functionality import *

#================================================
# MAIN FUNCTION: CELL CORNER COORDINATES RETRIEVAL

def get_multiple_cell_corner_coords(positions:np.ndarray, cell_width:float, cell_length:float) -> np.ndarray:
    '''
    Gets the corner coordinates for multiple grid cells.
    
    ---

    PARAMETERS:
    - `positions` (np.ndarray): Positions of cells
        - 1st column: Row indices
        - 2nd column: Column indices
    - `cell_width` (float): Width of each cell
    - `cell_length` (float): Length of each cell

    RETURNS:
    - (np.ndarray): Array where each row contains the corner
      coordinates for a grid cell in the format:\n
      [x1, y1, x2, y2, x3, y3, x4, y4]
    '''

    return np.array([
        positions[:, 1] * cell_width, positions[:, 0] * cell_length,  # Bottom-left
        positions[:, 1] * cell_width + cell_width, positions[:, 0] * cell_length,  # Bottom-right
        positions[:, 1] * cell_width + cell_width, positions[:, 0] * cell_length + cell_length,  # Top-right
        positions[:, 1] * cell_width, positions[:, 0] * cell_length + cell_length  # Top-left
    ]).T

#================================================
# HELPER: INDEX PAIRS FOR A CELL CLUSTER (BASED ON GIVEN ROW AND COLUMN INDEX RANGES)

def get_positions_for_cells_in_cluster(i_1:int, i_2:int, j_1:int, j_2:int) -> np.ndarray:
    '''
    Gets an array of all pairs (i, j) for given ranges:
    - i_1:i_2 (for row indices)
    - j_1:j_2 (for column indices)

    ---
    
    PARAMETERS:
    - `i_1` (int): Start of the range for i (inclusive)
    - `i_2` (int): End of the range for i (exclusive)
    - `j_1` (int): Start of the range for j (inclusive)
    - `j_2` (int): End of the range for j (exclusive)

    RETURNS:
    - (np.ndarray): Array of shape (N, 2) where N = number of positions
    '''
    
    i_values = np.arange(i_1, i_2)
    j_values = np.arange(j_1, j_2)

    # Efficiently form all combinations using broadcasting:
    i_grid, j_grid = np.meshgrid(i_values, j_values, indexing='ij')
    pairs = np.stack([i_grid.ravel(), j_grid.ravel()], axis=-1)
    return pairs

#================================================
# TEST CASES

i_1, i_2 = 0, 3
j_1, j_2 = 2, 6
print(f"\nRow Range: [{i_1}, {i_2}), Column Range: [{j_1}, {j_2})\n")
positions = get_positions_for_cells_in_cluster(i_1, i_2, j_1, j_2)  # Example grid positions
print(f"\nShape of Positions Array: {positions.shape}\n")
cell_width = 5.0
cell_length = 7.0

#================================================
# TEST PART 1: DISPLAY CORNER COORDINATES

corner_coords = get_multiple_cell_corner_coords(positions, cell_width, cell_length)
print(f"\nCorner Coordinate Array:\n{corner_coords}\n")
display_corner_coords(positions, corner_coords)

#================================================
# TEST PART 2: PLOT CORNER COORDINATES

plot_corner_coords(positions, corner_coords, cell_width, cell_length)