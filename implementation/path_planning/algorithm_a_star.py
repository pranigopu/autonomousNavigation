from queue import PriorityQueue
from helpers import *

#================================================
# HELPER: Reconstruction of path based on end position and data on visited nodes

def reconstruct_path(end_position:tuple[int, int], visited:dict) -> list[tuple[int, int]]:
    '''
    Reconstructs path from end position and data on visited nodes.

    ---

    PARAMETERS:
    - `end_position` (tuple[int, int]): End position of the path
    - `visited` (dict): Dictionary containing data on visited nodes in the following format:
        - Keys: Grid Position (tuple[int, int])
        - Items: A list of the format:
            ```
            [
                heuristic cost,
                previous position (from existing best path),
                total cost = heuristic + path cost
            ]
            ```
    '''
    
    # Initialising path:
    current_position = tuple(end_position)
    path = [current_position]
    current_position = visited[current_position][1]

    # Reconstructing path:
    while visited[current_position][1] != current_position:
        path.insert(0, current_position)
        current_position = visited[current_position][1]

    # Inserting the starting position to the front of the path:
    path.insert(0, visited[current_position][1])
    return path

#================================================
# HELPER: Check for turn/change in direction around current node in path

def detect_direction_change(next_position, current_position, previous_position) -> bool:
    '''
    Detects direction change around current node in path.

    ---

    PARAMETERS:
    - `next_position` (tuple[int, int]): Next position in path (maybe proposed)
    - `current_position` (tuple[int, int]): Current position in path
    - `previous_position` (tuple[int, int]): Previous position in path

    RETURNS:
    - (bool): Direction change detected (True) or not (False)
    '''
    
    previous_to_current_direction = (current_position[0] - previous_position[0], current_position[1] - previous_position[1])
    current_to_next_direction = (next_position[0] - current_position[0], next_position[1] - current_position[1])

    return not (current_to_next_direction == previous_to_current_direction)

#================================================
# MAIN: A* algorithm

def a_star(end_position:tuple[int, int], start_position:tuple[int, int], agent:Agent, environment:BasicGridEnvironment, heuristic_cost=get_manhattan_distance, penalise_turns=True) -> list[tuple[int, int]]:
    '''
    A* pathfinding function.
    
    Pathfinds from `start_position` to `end_position`; `start_position`
    is assigned as `agent.position` if given as "agent" in the arguments.
    
    ---

    PARAMETERS:
    - `end_position` (tuple[int, int]): Position to be reached/approached
    - `start_position` (tuple[int, int]): Agent start position; if given as "agent", defaults to `agent.position`
    - `agent` (Agent): Navigating agent
    - `environment` (BasicGridEnvironment): Environment to navigate within
    - `heuristic` (function, optional): Heuristic cost function used
    - `penalise_turns` (bool, optional): Add turning cost or not

    RETURNS:
    - (list[tuple[int, int]]): Path
    '''
    
    #------------------------------------
    # Assigning start position if not already given:
    if start_position == "agent":
        start_position = agent.position
    
    #------------------------------------
    # Goal test, in case we have already fulfilled the pathfinding requirements:
    if start_position == end_position:
        return [start_position]

    #------------------------------------
    # Initialising the data storage of visited nodes:
    visited = {}
    '''
    This will contain important data on visited nodes

    ---

    INTENDED FORMAT OF ITEMS:
    - Keys: Grid Position (tuple[int, int])
    - Items: A list of the format:
        ```
        [
            heuristic cost,
            previous position (from existing best path),
            total cost = heuristic + path cost
        ]
        ```
    '''
    # Defining constants to refer to the respective indices of the `visited` dictionaries items; this is for enhancing code readability:
    HEURISTIC, PREVIOUS_POSITION, TOTAL_COST = range(3)
    # Small helper for enhancing readability:
    def get_empty_entry_for_visited() -> list[None]:
        return [None] * 3
    # Initialising the first entry of `visited`:
    h = heuristic_cost(start_position, end_position)
    visited[start_position] = get_empty_entry_for_visited()
    visited[start_position][HEURISTIC] = h
    visited[start_position][PREVIOUS_POSITION] = start_position
    visited[start_position][TOTAL_COST] = h
    # NOTE: Total cost for the starting point is the heuristic cost itself, since path cost is 0

    #------------------------------------
    # Initialising the frontier data structure:
    frontier = PriorityQueue()
    frontier.put((h, start_position, 0))
    '''
    INTENDED FORMAT OF ELEMENTS:
    (
        priority = heuristic cost + path cost,
        node's grid position,
        path cost 
    )

    NOTE 1: Path cost => Cost of the best existing path to the node.

    NOTE 2: For origin node, path cost is 0.
    
    ---
    
    NOTE ON PriorityQueue:
    
    This is a class that implements the priority queue data structure.
    Items are ordered (by default in ascending order) based on the
    values or (in case of tuple items) the value of the item's first
    element of the tuple.
    '''

    #------------------------------------
    # Exploring the frontier until it is empty...
    
    while not frontier.empty():
        # Get highest priority path to explore next:
        _, current_position, path_cost = frontier.get()
        
        # Goal test:
        if current_position == end_position:
            return reconstruct_path(current_position, visited)
        
        # If goal not reached, explore neighbours:
        open_neighbour_positions = get_open_neighbours(current_position, [environment.permanent_obstacle_symbol, environment.temporary_obstacle_symbol], environment.grid)
        for neighbour_position in open_neighbour_positions:
            # Calculate the heuristic:
            # NOTE: If already visited, we will not recalculate the heuristic; it is a good practice, especially when scaling up
            try:
                h = visited[neighbour_position][HEURISTIC]
            except KeyError:
                h = heuristic_cost(neighbour_position, end_position)

            #____________
            # Define the transition cost:

            previous_position = visited[current_position][PREVIOUS_POSITION]

            # CASE 1: Neighbour is along the same axis as the previous and current position:
            if penalise_turns and previous_position != current_position and not detect_direction_change(neighbour_position, current_position, previous_position):
                transition_cost = 1
            # CASE 2: Neighbour is adjacent to the current position but not necessarily along the same axis:
            elif is_adjacent(current_position, neighbour_position):
                transition_cost = 2
            # CASE 3: Neighbour is diagonal to the current position:
            else:
                transition_cost = 3

            #____________
            # Calculate the total cost (h + g, where g now is path_cost + transition_cost):
            new_total_cost = h + path_cost + transition_cost
            
            #____________
            # Add this neighouring position to the priority queue if one of the two condition are fulfilled:
            # 1. If the positions have never been visited before
            # 2. If the new path found to this position has a lower total cost than the previous one
            if not (neighbour_position in visited) or visited[neighbour_position][TOTAL_COST] > new_total_cost: # NOTE: Refer to the intended format of the items
                frontier.put((new_total_cost, neighbour_position, path_cost + transition_cost))
                # NOTE: The above line adds a new path to the list of cost-wise sorted paths
                
                # Update stored data for `neighbour_position`:
                visited[neighbour_position] = get_empty_entry_for_visited()
                visited[neighbour_position][HEURISTIC] = h
                visited[neighbour_position][PREVIOUS_POSITION] = current_position
                visited[neighbour_position][TOTAL_COST] = new_total_cost
                '''
                NOTE: For `neighbour_position`, the above lines either...
                1. ... update heuristic, previous position and total costs
                (given that the newly found path to it is less costly)
                OR
                2. ... create heuristic, previous position and total costs
                (given that it was previously unvisited)
                '''
    return []