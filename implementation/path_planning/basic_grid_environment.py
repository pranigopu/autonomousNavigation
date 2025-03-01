import numpy as np

# EXTRA FEATURE: ANSI escape codes for better grid presentation
COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bright_black": "\033[90m", # Gray
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "bright_white": "\033[97m",
    "reset": "\033[0m" # Resets color back to default
}

class BasicGridEnvironment:
    '''
    Basic grid environment for testing multi-agent pathfinding
    functions; this is strictly a square-celled grid, for simplicity.
    '''
    
    def __init__(self, grid_length_in_meters=10, grid_length_in_cells=20, prng_seed=None):
        '''
        PARAMETERS:
        - `grid_length_in_meters`: Length of the square grid in meters
        - `grid_length_in_cells`: Number of cells making a side of the square grid

        DEFAULT VALUES:
        - 10 m x 10 m warehouse
        - Obstacle grid = Warehouse divided into 20 square cells
        
        NOTE: Why 20? To make the minimum obstacle-forming unit 1/2 meter, which seems reasonable.
        '''

        self.grid_length_in_meters = grid_length_in_meters
        self.grid_length_in_cells = grid_length_in_cells
        self.cell_length_in_meters = grid_length_in_meters / grid_length_in_cells

        '''
        NOTE ON ROBOT SIZE: We take the robot size to be the same as cell
        length in meters. Hence, to handle this program's functionality for
        a differently sized robot, change the above parameters so that cell
        length in meters matches.
        '''

        self.free_space_symbol = '.'
        self.permanent_obstacle_symbol = '#'
        self.temporary_obstacle_symbol = '+'
        self.grid = np.array([[self.free_space_symbol] * self.grid_length_in_cells] * self.grid_length_in_cells)

        # Creating a PRNG with the specified seed (if any) for ensuring replicability of randomised grid:
        self.prng = np.random.RandomState(seed=prng_seed)

    #================================================
    def generate_random_grid(self, p:float=0.05):
        '''
        Generating random grid (an optional way to create an environment).

        ---

        PARAMETERS:
        - `p` (float): Probability of creating an obstacle at a given position
        '''

        for i in range(self.grid_length_in_cells):
            for j in range(self.grid_length_in_cells):
                if self.grid[i, j] == self.permanent_obstacle_symbol: # This may be encountered, since we are creating obstacles that stretch beyond the current position
                    continue

                # Creating an obstacle with a chance of `p`:
                if self.prng.rand() < p:
                    # Generating a boxy obstacle of a random size:
                    k, K = i, i + self.prng.randint(self.grid_length_in_cells // 10, self.grid_length_in_cells // 5)
                    l, L = j, j + self.prng.randint(self.grid_length_in_cells // 10, self.grid_length_in_cells // 5)
                    while l < L and l < self.grid_length_in_cells:
                        while k < K and k < self.grid_length_in_cells:
                            self.grid[k, l] = self.permanent_obstacle_symbol
                            k += 1
                        k = i
                        l += 1

    #================================================
    # GRID DISPLAY
    
    def display_grid_as_text(self, grid:np.ndarray=None, color_map:dict={}):
        '''
        Displays the grid as text.

        ---

        PARAMETERS:
        - `grid` (np.ndarray, optional): Grid
            - Defaults to `.grid` if given as `None`
            - Allows for displaying modified or custom grids

        ---

        NOTE ON REVERSE ORDER OF ROWS IN DISPLAY:
        Displaying the grid in a text/terminal-based form. Observe that
        the rows are printed backwards. This is because the environment
        is taken as a grid/coordinate space with the origin at the
        bottom left-most corner. Hence, to match this conception with the
        grid indices, the rows are printed backwards, with the first row
        displayed at the bottom and index (0, 0) displayed at the bottom
        left-most corner.

        NOTE: This conception of the space was enforced to match the coordinate system implicit in the assignment.
        '''

        if grid is None:
            grid = self.grid

        for i in range(grid.shape[0] - 1, -1, -1):
            for j in range(grid.shape[1]):
                key = grid[i, j]
                color = color_map.get(key, COLORS["yellow"])
                print(f"{color}{key}{COLORS["reset"]}", end=' ')
            print()
    
    #================================================
    # COORDINATES AND GRID POSITION MAPPING

    #------------------------------------
    # Conversion between coordinates (in meters) and grid cells:
    # NOTE 1: Coordinates are defined in meters, with the (0, 0) being at the bottom left-most
    # NOTE 2: x-axis <=> columns, y-axis <=> rows
    def grid_to_coord(self, cell:tuple[int]) -> tuple[float]:
        '''
        Returns the midpoint coordinates of the cell.

        ---

        PARAMETERS:
        - `cell` (tuple[int]): Grid position of the cell (row, column)
    
        RETURNS
        - (tuple[float]): Coordinates of the cell's midpoint
        ---

        NOTE ON RETURNING THE MIDPOINT:
        It is essential to work with the midpoints of cells rather than
        their bottom left corners (which would be the case if we did not
        add `self.cell_length_in_meters / 2` to both coordinates) as it
        ensures that when the robot is made to navigate to a grid cell,
        it actually navigates to the grid cell itself and not an adjacent
        cell (which would happen if the robot tried to navigate to the
        corner coordinates of the cell). Before ensuring the midpoint was
        returned, the robot was observed to oscillate between two cells
        adjacent to the desired cell in certain instances (e.g. when the
        robot had to backtrack and explore less traversed cells).
        '''

        x = cell[1] * self.cell_length_in_meters + self.cell_length_in_meters / 2
        y = cell[0] * self.cell_length_in_meters + self.cell_length_in_meters / 2
        return (x, y)
    
    #------------------------------------
    def coord_to_grid(self, coord:tuple[float]) -> tuple[int]:
        '''
        Returns to grid position corresponding to the coordinates.

        ---

        PARAMETERS:
        - `coord` (tuple[float]): Coordinates

        RETURNS:
        - (tuple[int]): Grid position of the cell containing the given coordinates
        '''
        
        return int(coord[1] / self.cell_length_in_meters), int(coord[0] / self.cell_length_in_meters)

#############################################################
# TESTING
#############################################################

if __name__ == "__main__":
    environment = BasicGridEnvironment(10, 20, 2)
    environment.generate_random_grid()
    environment.display_grid_as_text()