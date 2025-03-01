from basic_grid_environment import *
from agent import *

#================================================
# CELL TYPE CHECK

#------------------------------------
def is_free_space(cell:tuple[int, int], free_space_symbol, grid:np.ndarray) -> bool:
    '''
    Checks if the cell is a free/open space or not.

    ---

    PARAMETERS:
    - `cell` (tuple[int, int]): Grid position of cell to be checked
    - `free_space_symbol` (Any): Symbol denoting free space within the grid
    - `grid` (np.ndarray): 2D array denoting the environment grid
    
    RETURNS:
    - (bool): Is free space or not
    '''
    
    try:
        return grid[cell[0], cell[1]] == free_space_symbol
    except IndexError:
        raise False

#------------------------------------
def is_permanent_obstacle(cell:tuple[int, int], permanent_obstacle_symbol, grid:np.ndarray) -> bool:
    '''
    Checks if the cell is a permanent obstacle or not.

    ---

    PARAMETERS:
    - `cell` (tuple[int, int]): Grid position of cell to be checked
    - `free_space_symbol` (Any): Symbol denoting permanent obstacle within the grid
    - `grid` (np.ndarray): 2D array denoting the environment grid
    
    RETURNS:
    - (bool): Is permanent obstacle or not
    '''
    
    try:
        return grid[cell[0], cell[1]] == permanent_obstacle_symbol
    except IndexError:
        return True

#------------------------------------
def is_temporary_obstacle(self, cell:tuple[int, int], temporary_obstacle_symbol, grid:np.ndarray) -> bool:
    '''
    Checks if the cell is a temporary obstacle or not.

    ---

    PARAMETERS:
    - `cell` (tuple[int, int]): Grid position of cell to be checked
    - `free_space_symbol` (Any): Symbol denoting temporary obstacle within the grid
    - `grid` (np.ndarray): 2D array denoting the environment grid
    
    RETURNS:
    - (bool): Is temporary obstacle or not
    '''
    
    try:
        return grid[cell[0], cell[1]] == temporary_obstacle_symbol
    except IndexError:
        return True

#------------------------------------
def is_obstacle(cell:tuple[int, int], obstacle_symbols:list, grid:np.ndarray) -> bool:
    '''
    Checks if the cell is an obstacle or not.

    ---

    PARAMETERS:
    - `cell` (tuple[int, int]): Grid position of cell to be checked
    - `obstacle_symbols` (list): List of symbols denoting obstacles within the grid
    - `grid` (np.ndarray): 2D array denoting the environment grid
    
    RETURNS:
    - (bool): Is obstacle or not
    '''
    
    try:
        return grid[cell[0], cell[1]] in obstacle_symbols
    except IndexError:
        return True
    
#------------------------------------
def get_free_space_positions(free_space_symbol, grid:np.ndarray) -> np.ndarray:
    '''
    Gets all free space positions in a grid.

    ---

    PARAMETERS:
    - `free_space_symbol` (Any): Symbol denoting free space within the grid
    - `grid` (np.ndarray): 2D array denoting the environment grid
    
    RETURNS:
    - (list[tuple[int, int]]): List of free space grid positions
    '''

    return np.argwhere(grid == free_space_symbol).tolist()

#================================================
# SURROUNDING CELL SEARCH

#------------------------------------
def get_open_neighbours(cell:tuple[int, int], obstacle_symbols:list, grid:np.ndarray) -> list[tuple[int, int]]:
    '''
    Gets the cell's open neighours.
     
    NOTE: "Open" => Into which movement is possible.

    ---

    PARAMETERS:
    - `cell` (tuple[int, int]): Cell denoting the current/referenced grid position
    - `obstacle_symbols` (list): List of symbols denoting obstacles in the grid
    - `grid` (np.ndarray): 2D grid denoting the grid environment

    RETURNS:
    - (list[tuple[int, int]]): List of grid positions of open neighbours
    '''
    
    neighbours = [
        (cell[0] + 1, cell[1]), # Up
        (cell[0], cell[1] - 1), # Left
        (cell[0] - 1, cell[1]), # Down
        (cell[0], cell[1] + 1)  # Right
    ]

    num_rows, num_columns = grid.shape

    open_neighbours = []
    for neighbour in neighbours:
        # Making sure the adjacent position is within bounds:
        if neighbour[0] >= num_rows or neighbour[0] < 0:
            continue
        if neighbour[1] >= num_columns or neighbour[1] < 0:
            continue
        # Making sure the adjacent position does not have an obstacle:
        if is_obstacle(neighbour, obstacle_symbols, grid):
            continue
        open_neighbours.append(neighbour)
    
    return open_neighbours

#------------------------------------
def get_open_neighbours_at_time_stamp(cell:tuple[int, int, int], obstacle_symbols:list, grid:np.ndarray, reservation_table:dict, do_include_current_cell_if_free=False) -> list[tuple[int, int, int]]:
    '''
    Gets the cell's open neighours (with time stamp) in time stamp.
    
    NOTE 1: Time stamp is contained in the 3rd dimension of `cell`.

    NOTE 2: "Open" => Into which movement is possible next time stamp.

    ---

    PARAMETERS:
    - `cell` (tuple[int, int, int]): Cell denoting the current/referenced grid position, along with time stamp as the 3rd dimension
    - `obstacle_symbols` (list): List of symbols denoting obstacles in the grid
    - `grid` (np.ndarray): 2D grid denoting the grid environment
    - `reservation_table` (dict): Table indicating reserved cells across time stamp; must be in the format:
        - Keys: (row index, column index, time stamp)
        - Items: Index of the agent which has reserved the above position in the above time stamp

    RETURNS:
    - (list[tuple[int, int]]): List of grid positions of open neighbours at time stamp `cell[2] + 1`
    
    ---

    A position is considered to be not open (even if it is free in the
    next time stamp) if either (1) a dynamic obstacle in the current
    time stamp swaps positions with the agent in the current cell in
    the next time stamp, or (2) if the vector of a dynamic obstacle
    across the current and next time stamps and the vector of the agent
    in the current cell across the current and next time stamp
    intersect (this would be a "cross-over"). Realistically, both cases
    would lead to collisions, despite the positions being "free" in the
    next time stamp.

    Currently, we are only checking for position swapping, which is a
    specific type of cross-over. For use-cases with strictly right-angle
    turns, this is sufficient. However, if we introduce turns in other
    angles, we need to also check for cross-overs to avoid collisions
    with dynamic obstacles; implementing this efficiently (without
    excessive loops) would require implementing more efficient data
    structures to store and retrieve data about reserved positions
    across time stamps.
    '''
    
    open_neighbours_with_time_stamp = []
    potentially_open_neighbours = get_open_neighbours(cell[:2], obstacle_symbols, grid)
    potentially_open_neighbours.append((cell[0], cell[1], cell[2] + 1))
    for pon in potentially_open_neighbours:
        reserving_agent_index = reservation_table.get((pon[0], pon[1], cell[2] + 1), None)
        
        # If the neighbour is free in the next time stamp:
        if reserving_agent_index is None:
            # Checking for position swapping (the dynamic obstacle and the agent at the current cell cannot realistically swap positions within 1 time step without colliding):
            # NOTE: TO DO (FUTURE): Logic to prevent cross-overs; currently, we are only checking for position swaps
            
            a = reservation_table.get((cell[0], cell[1], cell[2] + 1), None)
            b = reservation_table.get((pon[0], pon[1], cell[2]), None)
            
            # Add the free position as an open neighbour only if there is no position swapping:
            if a is None or b is None or a != b:
                open_neighbours_with_time_stamp.append((pon[0], pon[1], cell[2] + 1))
    
    # Remove current cell as an open cell if all neighbouring cells do not contain dynamic obstacles:
    if not do_include_current_cell_if_free and len(open_neighbours_with_time_stamp) == len(potentially_open_neighbours):
        open_neighbours_with_time_stamp.remove((cell[0], cell[1], cell[2] + 1))
    '''
    NOTE ON CONDITIONALLY REMOVING THE CURRENT CELL:
    The reservation table only informs about dynamic obstacles. If a
    potentially open position was removed due to a dynamic obstacle,
    only then does it make sense to also include the current cell, in
    case the agent finds it more beneficial to wait at the current cell
    rather than move to some other open cell. Note that this would be
    suboptimal when dealing with static obstacles, since we can expect
    only dynamic obstacles to move and give way later, not static ones.
    Hence, we want to enforce movement if no dynamic obstacles were
    found.
    '''
    return open_neighbours_with_time_stamp

#================================================
# HEURISTIC FUNCTIONS

#------------------------------------
def get_manhattan_distance(position:tuple[int, int], end_position:tuple[int, int]) -> int:
    '''
    Calculates and returns the Manhattan distance between two grid
    positions. Manhattan distance does not favour zig-zag paths to
    straighter paths, making it easier to add a turning cost on top of
    it to encourage straighter paths.

    ---

    PARAMETERS:
    - `position` (tuple[int, int]): Reference/current position
    - `end_position` (tuple[int, int]): End position

    RETURNS:
    - (int): Manhattan distance
    '''
    
    return abs(position[0] - end_position[0]) + abs(position[1] - end_position[1])

#------------------------------------
def get_euclidean_distance(position:tuple[int, int], end_position:tuple[int, int]) -> float:
    '''
    Calculates and returns the Euclidean distance between two grid
    positions. Euclidean distance minimises total distance between
    the start and end positions.

    ---

    PARAMETERS:
    - `position` (tuple[int, int]): Reference/current position
    - `end_position` (tuple[int, int]): End position

    RETURNS:
    - (float): Euclidean distance
    '''
    
    return np.sqrt((position[0] - end_position[0])**2 + (position[1] - end_position[1])**2)

#================================================
def is_adjacent(cell1:tuple[int, int], cell2:tuple[int, int]) -> bool:
    '''
    Checks if the 2 given cells are adjacent.

    ---

    PARAMETERS:
    - `cell1` (tuple[ints]): 1st cell position
    - `cell2` (tuple[ints]): 2nd cell position

    RETURNS:
    - (bool): Adjacent or not
    '''
    
    if cell1[0] == cell2[0] and abs(cell1[1] - cell2[1]) == 1:
        return True
    if cell1[1] == cell2[1] and abs(cell1[0] - cell2[0]) == 1:
        return True
    return False