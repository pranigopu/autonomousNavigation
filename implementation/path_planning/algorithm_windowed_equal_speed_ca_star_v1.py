from algorithm_a_star_across_time import a_star_across_time, a_star
from helpers import *

#================================================
# HELPER: Get abstract distance

def get_abstract_distance(end_position:tuple[int, int], start_position:tuple[int, int], agent:Agent, environment:BasicGridEnvironment, heuristic_cost=get_manhattan_distance, penalise_turns=True) -> int|float:
    '''
    Gets the length of the abstract path between 2 positions.

    NOTE: Abstract path => Path not considering other agents

    ---

    PARAMETERS:
    - `end_position` (tuple[int]): Position to be reached/approached
    - `start_position` (tuple[int]): Agent start position; if given as "agent", defaults to `agent.position`
    - `agent` (Agent): Navigating agent
    - `environment` (BasicGridEnvironment): Environment to navigate within
    - `heuristic` (function, optional): Heuristic cost function used
    - `penalise_turns` (bool, optional): Add turning cost or not
    
    RETURNS:
    - (int|float): Length of the abstract path

    ---

    FUTURE OPTIMISATIONS:

    1.
    This function could leverage data structures that store abstract
    distances (i.e. abstract path lenths) that may be precalculated or
    calculated across time.

    2.
    This function could use the reverse resumable A* approach mentioned
    in "Cooperative Pathfinding" by David Silder (academic paper) to
    calculate abstract distances on demand.
    '''
    
    abstract_path = a_star(end_position, start_position, agent, environment, heuristic_cost, penalise_turns)
    return len(abstract_path)

#================================================
# HELPER: Reprioritisation

VALID_REPRIORITISATION_APPROACHES = ["randomised", "round_robin", "shortest_abstract_path_first"]

def reprioritise(agent_indices:list[int], reprioritisation_approach:str, end_positions:list[tuple[int, int]]=None, start_positions:list[tuple[int, int]]=None, agents:list[Agent]=None, environment:BasicGridEnvironment=None):
    '''
    Reorders agent indices to represent a rearrangement in the order of
    agent reservation priorities; hence, represents reprioritisation.
    
    ---

    PARAMETERS:
    - `agent_indices` (list[int]): Indices of the agents whose selection order (i.e. reservation order) is to be rearranged
    - `reprioritisation_approach` (str): Reprioritisation method to be used per window
        - "randomised": Randomised reprioritisation
        - "round_robin": Round-Robin reprioritisation
        - "shortest_abstract_path_first": Shortest abstract path reprioritisation
    '''

    agent_indices = agent_indices.copy()
    '''
    NOTE: Copying the agent indices list is super important! This is
    because in reprioritisation, we are going to be altering the list
    of agent indices, and in some reprioritisation approaches, this
    alteration is done in-place. Hence, if the same list pointer is
    used, there is a risk of unexpected changes to the list of
    reprioritised agent indices and/or the original list of agent
    indices due to operations in this function or in the windowed CA*
    function.
    '''
    
    if reprioritisation_approach == "randomised":
        return np.random.choice(agent_indices, size=len(agent_indices), replace=False)
    elif reprioritisation_approach == "round_robin":
        if len(agent_indices) > 2:
            return agent_indices[len(agent_indices)] + agent_indices[1:len(agent_indices)] + agent_indices[0]
        agent_indices.reverse()
        return agent_indices
    elif reprioritisation_approach == "shortest_abstract_path_first":
        if len(agent_indices) == 1:
            return agent_indices
        abstract_distances = []
        for agent_index in agent_indices:
            abstract_distances.append(get_abstract_distance(end_positions[agent_index], start_positions[agent_index], agents[agent_index], environment))
        sort_values(agent_indices, abstract_distances, order=0)
        return agent_indices
    
    raise Exception(f"Reprioritisation approach \"{reprioritisation_approach}\" is invalid: should be one of {VALID_REPRIORITISATION_APPROACHES}")

#================================================
# MAIN: Windowed equal speed CA* (one path per agent)

def windowed_equal_speed_ca_star_v1(end_positions:list[tuple[int]], start_positions:list[tuple[int]], agents:list[Agent], environment:BasicGridEnvironment, heuristic_cost=get_manhattan_distance, penalise_turns:bool=True, window_size:int=10, reprioritisation_approach:str="randomised") -> list[tuple[int, int, int]]:
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
    - `reprioritisation_approach` (str, optional): Reprioritisation method to be used per window
        - "randomised": Randomised reprioritisation
        - "round_robin": Round-Robin reprioritisation
        
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
    '''

    paths = []
    start_positions = start_positions.copy()
    # NOTE: We are copying start positions as we shall be modifying this list later; copying prevents unexpected changes to the original list

    # Initialisation:
    paths = [[] for _ in range(len(agents))]
    agent_indices = list(range(len(agents)))
    
    # Running the CA* algorithm:
    while len(agent_indices) > 0:

        # Reservation table and counters reset every window:
        reservation_table = {}

        # Reprioritise:
        indices = reprioritise(agent_indices, reprioritisation_approach, end_positions, start_positions, agents, environment)
        
        # Loop through the agents for the next time window:
        k = 0
        while k < len(indices):
            i = int(indices[k]) # `int` is applied for better presentation, since otherwise, it is going to be displayed as `np.int64(...)`
            k += 1

            path = a_star_across_time(end_positions[i], start_positions[i], agents[i], environment, heuristic_cost, penalise_turns, reservation_table)
            if len(path) >= window_size:
                start_positions[i] = path[window_size - 1][:2]
            else:
                '''
                Happens when the path is smaller than the window (which means it
                can also happen if the path is empty). Hence, if this else-block
                is reached, it means either (1) the agent has reached its goal
                within the window or (2) the agent has failed to reach its goal
                and is stationary.
                '''
                agent_indices.remove(i)
                if path != []:
                    start_positions[i] = path[-1][:2]
            
            # Updating the reservation table for this window:
            time_stamp, max_time_stamp, j = path[0][2], path[-1][2], 1
            while time_stamp <= window_size and time_stamp < max_time_stamp:
                time_stamp = path[j][2]
                reservation_table[path[j]] = i
                j += 1
            
            # Filling out the reservation table with the agent's last position (if the agent has stopped) for the remaining time stamps within the window:
            # NOTE: This ensures that lower priority agents consider the stationary position of this agent within this time window
            if j == len(path):
                j = -1
            while time_stamp <= window_size:
                reservation_table[(path[j][0], path[j][1], time_stamp)] = i
                time_stamp += 1

            path = path[:window_size - 1] # We subtract window size by 1 because we do not want to duplicate the end of the path, which is going to be the start of the next path
            '''
            NOTE: It is VERY CRUCIAL to trim the path AFTER reserving the agent
            path positions, including the last position. Why? Consider: why do
            we trim the path? Not because the agent is not going to be in the
            last position of its path, but precisely because it IS going to be
            in the last position of its path and must use this as a starting
            point for the next pathfinding iteration. This means we need to
            reserve this position first, and then remove it before the next
            iteration so that we do not duplicate this position for the agent.
            '''
            paths[i] = paths[i] + path
                
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
    paths, reservation_table = windowed_equal_speed_ca_star_v1(start_positions, end_positions, agents, environment, do_get_reservation_table=True)
    for i, path in enumerate(paths):
        print(f"\nPATH {i + 1}\n{path}\n")