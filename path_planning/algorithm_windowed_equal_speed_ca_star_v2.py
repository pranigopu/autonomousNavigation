from algorithm_a_star_across_time import a_star_across_time
from helpers import *

#================================================
# MAIN: Windowed equal speed CA* (one path per agent)

def windowed_equal_speed_ca_star_v2(end_positions:list[tuple[int]], start_positions:list[tuple[int]], agents:list[Agent], environment:BasicGridEnvironment, heuristic_cost=get_manhattan_distance, penalise_turns:bool=True, window_size:int=10) -> list[tuple[int, int, int]]:
    '''
    CA* that cooperatively navigates `agents` under these constraints:
    - Priorities are set per time window (we can either reorder them or keep them fixed)
    - Each agent has exactly one start-and-end positions pair
    - An agent that has reached its end position disappears (i.e. it is no longer considered as a part of the grid)
    - Agents move at equal speeds (measured in grid cells / time step) \n
      NOTE: For simplicity and since it can be scaled, speed = 1 cell/time step

    ---

    PARAMETERS:
    - `end_positions` (list[tuple[int]]): List of end positions; end position i corresponds to agent i
    - `start_positions` (list[tuple[int]]): List of start positions; start position i corresponds to agent i
    - `agents` (list[Agent]): Navigating agents
    - `environment` (BasicGridEnvironment): Environment to navigate within
    - `heuristic` (function, optional): Heuristic cost function used
    - `penalise_turns` (bool, optional): Add turning cost or not
        
    RETURNS:
    - (list[list[tuple[int, int, int]]]): List of cooperative paths, each corresponding to an agent
        - 1st element: Row index
        - 2nd element: Column index
        - 3rd element: Time stamp

    ---

    NOTE: The time step size is not given as a parameter as the integer
    time steps used here can easily be scaled up or down as needed to
    fit the desired time step size. Furthermore, using integer time 
    stamps within the logic and stored data reduces memory overhead. 
    
    ---

    POSSIBLE OPTIMISATION:

    We could optimise the resetting of the window size for the next
    planning iteration by setting it as the size of the smallest path
    length among the agents who have not yet reached their goals. But
    for simplicity, this optimisation is avoided in this implementation.
    '''

    paths = []
    start_positions = start_positions.copy()
    # NOTE: We are copying start positions as we shall be modifying this list later; copying prevents unexpected changes to the original list

    #------------------------------------
    # Initialisation:
    paths = [[] for _ in range(len(agents))]
    agent_indices = list(range(len(agents)))
    initial_window_size = window_size
    path_lengths = [1] * len(agent_indices)
    completed_agents = []
    
    #------------------------------------
    # Running the CA* algorithm:
    while len(completed_agents) < len(agents):
        # Reservation table and counters reset every window:
        reservation_table = {}
        sort_values(agent_indices, path_lengths)
        previous_indices = []
        path_lengths = []
        paths_in_window = []
        window_size = initial_window_size
        just_completed_agents = []
        
        #________________________
        # Loop through the agents for the next time window:
        k = 0
        while k < len(agent_indices):
            i = int(agent_indices[k]) # `int` is applied for better presentation, since otherwise, it is going to be displayed as `np.int64(...)`
            k += 1

            #............
            # PATHFINDING

            # Pathfinding (cooperatively for time steps within the window, non-cooperatively for the rest of the time steps):
            path = a_star_across_time(end_positions[i], start_positions[i], agents[i], environment, heuristic_cost, penalise_turns, reservation_table)
            
            # I do not want to deal with empty paths for now:
            if path == []:
                raise Exception(f"No path found for agent ID {i}; retry pathfinding in a new environment/with new start and end points")
            
            # Storing the path length for sorting the agents accordingly next time:
            path_lengths.append(len(path))
            
            #............
            # SETTING NEXT STARTING POINT AND ADJUSTING WINDOW SIZE IF NECESSARY

            if len(path) >= window_size:
                start_positions[i] = path[window_size - 1][:2]
            elif len(path) > 1:
                '''
                Happens when the path is smaller than the window but not equal to 1
                (path length equalling 1 means the agent is stationary, which means
                it had already reached its goal in the previous planning iteration).
                Hence, if this else-block is reached, it means the agent has
                reached its goal within the window.

                ---

                NOTE: If path length is equal to 1, it means the agent is stationary,
                which means it reached its goal in the previous planning iteration
                and was thus prioritised for the next (i.e. current) planning
                iteration over the agents that are still moving in the current
                iteration.
                '''

                start_positions[i] = path[-1][:2]

                # Adjusting the window size to a smaller size:
                window_size = len(path)

                # Trimming window-specific paths for previous (higher-priority) agents according to new window size:
                # NOTE: This ensures that higher-priority agents do not unintentionally collide with this stationary agent
                for previous_k, previous_i in enumerate(previous_indices):
                    try:
                        start_positions[previous_i] = paths_in_window[previous_k][window_size - 1][:2]
                    except IndexError:
                        start_positions[previous_i] = paths_in_window[previous_k][-1][:2]
                    paths_in_window[previous_k] = paths_in_window[previous_k][:window_size - 1]

            #............
            # CHECKING WHICH AGENTS HAVE JUST COMPLETED THEIR PATHS

            if len(path) < window_size and not (i in completed_agents):
                just_completed_agents.append(i)
            
            #............
            # UPDATING RESERVATION TABLE FOR CURRENT TIME WINDOW

            # Reserving path positions:
            time_stamp, max_time_stamp, j = path[0][2], path[-1][2], 1
            while time_stamp <= window_size and time_stamp < max_time_stamp:
                time_stamp = path[j][2]
                reservation_table[path[j]] = i
                j += 1

            # Reserving stationary position across time (if agent has stopped due to path completion of pathfinding failure):            
            # NOTE: This ensures that lower priority agents consider the stationary position of this agent within this time window
            if j == len(path):
                j = -1
            while time_stamp <= window_size:
                reservation_table[(path[j][0], path[j][1], time_stamp)] = i
                time_stamp += 1
            
            #------------------------------------
            # SETTING WINDOW-SPECIFIC PATH

            path = path[:window_size - 1] # We trim the path by subtracting window size by 1, because we do not want to duplicate the end of the path, which is going to be the start of the next path
            '''
            NOTE: It is VERY CRUCIAL to trim the path AFTER reserving the agent
            path positions, including the last position. Why? Consider: why do
            we trim the path? Not because the agent is not going to be in the
            last position of its path, but precisely because it IS going to be
            in the last position of its path and must use this as a starting
            point for the next pathfinding iteration. This means we need to
            reserve this position first, and then remove it before the next
            iteration so that we do not duplicate this position for the agent.

            ALTERNATIVELY, for this implementation, we can simply trim each
            path in the following loop where we append the current window's
            paths to the agents' existing path.
            '''
            paths_in_window.append(path)
            previous_indices.append(i)
        
        #________________________
        # Append the window-specific paths to the overall paths of the agents:
        for k, path_in_window in enumerate(paths_in_window):
            i = agent_indices[k]
            if not (i in completed_agents):
                paths[i].extend(path_in_window)
                '''
                Using `.extend` is functionally equivalent to:
                ```
                paths[i] = paths[i] + path_in_window
                ```
                
                However, list extension using `.extend` is more efficient than list
                concatenation, because it does not create a new list and copy the
                elements of both lists into it. Rather, it merely modifies an
                existing list in-place. Hence, if...

                - N = `len(paths[i])`
                - K = `len(path_in_window)`

                ... then we have that:
                
                - Concatenation has the time complexity of O(N + K)
                - Extension has the time complexity of O(K)
                '''
            if i in just_completed_agents:
                completed_agents.append(i)

    #------------------------------------
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
    ]
    start_positions = [
        (0, 0),
        (10, 15)
    ]
    end_positions = [
        (10, 15),
        (0, 0)
    ]
    paths, reservation_table = windowed_equal_speed_ca_star_v2(start_positions, end_positions, agents, environment)
    for i, path in enumerate(paths):
        print(f"\nPATH {i + 1}\n{path}\n")
