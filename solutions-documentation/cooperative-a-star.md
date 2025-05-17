<h1>COOPERATIVE A* (CA*)</h1>

---

**Contents**:

- [Motivation for CA\*](#motivation-for-ca)
- [Motivation for understanding CA\* conceptually](#motivation-for-understanding-ca-conceptually)
- [Overview of CA\*](#overview-of-ca)
- [Key considerations in implementing CA\*](#key-considerations-in-implementing-ca)
  - [Search space definition accounting for time](#search-space-definition-accounting-for-time)
  - [Allowing for waiting and backtracking](#allowing-for-waiting-and-backtracking)
  - [Limiting wait time](#limiting-wait-time)
  - [Stopping search](#stopping-search)
  - [Accounting for collisions](#accounting-for-collisions)
- [Technical considerations in implementing CA\*](#technical-considerations-in-implementing-ca)
  - [Implementing reservation table](#implementing-reservation-table)
  - [Standardising speed representation using integer time steps](#standardising-speed-representation-using-integer-time-steps)
- [Fixed-priority equal speed CA\*](#fixed-priority-equal-speed-ca)

---

# Motivation for CA\*
See the following resources:

- ["The Problem with A\*", _Cooperative Pathfinding_ by David Silver](https://cw.fel.cvut.cz/b211/_media/courses/b3m33mkr/coop-path-aiwisdom.pdf)
- ["Why CA\*?", _Multi-Agent Path Planning_, `ideation`](../ideation/multi-agent-path-planning.md#why-ca)

# Motivation for understanding CA\* conceptually
A conceptual solution:

- Integrates a range of specific contexts; thus, is generalisable
- Enables the recognition of essentials and broader purposes
    - Keeps focus simple when implementing solutions
    - Allows us to set purposeful and effective goals

---

The same applies for the conceptual solution for CA\*. In particular, the conceptual solution for CA\* allows us to see what is the essential functionality that makes CA\* effective, and what is the essential structure of the algorithm that can then be understood in and translated to implementations. This is important, especially when implementing less optimised versions of CA\*, because grasping the essentials also helps us see the fundamental limitations and potential extensions of the core logic itself, thereby leading to a clearer grasp of a more optimised implementation.

# Overview of CA\*
_Consider a grid environment divided into equally-sized cells._

At each time step, each agent $A_i$ reserves a position for the next $k_i$ time steps. The agent with the highest priority reserves its position(s) without taking other agents into account for these $k$ time steps. At any given time step, agents with lower priorities search for open neighbours in the next time step (open neighbours are cells allowing movement and avoiding collisions with static obstacles and other agents); static obstacles are avoided by referring to the grid environment itself, and agents with higher priorities are avoided by referring to the reservation table. Each agent reserves its positions before agents with lower priorities, while accounting for agents with higher priorities.

Now, I have mentioned $k_i$ time steps for an agent $A_i$. Here, $k_i$ can be interpreted based on the implementation. In an implementation that reassigns agent priorities after a fixed window of time steps, $k_i$ is equal for all $i$ and represents the window size. In an implementation that fixes priorities at the start and does not change them, $k_i$ is the number of time steps $A_i$ needs to complete its path.

_The algorithm for CA\* is otherwise very similar to A\*._

# Key considerations in implementing CA\*
## Search space definition accounting for time
Unlike A\* (which is a single-agent algorithm), a node in the algorithm's search space is not merely a position but a position _with_ a time stamp (i.e. a value indicating the number of time steps that have passed since some starting point). Hence, a position explored at a later time stamp is distinct from the same position explored at an earlier time stamp. This has some significant implications in the nature of the algorithm's progression:

- Re-expanding a previously explored nodes involves:
    - Moving to another path in space (like A\*)
    - Shifting to another (past or future) time stamp
- Due to the inclusion of time stamps, a position can be:
    - Validly revisited/backtracked to
    - Maintained across time stamps (e.g. the agent can "wait")

## Allowing for waiting and backtracking
It is important to allow the agent to backtrack to previous positions at later time stamps, or to allow the agent to wait at the same position across time stamps, in order to accommodate/give way to dynamic obstacles (e.g. other agents) without moving around unnecessarily. However, to this end, it is important to identify an obstacle as static or dynamic; if it is possible to stay in the same position across time stamps when a static obstacle is encountered, an agent may simply freeze if neighbouring cells are further away from the goal, but the ability to stay in the same position across time stamps when a dynamic obstacle is encountered can prevent unnecessary movement, since a dynamic obstacle can be expected to give way later and let the agent continue in an efficient path.

## Limiting wait time
Even though the ability to wait for dynamic obstacles to pass is valuable, it may be necessary to introduce a limit to how much an agent can wait, so that, in case a dynamic obstacle (e.g. another agent) stays in one place for an unexpectedly long duration (e.g. in a realistic use-case, due to a vehicle breakdown or time-consuming work at a location), the agent is not held in place for an indefinite or unnecessary amount of time.

## Stopping search
Since every time stamp makes the same position a part of a new node in the algorithm's search space, the algorithm on its own cannot realise whether the positions have been searched exhaustively enough to conclude if no path can be found. Some ways to mitigate this are: (1) limit the number of time steps for which the agent is allowed to search for a path, (2) run a parallel logic that checks for positions irrespective of time, or (3) run A\* at the start to ensure that the goal is reachable (omitting dynamic obstacles).

## Accounting for collisions
A position cannot be considered to be not open (i.e. possible to move into, even if it is free in the next time stamp) if either (1) a dynamic obstacle in the current time stamp swaps positions with the agent in the current cell in the next time stamp, or (2) if the vector of a dynamic obstacle across the current and next time stamps and the vector of the agent in the current cell across the current and next time stamp intersect (this would be a "cross-over" and a likely collision in reality). Realistically, both cases would lead to collisions, despite the positions being "free" in the next time stamp. This is harder to figure out of agents can move across different number of cells in a single time step; however, we can standardise the algorithm to make sure an agent moves at most one cell in one time step (see: [Standardising speed representation using integer time steps](#standardising-speed-representation-using-integer-time-steps)).

# Technical considerations in implementing CA\*
## Implementing reservation table
A data structure that informs which position is reserved by which agent at a given time stamp (if at all). This a crucial data structure when planning while accounting for the paths of dynamic, such as other agents. A simple implementation of a reservation is as follows (using a Python dictionary as the data structure):

- **Key**: A tuple in the form `(row index, column index, time stamp)`
- **Item**: The index/ID of the reserving agent

## Standardising speed representation using integer time steps
**Preference for using integer time steps**:

- Simpler to interpret and implement in code
- Can be standardised for any use-case, as shall be shown below
- Integer time stamps have lesser memory overhead <br> _Note that time stamps are to be stored for each position in_...
    - _Reservation table_
    - _Path planner search graph data storage_

---

**Extensiblity of standardisation using integer time steps**:

**NOTE**: _LCM stands for "least common multiple"._

Let the speeds of the agents $A_1, A_2 ... A_n$ (measured in cells per time step, i.e. cells / $\Delta t$) be $\frac{a_1}{\Delta t}, \frac{a_2}{\Delta t} ... \frac{a_n}{\Delta t}$ respectively. First, let us ensure that the numerators are whole numbers; to do this, multiply each of $a_1, a_2 ... a_n$ with a constant $b$. Such a constant exists as long as $a_1, a_2 ... a_n$ are rational. More precisely, if:

 $a_i = \frac{p_i}{q_i} \text{ } \forall i \in \set{1, 2 ... n}$, then:
 
 $b = LCM(q_1, q_2 ... q_n)$

**KEY POINT**: _Each of_ $a_1, a_2 ... a_n$ _must be a rational number._

---

Now, let us define $b_i$ such that:

$b \cdot \frac{a_i}{\Delta t} = \frac{b_i}{\Delta t} \text{(where } b_i \in ℕ \text{)} \text{ } \forall i \in \set{1, 2 ... n}$

Thus, multiplying each speed with $b$, we get $\frac{b_1}{\Delta t}, \frac{b_2}{\Delta t} ... \frac{b_n}{\Delta t}$. These values may not be the exact speeds of the agents, but they have the same ratio between each other as the corresponding agent speeds have between each other (hence, these values tell us about relative speeds, i.e. about how much faster is one agent compared to another; this information allows us to scale the speed appropriately when rendering the simulation). Now, note that:

$\frac{b_i}{\Delta t} = \frac{1}{\Delta t / b_i} \text{ } \forall i \in \set{1, 2 ... n}$

Now, let $c = LCM(b_1, b_2 ... b_n)$; thus, $c / b_i = c_i \in ℕ$. Hence:

$\frac{1}{c} \cdot \frac{1 }{\Delta t / b_i} = \frac{1}{(c / b_i) \Delta t} = \frac{1}{c_i \Delta t} \text{ } \forall i \in \set{1, 2 ... n}$

---

Now, note that:

- $\frac{1}{c_1 \Delta t}, \frac{1}{c_2 \Delta t} ... \frac{1}{c_n \Delta t}$ also tell us about relative speeds
- $\frac{1}{c_i \Delta t}$ can be read as: stay in 1 cell for $c_i$ time steps

This method allows us to duplicate agent positions across time steps in a structured and integer-oriented manner. By doing so, we conveniently and accurately represent relative speeds without requiring fractional time steps. Making sure time steps are integers while accurately conveying relative speeds is valuable because we can simplify and standardise the logic of the implementation while making sure it can be applied in a real-life use-case. Moreover, relative speed is sufficient for the cooperative path planning logic, since what such a planner needs is information about where the other agents would be or move in relation to a given agent with every iteration; the exact time-scale of the iteration is irrelevant. Furthermore, for rendering the simulation (either in real-time or in scaled up/down simulated time), we can simply scale up/down the simulator's time steps. To put it briefly, the unit of measurement is irrelevant for the path planner, and the desired unit can be applied by simply scaling (i.e. constant multiplication).

# Fixed-priority equal speed CA\*
To see why we are starting with this, see (1) ["Starting with fixed priority CA\*", _Multi-Agent Path Planning_, `ideation`](../ideation/multi-agent-path-planning.md#starting-with-fixed-priority-ca), and (2) ["Starting with equal speed assumption", _Multi-Agent Path Planning_, `ideation`](../ideation/multi-agent-path-planning.md#starting-with-equal-speed-assumption). Furthermore, we are using integer time steps; to see why this is an extensible and thus valid standardisation, see (3) ["Standardising speed representation using integer time steps" in this document](#standardising-speed-representation-using-integer-time-steps).

---

In this version of CA\*, each agent has a fixed priority even before the algorithm runs. The 1st agent pathfinds without considering any other agent, the 2nd agent pathfinds while considering only the 1st agent, the 3rd agent pathfinds while considering only the 1st and 2nd agents, etc. Under the equal speed assumption, all agents move at the same rate; specifically, for simplicity, all agents cover at most one cell per time step. Since there are no additional speed adjustments (e.g. artificial waiting to balance speed differences), agents move every time step unless they choose to wait when obstructed by a dynamic obstacle.
