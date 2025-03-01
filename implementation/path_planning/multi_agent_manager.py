from agent import *
class MultiAgentManager:
    def __init__(self, agents:list[Agent], environment:BasicGridEnvironment):
        self.agents = agents
        self.environment = environment
    
    #================================================
    def get_agent(self, agent_index):
        try:
            return self.agents[agent_index]
        except IndexError:
            raise Exception(f"Only {len(self.agents)} agents are available, but requested agent index was {agent_index}")

    #================================================
    # BASIC A* IMPLEMENTATION
    # NOTE: This is mainly for testing the simulation framework initially

    def a_star(self, end_position, start_position, agent_index) -> list[tuple[int, int]]:
        from algorithm_a_star import a_star
        return a_star(end_position, start_position, self.get_agent(agent_index), self.environment)

    #================================================
    # FIXED PRIORITY EQUAL SPEED CA* IMPLEMENTATION

    def fixed_priority_equal_speed_ca_star(self, end_positions, start_positions, agent_indices=None) -> tuple[list[tuple[int, int, int]], list[Agent]]:
        from algorithm_fixed_priority_equal_speed_ca_star import fixed_priority_equal_speed_ca_star
        if agent_indices is None:
            agents = self.agents
        else:
            agents = [self.get_agent(agent_index) for agent_index in agent_indices]
        return fixed_priority_equal_speed_ca_star(end_positions, start_positions, agents, self.environment), agents

    #================================================
    # WINDOWED EQUAL SPEED CA* IMPLEMENTATION

    def windowed_equal_speed_ca_star_one_path_per_agent(self, end_positions, start_positions, agent_indices=None, window_size=10, reprioritisation_approach="randomised") -> tuple[list[tuple[int, int, int]], list[Agent]]:
        from algorithm_windowed_equal_speed_ca_star_one_path_per_agent import windowed_equal_speed_ca_star_one_path_per_agent
        if agent_indices is None:
            agents = self.agents
        else:
            agents = [self.get_agent(agent_index) for agent_index in agent_indices]
        return windowed_equal_speed_ca_star_one_path_per_agent(end_positions, start_positions, agents, self.environment, window_size=window_size, reprioritisation_approach=reprioritisation_approach), agents
