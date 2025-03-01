from .display_functionality import *

#================================================
# MAIN FUNCTION: CELL CORNER COORDINATES RETRIEVAL

def get_multiple_cell_corner_coords(positions: list[tuple[int]], cell_width: float, cell_length: float) -> np.ndarray:
    '''
    Gets the corner coordinates for multiple grid cells.
    
    ---

    PARAMETERS:
    - `positions` (list[tuple[int]]): (row, column) positions of cells
    - `cell_width` (float): Width of each cell
    - `cell_length` (float): Length of each cell

    RETURNS:
    - (np.ndarray): Array where each row contains the corner
      coordinates for a grid cell in the format:\n
      [x1, y1, x2, y2, x3, y3, x4, y4]
    '''
    corner_coords_list = []

    for position in positions:
        corners = [
            [position[1] * cell_width, position[0] * cell_length],  # Bottom-left
            [position[1] * cell_width + cell_width, position[0] * cell_length],  # Bottom-right
            [position[1] * cell_width + cell_width, position[0] * cell_length + cell_length],  # Top-right
            [position[1] * cell_width, position[0] * cell_length + cell_length]  # Top-left
        ]
        corner_coords_list.append(np.array(corners))

    return np.array(corner_coords_list)

#================================================
# TEST CASES

positions = [(2, 4), (1, 2), (3, 1)]  # Example grid positions
cell_width = 5.0
cell_length = 7.0

#================================================
# TEST PART 1: DISPLAY CORNER COORDINATES

corner_coords = get_multiple_cell_corner_coords(positions, cell_width, cell_length)
display_corner_coords(positions, corner_coords)

#================================================
# TEST PART 2: PLOT CORNER COORDINATES

plot_corner_coords(positions, corner_coords, cell_width, cell_length, annotate_corners=True)