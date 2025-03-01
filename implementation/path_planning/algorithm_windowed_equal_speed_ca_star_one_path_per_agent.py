from algorithm_a_star_across_time import a_star_across_time
from helpers import *

#================================================
# HELPER: Reprioritisation

VALID_REPRIORITISATION_APPROACHES = ["randomised", "round_robin"]

def reprioritise(agent_indices:list[int], reprioritisation_approach:str):
    '''
    Reorders agent indices to represent a rearrangement in the order of
    agent reservation priorities; hence, represents reprioritisation.
    
    ---

    - `agent_indices` (list[int]): Indices of the agents whose selection order (i.e. reservation order) is to be rearranged
    - `reprioritisation_approach` (str): Reprioritisation method to be used per window
        - "randomised": Randomised reprioritisation
        - "round_robin": Round-Robin reprioritisation 
    '''
    
    if reprioritisation_approach == "randomised":
        return np.random.choice(agent_indices, size=len(agent_indices), replace=False)
    elif reprioritisation_approach == "round_robin":
        if len(agent_indices) > 2:
            return agent_indices[len(agent_indices)] + agent_indices[1:len(agent_indices)] + agent_indices[0]
        agent_indices.reverse()
        return agent_indices
    raise Exception(f"Reprioritisation approach \"{reprioritisation_approach}\" is invalid: should be one of {VALID_REPRIORITISATION_APPROACHES}")

#================================================
# MAIN: Windowed equal speed CA* (one path per agent)

def windowed_equal_speed_ca_star_one_path_per_agent(end_positions:list[tuple[int]], start_positions:list[tuple[int]], agents:list[Agent], environment:BasicGridEnvironment, heuristic_cost=get_manhattan_distance, penalise_turns:bool=True, do_get_reservation_table:bool=False, window_size:int=10, reprioritisation_approach:str="randomised") -> list[tuple[int, int, int]] | tuple[list[tuple[int, int, int]], dict]:
    '''
    CA* that cooperatively navigates `agents` under these constraints:
    - Priorities are set per time window (we can either reorder them or keep them fixed)
    - Each agent has exactly one start-and-end positions pair
    - An agent that has reached its end position disappears (i.e. it is no longer considered as a part of the grid)
    - Agents move at equal speeds (measured in grid cells / time step) \n
      NOTE: For simplity + since it can be scaled, speed = 1 cell/time step

    ---

    PARAMETERS:
    - `end_positions` (list[tuple[int]]): List of end positions; end position i corresponds to agent i
    - `start_positions` (list[tuple[int]]): List of start positions; start position i corresponds to agent i
    - `agents` (list[Agent]): Navigating agents \n
      NOTE: Agent indices in this list indicate their priority, with index 0 indicating the highest priority
    - `environment` (BasicGridEnvironment): Environment to navigate within
    - `heuristic` (function, optional): Heuristic cost function used
    - `penalise_turns` (bool, optional): Add turning cost or not
    - `reservation_table` (dict, optional): Table indicating reserved cells across time stamps; must be in the format:
        - Keys: (row index, column index, time stamp)
        - Items: Index of the agent which has reserved the above position in the above time stamp
    - `reprioritisation_approach` (str, optional): Reprioritisation method to be used per window
        - "randomised": Randomised reprioritisation
        - "round_robin": Round-Robin reprioritisation 
        
    RETURNS:
    - (list[list[tuple[int, int, int]]]): List of cooperative paths, each corresponding to an agent
    - (dict, optional): Reservation table

    ---

    NOTE: The time step size is not given as a parameter as the integer
    time steps used here can easily be scaled up or down as needed to
    fit the desired time step size. Furthermore, using integer time 
    stamps within the logic and stored data reduces memory overhead. 
    '''

    paths = []

    # Initialisation:
    paths = [[]] * len(agents)
    agent_indices = list(range(len(agents)))
    
    # Running the CA* algorithm:
    while len(agent_indices) > 0:

        # Reservation table and counters reset every window:
        reservation_table = {}

        # Reprioritise:
        indices = reprioritise(agent_indices, reprioritisation_approach)
        k = 0
        while k < len(indices):
            i = int(indices[k]) # For better presentation, since otherwise, it is going to be displayed as `np.int64(...)`
            path = a_star_across_time(end_positions[i], start_positions[i], agents[i], environment, heuristic_cost, penalise_turns, reservation_table)
            if len(path) >= window_size:
                start_positions[i] = path[window_size - 1][:2]
            else:
                '''
                Happens when the path is smaller than the window (which means it
                can also happen if the path is empty). Hence, if this exception
                is caught, it means either (1) the agent has reached its goal
                within the window or (2) the agent has failed to reach its goal
                and is stationary.
                '''
                agent_indices.remove(i)
                if path != []:
                    start_positions[i] = path[-1][:2]
            path = path[:window_size - 1] # We subtract window size by 1 because we do not want to duplicate the end of the path, which is going to be the start of the next path
            paths[i] = paths[i] + path
            
            # Updating the reservation table for this window:
            time_stamp, max_time_stamp, j = path[0][2], path[-1][2], 1
            while time_stamp <= window_size and time_stamp < max_time_stamp:
                time_stamp = path[j][2]
                reservation_table[path[j]] = i
                j += 1
            
            k += 1

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
    paths, reservation_table = windowed_equal_speed_ca_star_one_path_per_agent(start_positions, end_positions, agents, environment, do_get_reservation_table=True)
    from pandas import DataFrame
    for i, path in enumerate(paths):
        print(f"\nPATH {i + 1}\n{path}\n")
    print('-'*48)
    print(DataFrame(data={"key": reservation_table.keys(), "value": reservation_table.values()}))