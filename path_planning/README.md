<h1>PATH PLANNING</h1>

---

# About
Contains code for single and multi-agent path planning.

Key algorithms:

- A\*
- Cooperative A\* (CA\*) (extends A\* to a multi-agent context)
- Windowed CA\* (WCA\*) (extends CA\* to ensure window-wise replanning)
- Dynamic window-size WCA\* (extends WCA\* to ensure dynamic window resizing \[1\])

\[1\] *This lets higher priority agents account for stationary lower priority agents.*

---

> **Key theoretical reference**: [*Cooperative A\**, **Autonomous Navigation**, **pranigopu.github.io**](https://pranigopu.github.io/autonomous-navigation/cooperative-a-star.html)

# Contents
**Base classes**:

- [`agent.py`](./agent.py): <br> *Defines `Agent` class for agent representation*
- [`basic_grid_environment.py`](./basic_grid_environment.py): *Defines `BasicGridEnvironment` for environment representation*

**Algorithms**:

- [`algorithm_a_star.py`](./algorithm_a_star.py): <br> *Basic A\* implementation*
- [`algorithm_a_star_across_time.py`](./algorithm_a_star_across_time.py): *Important for CA\**
- [`algorithm_fixed_priority_equal_speed_ca_star.py`](./algorithm_fixed_priority_equal_speed_ca_star.py): <br> *Fixed priority CA\* implementation*
- [`algorithm_windowed_equal_speed_ca_star_v1.py`](./algorithm_windowed_equal_speed_ca_star_v1.py): <br> *WCA\* implementation*
- [`algorithm_windowed_equal_speed_ca_star_v2.py`](./algorithm_windowed_equal_speed_ca_star_v2.py): <br> *Dynamic window size WCA\* implementation*

**Others**:

- [`helpers.py`](./helpers.py): *Defines core functionality common across source codes*
- [`multi_agent_manager.py`](./multi_agent_manager.py): *Defines interface to handle multi-agent navigation*
- [`simulation.py`](./simulation.py): *Defines simulation test cases to run*
