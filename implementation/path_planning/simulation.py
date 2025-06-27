from os import system, name
from time import sleep
from sys import stdout, argv
from multi_agent_manager import *
from pandas import DataFrame

def get_agent_symbols(agent_indices:list[int]) -> dict:
    # Define agent symbols for presentation:
    agent_symbols = {}
    for i, agent_index in enumerate(agent_indices):
        if i < 26:
            agent_symbols[agent_index] = chr(ord('A') + i)
        elif i < 52:
            agent_symbols[agent_index] = chr(ord('a') + i - 26)
        else:
            agent_symbols[agent_index] = chr(ord('0') + i - 52)
    
    return agent_symbols

#############################################################
# TEST CASE DEFINITIONS
#############################################################

# TEST CASE 1: A*

def test_a_star(end_position, start_position, manager:MultiAgentManager, time_step_size=0.5):
    path = manager.a_star(end_position, start_position, 0)
    
    print(f"OBTAINED PATH:\n{path}\n")
    
    # Duplicating the grid to modify it:
    grid = environment.grid.copy()
    
    # Adding path position markers to the grid:
    for position in path:
        grid[position[0], position[1]] = '*'

    # Defining color map:
    color_map = {
        environment.free_space_symbol: COLORS["blue"],
        environment.permanent_obstacle_symbol: COLORS["red"],
        environment.temporary_obstacle_symbol: COLORS["yellow"],
        '*': COLORS["yellow"],
        'O': COLORS["green"]
    }

    # Displaying environment as text:
    print("\nENVIRONMENT GRID\n")
    environment.display_grid_as_text(grid, color_map)

    # Running real-time:
    user_input = input("Enter y to continue with real-time simulation...\n")
    grid = environment.grid.copy()
    previous_position = None
    if user_input == 'y':
        total_time_elapsed = time_step_size
        for current_position in path:
            system(clear_command)
            print('RUNNING THE SIMULATION\n\nO => Robot\n* => Path Trail')
            grid[current_position[0], current_position[1]] = 'O'
            if not (previous_position is None):
                grid[previous_position[0], previous_position[1]] = '*'
            previous_position = current_position
            environment.display_grid_as_text(grid, color_map)
            stdout.write(f'\rTime elapsed: {total_time_elapsed}')
            sleep(time_step_size)
            total_time_elapsed += time_step_size
    print("\n\nSimulation Ended\n")

#================================================
# TEST CASE 2: CA* WITH FIXED PRIORITY OR WINDOWED AND EQUAL SPEED

def test_equal_speed_ca_star_one_path_per_agent(paths, start_positions, end_positions, agents, agent_indices, agent_symbols, time_step_size=0.5):
    # Display agent paths:
    print("\nINTENDED PATHS:\n")
    for i in range(len(start_positions)):
        print(f"{start_positions[i]} --> {end_positions[i]}")
    print('-' * 48)
    
    # Show obtained paths:
    print("\n\nOBTAINED PATHS:\n")
    for agent_index, path in zip(agent_indices, paths):
        print(f"\nPATH FOR AGENT {agent_symbols[agent_index]}\n{path}\n")
    print('-' * 48)

    # Show agents for which paths were and were not found:
    print("\n\nSUCCESSFUL AND FAILED AGENTS:\n")
    successful_agent_indices, failed_agent_indices = [], []
    for i in range(len(paths)):
        if paths[i] == []:
            failed_agent_indices.append(i)
        else:
            successful_agent_indices.append(i)
    print(f"Successful agents (paths were found for these):\n{[agent_symbols[i] for i in successful_agent_indices]}\n")
    print(f"Failed agents (no paths were found for these):\n{[agent_symbols[i] for i in failed_agent_indices]}\n")
    print('-' * 48)
        
    # Duplicating the grid to modify it:
    grid = environment.grid.copy()

    # Defining color map:
    color_map = {
        environment.free_space_symbol: COLORS["blue"],
        environment.permanent_obstacle_symbol: COLORS["red"],
        environment.temporary_obstacle_symbol: COLORS["red"],
        '*': COLORS["bright_blue"]
    }
    # Coloring the agents:
    color_choices = [
        "green",
        "white",
        "magenta",
        "bright_black",
        "yellow",
        "bright_red",
        "bright_green",
        "bright_yellow",
        "bright_magenta",
        "bright_white"]
    for i in agent_indices:
        color_map[agent_symbols[i]] = COLORS[color_choices[i % len(color_choices)]]

    # Displaying environment as text:
    print("\nENVIRONMENT GRID\n")
    environment.display_grid_as_text(grid, color_map)

    # Running real-time:
    user_input = input("Enter y to continue with real-time simulation...\n")
    reached_agents_indices = []
    reached_agents_symbols = []
    timings = []
    if user_input == 'y':
        t, total_time_elapsed = 0, time_step_size
        while True:
            system(clear_command)
            print("RUNNING THE SIMULATION\n\n('*' = Goal position of agent which has reached its goal; may be regarded as free space)\n\n")
            grid = environment.grid.copy()
            for i in successful_agent_indices:
                try:
                    agents[i].position = paths[i][t][:2]
                    grid[agents[i].position[0], agents[i].position[1]] = agent_symbols[agent_indices[i]]
                except IndexError:
                    if not (i in reached_agents_indices):
                        reached_agents_indices.append(i)
                        reached_agents_symbols.append(agent_symbols[i])
                        timings.append(total_time_elapsed)
                    if grid[agents[i].position[0], agents[i].position[1]] == environment.free_space_symbol:
                        grid[agents[i].position[0], agents[i].position[1]] = '*'
            environment.display_grid_as_text(grid, color_map)
            stdout.write(f"\rTime elapsed: {total_time_elapsed}\n\n")
            if len(reached_agents_symbols) > 0:
                stdout.write(f"Agents who reached their goal:\n{", ".join(reached_agents_symbols)}")
            
            sleep(time_step_size)
            total_time_elapsed += time_step_size
            t += 1
            
            if len(reached_agents_indices) == len(successful_agent_indices):
                break
    print("\n\nSimulation Ended\n")
    print('-' * 48)

    print("TIMINGS:\n")
    agent_symbols_data = []
    start_positions_data = []
    end_positions_data = []
    timings_data = []
    for reached_agent, timing in zip(reached_agents_indices, timings):
        agent_symbols_data.append(agent_symbols[reached_agent])
        start_positions_data.append(start_positions[reached_agent])
        end_positions_data.append(end_positions[reached_agent])
        timings_data.append(timing)
    print(
        DataFrame(
            data={
                "Agent": agent_symbols_data,
                "Start": start_positions_data,
                "End": end_positions_data,
                "Timing": timings_data
            }
        )
    )
    print()

#================================================
# TEST CASE 3: CA* EQUAL SPEED ONGOING SIMULATION

def test_equal_speed_ca_star_ongoing(paths, agents, agent_indices, agent_symbols, time_step_size=0.5):
    # Duplicating the grid to modify it:
    grid = environment.grid.copy()
    
    # Defining color map:
    color_map = {
        environment.free_space_symbol: COLORS["blue"],
        environment.permanent_obstacle_symbol: COLORS["red"],
        environment.temporary_obstacle_symbol: COLORS["red"],
        '*': COLORS["bright_blue"]
    }
    # Coloring the agents:
    color_choices = [
        "green",
        "white",
        "magenta",
        "bright_black",
        "yellow",
        "bright_red",
        "bright_green",
        "bright_yellow",
        "bright_magenta",
        "bright_white"]
    for i in agent_indices:
        color_map[agent_symbols[i]] = COLORS[color_choices[i % len(color_choices)]]

    # Displaying environment as text:
    print("\nENVIRONMENT GRID\n")
    environment.display_grid_as_text(grid, color_map)

    # Running real-time:
    user_input = input("Enter y to continue with real-time simulation...\n")
    timings = []
    if user_input == 'y':
        t, total_time_elapsed = 0, time_step_size
        while True:
            system(clear_command)
            print("RUNNING THE SIMULATION\n\n('*' = Goal position of agent which has reached its goal; regarded as free space)\n\n")
            grid = environment.grid.copy()
            for i in agent_indices:
                try:
                    agents[i].position = paths[i][t][:2]
                    grid[agents[i].position[0], agents[i].position[1]] = agent_symbols[agent_indices[i]]
                except IndexError:
                    if grid[agents[i].position[0], agents[i].position[1]] == environment.free_space_symbol:
                        grid[agents[i].position[0], agents[i].position[1]] = '*'
            environment.display_grid_as_text(grid, color_map)
            stdout.write(f"\rTime elapsed: {total_time_elapsed}\n\n")
            
            sleep(time_step_size)
            total_time_elapsed += time_step_size
            t += 1
    
#############################################################
# RUNNING TEST CASES
#############################################################

test_case = argv[1]
if name == "nt":
    clear_command = "cls"
else:
    clear_command = "clear"

#================================================
# A*

if test_case == "a_star":
    environment = BasicGridEnvironment()
    environment.generate_random_grid()
    agent = Agent(horizontal_movement_limit=environment.grid.shape[0], vertical_movement_limit=environment.grid.shape[1])
    manager = MultiAgentManager([agent], environment)
    test_a_star((10, 11), (0, 0), manager, 0.5)

#================================================
# CA* FIXED PRIORITIES EQUAL SPEED FIXED VALUES

if test_case == "fixed_priorities_equal_speed_ca_star":
    environment = BasicGridEnvironment(10, 20, prng_seed=3)
    environment.generate_random_grid()
    a, b = environment.grid.shape
    agents = [
        Agent(a, b),
        Agent(a, b),
        Agent(a, b),
        Agent(a, b)
    ]
    start_positions = [
        (0, 0),
        (10, 15),
        (7, 5),
        (17, 4),
    ]
    end_positions = [
        (10, 15),
        (0, 0),
        (0, 1),
        (5, 5)
    ]
    # NOTE: The order in which agent indices were given determines agent priorities
    manager = MultiAgentManager(agents, environment)
    agent_indices = list(range(len(agents)))
    paths, agents = manager.fixed_priority_equal_speed_ca_star(end_positions, start_positions, agent_indices)
    agent_symbols = get_agent_symbols(agent_indices)
    test_equal_speed_ca_star_one_path_per_agent(paths, start_positions, end_positions, agents, agent_indices, agent_symbols, 0.5)

#================================================
# CA* FIXED PRIORITIES EQUAL SPEED RANDOMISED VALUES

if test_case == "fixed_priorities_equal_speed_ca_star_randomised":
    try:
        num_agents = int(argv[2])
    except IndexError:
        num_agents = 3
    environment = BasicGridEnvironment(10, 20, prng_seed=3)
    environment.generate_random_grid()
    free_space_positions = np.argwhere(environment.grid == environment.free_space_symbol).tolist()

    prng_seed = 5
    rand = np.random.RandomState(seed=prng_seed)

    agents = []
    start_positions = []
    end_positions = []
    for i in range(num_agents):
        # Create a new agent:
        agents.append(Agent(a, b))
        
        # Setting random start and end positions (making sure the end position is not the same as the start):
        start_position = tuple(free_space_positions[rand.randint(0, len(free_space_positions))])
        end_position = start_position
        while start_position == end_position:
            end_position = tuple(free_space_positions[rand.randint(0, len(free_space_positions))])
        
        # To make sure no other agent is given the same start position:
        free_space_positions.remove(list(start_position))

        # Add start and end positions for agent:
        start_positions.append(start_position)
        end_positions.append(end_position)
    
    manager = MultiAgentManager(agents, environment)
    agent_indices = list(range(len(agents)))
    paths, agents = manager.fixed_priority_equal_speed_ca_star(end_positions, start_positions, agent_indices)
    agent_symbols = get_agent_symbols(agent_indices)
    test_equal_speed_ca_star_one_path_per_agent(paths, start_positions, end_positions, agents, agent_indices, agent_symbols, 1)

#================================================
# WINDOWED CA* EQUAL SPEED

if test_case == "windowed_equal_speed_ca_star":
    try:
        num_agents = int(argv[2])
    except IndexError:
        num_agents = 3
    try:
        reprioritisation_approach = argv[3]
    except IndexError:
        reprioritisation_approach = "randomised"
    try:
        window_size = int(argv[4])
    except IndexError:
        window_size = 10
    
    environment = BasicGridEnvironment(10, 20, prng_seed=3)
    environment.generate_random_grid()
    free_space_positions = np.argwhere(environment.grid == environment.free_space_symbol).tolist()

    prng_seed = 6
    rand = np.random.RandomState(seed=prng_seed)

    agents = []
    start_positions = []
    end_positions = []
    for i in range(num_agents):
        # Create a new agent:
        agents.append(Agent(environment.grid.shape[0], environment.grid.shape[1]))
        
        # Setting random start and end positions (making sure the end position is not the same as the start):
        start_position = tuple(free_space_positions[rand.randint(0, len(free_space_positions))])
        end_position = start_position
        while start_position == end_position:
            end_position = tuple(free_space_positions[rand.randint(0, len(free_space_positions))])
        
        # To make sure no other agent is given the same start position:
        free_space_positions.remove(list(start_position))

        # Add start and end positions for agent:
        start_positions.append(start_position)
        end_positions.append(end_position)
    
    manager = MultiAgentManager(agents, environment)
    agent_indices = list(range(len(agents)))
    paths, agents = manager.windowed_equal_speed_ca_star_v1(end_positions, start_positions, agent_indices, window_size=window_size, reprioritisation_approach=reprioritisation_approach)
    agent_symbols = get_agent_symbols(agent_indices)
    test_equal_speed_ca_star_one_path_per_agent(paths, start_positions, end_positions, agents, agent_indices, agent_symbols, 1)

#================================================
# WINDOWED CA* EQUAL SPEED

if test_case == "windowed_equal_speed_ca_star_variable_window_size":
    try:
        num_agents = int(argv[2])
    except IndexError:
        num_agents = 3
    try:
        window_size = int(argv[3])
    except IndexError:
        window_size = 10
    
    environment = BasicGridEnvironment(10, 20, prng_seed=3)
    environment.generate_random_grid()
    free_space_positions = np.argwhere(environment.grid == environment.free_space_symbol).tolist()

    prng_seed = 6
    rand = np.random.RandomState(seed=prng_seed)

    agents = []
    start_positions = []
    end_positions = []
    for i in range(num_agents):
        # Create a new agent:
        agents.append(Agent(environment.grid.shape[0], environment.grid.shape[1]))
        
        # Setting random start and end positions (making sure the end position is not the same as the start):
        start_position = tuple(free_space_positions[rand.randint(0, len(free_space_positions))])
        end_position = start_position
        while start_position == end_position or end_position in end_positions:
            end_position = tuple(free_space_positions[rand.randint(0, len(free_space_positions))])
        
        # To make sure no other agent is given the same start position:
        free_space_positions.remove(list(start_position))

        # Add start and end positions for agent:
        start_positions.append(start_position)
        end_positions.append(end_position)
    
    manager = MultiAgentManager(agents, environment)
    agent_indices = list(range(len(agents)))
    paths, agents = manager.windowed_equal_speed_ca_star_v2(end_positions, start_positions, agent_indices, window_size=window_size)
    agent_symbols = get_agent_symbols(agent_indices)
    test_equal_speed_ca_star_one_path_per_agent(paths, start_positions, end_positions, agents, agent_indices, agent_symbols, 1)

#================================================
# WINDOWED CA* EQUAL SPEED ONGOING

if test_case == "windowed_equal_speed_ca_star_ongoing":
    try:
        num_agents = int(argv[2])
    except IndexError:
        num_agents = 3
    try:
        window_size = int(argv[3])
    except IndexError:
        window_size = 10
    
    environment = BasicGridEnvironment(10, 20, prng_seed=3)
    environment.generate_random_grid()

    agents = [Agent(environment.grid.shape[0], environment.grid.shape[1]) for _ in range(num_agents)]    
    manager = MultiAgentManager(agents, environment)
    agent_indices = list(range(len(agents)))
    paths, agents = manager.windowed_equal_speed_ca_star_v3(agent_indices, window_size=window_size, num_time_steps_before_return=5, prng_seed=10)
    agent_symbols = get_agent_symbols(agent_indices)
    test_equal_speed_ca_star_ongoing(paths, agents, agent_indices, agent_symbols, 1)
