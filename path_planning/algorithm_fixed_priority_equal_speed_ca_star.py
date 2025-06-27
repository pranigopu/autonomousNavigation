from algorithm_a_star_across_time import a_star_across_time
from helpers import *
from tqdm import tqdm

def fixed_priority_equal_speed_ca_star(end_positions:list[tuple[int]], start_positions:list[tuple[int]], agents:list[Agent], environment:BasicGridEnvironment, heuristic_cost=get_manhattan_distance, penalise_turns=True, do_get_reservation_table=False) -> list[tuple[int, int, int]] | tuple[list[tuple[int, int, int]], dict]:
    '''
    CA* that cooperatively navigates `agents` under these constraints:
    - Priorities are fixed (here, by the ordering in the given list)
    - Agents move at equal speeds (measured in grid cells / time step) \n
      NOTE: For simplicity and since it can be scaled, speed = 1 cell/time step

    ---

    PARAMETERS:
    - `end_positions` (list[tuple[int]]): List of end positions; end position i corresponds to agent i
    - `start_positions` (list[tuple[int]]): List of start positions; start position i corresponds to agent i
    - `agents` (list[Agent]): Navigating agents \n
      NOTE: Agent indices in this list indicate their priority, with index 0 indicating the highest priority
    - `environment` (BasicGridEnvironment): Environment to navigate within
    - `heuristic` (function, optional): Heuristic cost function used
    - `penalise_turns` (bool, optional): Add turning cost or not
    - `reservation_table` (dict): Table indicating reserved cells across time stamps; must be in the format:
        - Keys: (row index, column index, time stamp)
        - Items: Index of the agent which has reserved the above position in the above time stamp
    
    RETURNS:
    - (list[list[tuple[int, int, int]]]): List of cooperative paths, each corresponding to an agent
        - 1st element: Row index
        - 2nd element: Column index
        - 3rd element: Time stamp
    - (dict, optional): Reservation table

    ---

    NOTE: The time step size is not given as a parameter as the integer
    time steps used here can easily be scaled up or down as needed to
    fit the desired time step size. Furthermore, using integer time 
    stamps within the logic and stored data reduces memory overhead. 
    '''

    paths = []
    
    # Initialisation:
    reservation_table = {}
    max_path_length = 0
    
    # Running the CA* algorithm:
    for i in tqdm(range(len(agents))):
        path = a_star_across_time(end_positions[i], start_positions[i], agents[i], environment, heuristic_cost, penalise_turns, reservation_table)
        max_path_length = max(max_path_length, len(path))
        paths.append(path)
        for position_with_time_stamp in path:
            reservation_table[position_with_time_stamp] = i
    
    # If reservation table must also be returned (for reference):
    if do_get_reservation_table:
        return paths, reservation_table
    # If reservation table need not be returned, just return the paths found:
    return paths

#############################################################
# TESTING
#############################################################

if __name__ == "__main__":
    environment = BasicGridEnvironment(prng_seed=2)
    environment.generate_random_grid()
    a, b = environment.grid.shape
    agents = [
        Agent(a, b),
        Agent(a, b),
        #Agent((0, 0), a, b)
    ]
    start_positions = [
        (0, 0),
        (10, 15)
    ]
    end_positions = [
        (10, 15),
        (0, 0)
    ]
    paths, reservation_table = fixed_priority_equal_speed_ca_star(start_positions, end_positions, agents, environment, do_get_reservation_table=True)
    from pandas import DataFrame
    for i, path in enumerate(paths):
        print(f"\nPATH {i + 1}\n{path}\n")
    print('-'*48)
    print(DataFrame(data={"key": reservation_table.keys(), "value": reservation_table.values()}))