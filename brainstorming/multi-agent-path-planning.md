<h1>MULTI-AGENT PATH PLANNING</h1>

---

**Contents**:

- [Problem statement](#problem-statement)
- [Implementation approach](#implementation-approach)
  - [1. Establish test environment](#1-establish-test-environment)
  - [2. Separate item-handling and path planning](#2-separate-item-handling-and-path-planning)
  - [3. Choose the most extensible object-oriented approach](#3-choose-the-most-extensible-object-oriented-approach)
- [Algorithm choices](#algorithm-choices)
  - [Cooperative A\* (CA\*)](#cooperative-a-ca)
    - [Why CA\*?](#why-ca)
    - [Starting with fixed-priority CA\*](#starting-with-fixed-priority-ca)
    - [Implementing reservation table](#implementing-reservation-table)
    - [Starting with equal speed assumption](#starting-with-equal-speed-assumption)
    - [Windowed CA\* (WCA\*)](#windowed-ca-wca)

---

Start date: 2025-02-24

# Problem statement
In essential terms, we are dealing with a **search problem** with 3 essential capabilities given to the searching agent: (1) detect obstacles/collisions from a given position, (2) search and obtain possible movement positions, (3) move to a possible movement position. What we are seeking is generalisable solution for cooperative path planning, i.e. generalisable logic to handle dynamic obstacles (i.e. other agents) within path planning. If we can implement and test this solution in a simpler environment while ensuring that the solution's logic relies only on essentials and not on implementation-specific details (e.g. the specific method of obstacle detection and agent movement), we can generalise this logic for any grid-based environment and navigation.

**NOTE**: _Agent dimension and orientation are subsumed within obstacle detection, since these factors are key to detecting collisions with other bounding boxes in the environment (dynamic or static)._

# Implementation approach
## 1. Establish test environment
Establish a simple environment to learn about and test the cooperative path planning solution (so as to focus on resolving the complexities of cooperative path planning, and to ensure that the core solution can be easily presented, explained and generalised).

## 2. Separate item-handling and path planning
Keep item-handling separate from path planning. Why? Positions to pick and place items register simply as navigational waypoints to the path planner. Furthermore, to optimise item-handling (especially item-picking and putaway), we can either obtain heuristics or some path planning algorithm to obtain true distances, so as to figure out and minimise total distances travelled; even here, once the destinations are decided, all that remains is cooperative path planning to reach these destinations, all the while accounting for time taken to perform item-handling operations at the destinations (which can simply be inputs to the path planning algorithm, e.g. wait/pause time).

As for algorithms that plan which agents should handle which items in what way (so as to optimise overall operations), based on agent positions, capabilities and item placements, I am not sure what the best solution structure is. However, even if it requires integrated methods to handle both item-handling and path planning, it is still useful to implement and test path planning separately before integrating it (to come to terms with the complexities within path planning itself). Moreover, as far as I can project, the same essentials that apply for path planning on its own also apply to such integrated methods, namely (1) obstacle detection and collision avoidance, (2) possible movement position search, and (3) optimal navigation from position to position. As of now, I have no clear reason to integrate item-handling and path planning, and I have ample reasons to keep the solution modular (e.g. wide applicability in a variety of potential use-cases, and also, the broader coding practice-related reasons, e.g. separation of concerns). Also, the modular approach has more use-cases and offers better demonstrability, especially in the earlier and intermediate stages of development.

## 3. Choose the most extensible object-oriented approach
The goal is to implement cooperative path planning. In this, the agents must cooperate, but by what means? I see 2 options, broadly: (1) shared data, with planning logic distributed to each agent, and (2) an integrated "agent manager" object which manages agent coordination and gives the necessary path planning results to each agent (by necessary, I mean the information needed by the agent to move along the intended path; this may omit everything except the waypoints and wait times).

Ultimately, both approaches must achieve cooperative path planning, which means both approaches must be equivalent in terms of the outputs of the simulation (provided that the same constraints and planning algorithms are applied). However, the choice of approach could have significant consequences in practice; I say this for the following reasons:

A.<br>
(1) offers a decentralised approach with intelligent (and thus more computationally intensive) agents and frequent inter-agent communication, and (2) offers a centralised approach with an intelligent planner and unintelligent agents (thus, overall, less computationally intensive) with minimal communication between agents and more of a client-server system.

B.<br>
However, (1) makes agents more adaptable and less dependent on a central system and less reliant on a centralised communication network, thereby also offering more redundancy, since failure in one system (i.e. one agent) leaves the others intact and capable, and potentially, capable of compensating for the failure. On the other hand, (2) relies on a robust centralised infrastructure, and failure in either the central system or centralised communication network would impair the operation of the entire fleet of agents.

_Hence, the approach significantly shapes challenges and opportunities._

---

At this point, I am not sure which approach is better in practice, or whether the approach must change based on the use-case. Here, since both (1) and (2) are equivalent in terms of simulation output, and since it is not clear which approach should be prioritised, the key question becomes: what is the most extensible and adaptible solution?

To answer this, consider: (2) allows agent classes to be much simpler. Furthermore, the agent manager class will still have to associate agents to agent-specific data (i.e. the agent's movement across time) and logic (i.e. the agent's reactions and interactions with other agents); in my judgement, this association can be translated to (1) if necessary.

Secondly, both (1) and (2) involve an equal (or at least similar) amount of data consolidation for the path planner: agent positions and movements across time, how the agents must coordinate their movements with respect to other agents across time, what are the other agents' dimensions and speeds, how the other agents would react the an agent's decisions across time, etc. Hence, even to implement an intelligent agent approach, it makes sense to implement (2) and, if necessary, simply give access to the agent manager object (or its duplicates) to each agent, with minor modifications to ensure the agent executes its own decisions and not some other agent's.

---

Hence, in conclusion, solution (2) is viable for both:

- Centralised solution
- Decentralised solution

However, solution (1) is less straightforward for centralisation.

# Algorithm choices
## Cooperative A\* (CA\*)
> **Also see my solution documentation for CA\***: [Cooperative A\*_, `solutions-documentation`](../solutions-documentation/cooperative-a-star.md)

### Why CA\*?
A\* is an optimal, relatively simple and (as of now) sufficiently well-performing algorithm for single-agent pathfinding; moreover, due to the modularity of the code, we can easily switch the pathfinding algorithms used in the future, if need be, as long as we follow the same standard format for path representation. Due to this, my first attempt at multi-agent path planning will be to implement the simplest extension of A\* into a multi-agent context, namely cooperative A\*. Due to its basis in A\*, it should be relatively easy to understand, implement and test, and due to its optimal nature, it should produce promising results to present for the next minimum viable solution (MVS). Moreover, it introduces (in practical terms) multi-agent concepts such as consideration of other agent paths into an agent's own path planning, priority-based planning and fixed-window projection of future coordination (since cooperative path planning would be an ongoing process in a warehouse simulation context). Hence, in short, my first step toward multi-agent path planning is CA\* due to the following reasons:

- Relative simplicity (conceptually and technically)
    - Allows for quick and promising deliverable
    - Is potentially viable in practice with optimisations
    - Is a theoretically optimal and complete solution
- Introduces transferrable practical understanding
    - Consolidation and processing of data from multiple agents <br> _Improves understanding of necessary data structures, object-oriented approaches, etc._
    - Continual but efficient multi-agent processing <br> _Since simulations may run for long durations_ <br> **Examples**: _Windowed multi-agent processing, fixed-depth path optimisation, etc._

### Starting with fixed-priority CA\*
Fixed-priority CA\* is one where each agent is given a fixed precedence in reserving positions during pathfinding; the 1st agent simply pathfinds using A\*, the 2nd agent pathfinds while considering the 1st agent's movements, the 3rd agent pathfinds while considering the 1st and 2nd agents' movements, etc. This is the simplest cooperative A\* approach to implement, because a complete reservation table can be built simply by sequentially processing agents as per their priorities.

---

**Extensibility: Why start with fixed-priority CA\*?**

Once we have acquired the ability to build a reservation table as per agent priorities, we can apply this ability to build reservation tables that extend for only a fixed period of time (i.e. for a fixed window); this opens the door to windowed CA\* (WCA\*), which can (1) apply CA\* within an indefinite/long-term simulation, and (2) reprioritise agents with every window, thus potentially overcoming bottlenecks or deadlocks caused by a certain prioritisation, because the effectiveness of CA\*'s solution depends on the prioritisation of the agents, i.e. the order in which agent positions are reserved. Take the following example...

---

<details>
<summary><b>Demonstrating agent reservation order sensitivity</b></summary>
<p>

<pre>
Start state:
.  .  X  X  X  
B  1  .  2  A  
.  X  .  X  X 
.  .  .  .  .  
.  .  .  .  .  
</pre>

Here:

<ul>
    <li><code>1</code> denotes agent 1</li>
    <li><code>3</code> denotes agent 2</li>
    <li><code>A</code> marks the goal of agent 1</li>
    <li><code>B</code> marks the goal of agent 2</li>
    <li><code>X</code> denotes an obstacle cell</li>
    <li><code>.</code> denotes a free space cell</li>
</ul>

<b>CASE 1: Agent 1 has priority of reservation</b>:
<br>
<i>Agent 1 thus plans its path to A without considering agent 2.</i>

<pre>
1 reserves the next spot; 2 waits:
.  .  X  X  X  
B  .  1  2  A  
.  X  .  X  X 
.  .  .  .  .  
.  .  .  .  .

1 reserves the next spot; 2 moves back:
.  .  X  X  X  
B  .  1  .  2  
.  X  .  X  X 
.  .  .  .  .  
.  .  .  .  . 

Deadlock:
.  .  X  X  X  
B  .  .  1  2  
.  X  .  X  X 
.  .  .  .  .  
.  .  .  .  . 
</pre>

<b>CASE 2: Agent 2 has priority of reservation</b>:
<br>
<i>Agent 2 thus plans its path to A without considering agent 1.</i>

<pre>
2 reserves the next spot; 1 waits:
.  .  X  X  X  
B  1  2  .  A  
.  X  .  X  X 
.  .  .  .  .  
.  .  .  .  .

2 reserves the next spot; 1 moves back:
.  1  X  X  X  
B  .  2  .  A  
.  X  .  X  X 
.  .  .  .  .  
.  .  .  .  . 

The next steps: 1 waits until 2 moves to B, then navigates to A.
</pre>
</p>
</details>

---

The above example demonstrates how prioritisation can significantly impact the effectiveness (and success) of multi-agent path planning. Fixed-priority CA\* can lead to unresolvable deadlocks, whereas a more flexible, dynamic prioritisation can resolve such deadlocks by simply changing the prioritisation (although, note that it is still not guaranteed that the new prioritisation would work, and if poorly designed, the reprioritisation mechanism may result in endless cycles; imagine, in the above example, if we kept alternatively prioritising agents 1 and 2).

That being said, fixed-priority CA\* gives the technical foundations on which more optimised/well-designed algorithms can be built. By first implementing a robust reservation system and understanding its limitations, we can then introduce mechanisms such as cycle detection, adaptive heuristics (?), or local conflict resolution to enhance prioritisation strategies. This makes fixed-priority CA\* both a relatively simple and highly extensible starting point.

### Implementing reservation table
A data structure that informs which position is reserved by which agent at a given time stamp (if at all). This a crucial data structure when planning while accounting for the paths of dynamic, such as other agents. A simple implementation of a reservation is as follows (using a Python dictionary as the data structure):

- **Key**: A tuple in the form `(row index, column index, time stamp)`
- **Item**: The index/ID of the reserving agent

### Starting with equal speed assumption
Starting with the assumption that all agents have equal speeds helps us focus on cooperation-related complexities before moving on to synchronisation-related complexities. Moreover, a solution with this assumption is an extensible starting point, since unequal speeds can be established by duplicating an agent's position across time steps in the reservation table. This aspect is expanded upon in ["Standardising speed representation using integer time steps", _Cooperative A\*_, `solutions-documentation`](../solutions-documentation/cooperative-a-star.md#standardising-speed-representation-using-integer-time-steps) (note that the basis of the contents linked here were initially drafted roughly on paper, and was done so before moving on with the [implementation in 2025-02-26](../work-logs/2025-02.md#2025-02-26)).

### Windowed CA\* (WCA\*)
> **Key reference**: [_Cooperative Pathfinding (Academic Paper)_ by David Silver](../reading/cooperative-pathfinding-academic-paper.pdf)

---

Fixed-priority CA\* has a number of issues:

- Certain agent reservation orders may have no solutions
- Agents "disappear" once they reach their goals
    - Hence, inactive agents cannot be accounted for\*
    - Agent paths may be unequal, making this issue relevant
- It is not applicable in an indefinite/long simulation
    - There is no clear repeatable pathfinding process
    - Time-coordination is not straightforward <br> _E.g. if a lower priority reaches its goal sooner, when and how does it move to its next path?_

\* _We can account for higher priority inactive agents by marking them as obstacles in the environment grid; however, this is inadequate, since lower priority inactive agents are still ignored, i.e. their positions are treated as free space by higher priority agents; hence, the rendered simulation would still show a number of agents passing through the positions of inactive agents._

---

To address these issues, we can instead prioritise and _cooperatively_ pathfind for a fixed number of time steps, i.e. a fixed window of time steps, before reprioritising. Here, an agent follows its destinations or waits at a destination however it needs to, but its steps are partitioned into a fixed window of time steps for which it contributes to the reservation table as per its assigned priority for the current window. Within each window, it _cooperatively_ pathfinds to its destination(s) for up to a fixed number of time steps, which means up to a fixed search depth (new destination(s) may be considered if the agent has reached one destination within the window and needs to reroute to its next destination); this means that an agent may not find and move according to its full optimal _cooperative_ path to its destination. This approach has some tradeoffs:

- The entire _cooperative_ optimal path may not be found
- Thus, partial paths may be suboptimal in a cooperative context <br> _Because future reroutes for more optimal cooperative paths may be ignored_

**NOTE**: _The word "cooperative" is emphasised, because, logically, we only need to limit the cooperative search due to window-based reprioritisation; however, in order to orient itself effectively, an agent may still pathfind non-cooperatively (i.e. using regular A\*) beyond the window. This is further discussed below._

---

Quoting from [David Silver (Cooperative Pathfinding)](../reading/cooperative-pathfinding-academic-paper.pdf):

_To ensure that the agent heads in the correct direction, only the cooperative search depth is limited to a fixed depth, whilst the abstract search is executed to full depth. A window of size w can be viewed as an intermediate abstraction that is equivalent to the base level state space for w steps, and then equivalent to the abstract level state space for the remainder of the search. In other words, other agents are only considered for w steps (via the reservation table) and are ignored for the remainder of the search._

In other words, during pathfinding, the agent considers other agents for only $w$ time steps ($w$ being the window size), after which it pathfinds as if there are no agents (i.e. in the "abtract search space", which is simply the grid without any other agents). Hence, the agent pathfinds cooperatively for $w$ time steps, and non-cooperatively for the remainder of the time steps until it finds the path to its goal.

**NOTE**: _Finding and following the full cooperatively optimised path based on the current prioritisation is not geared to be effective, since the current prioritisation is likely to change in the next window before the agent reaches its destination._

---

<details>
<summary><b>SIDE NOTE: Connection to hierarchical cooperative A* (HCA*)</b></summary>
<p>
In the same referenced paper, the following is given:
<br><br>
<i>To search this new search space efficiently, a simple trick can be used. Once w steps have elapsed, agents are ignored and the search space becomes identical to the abstract search space. This means that the abstract distance provides the same information as completing the search. For each node Ni reached after w steps a special terminal edge is introduced, going directly from Ni to the destination G, with a cost equal to the abstract distance from Ni to G. Using this trick, the search is reduced to a w-step window using the abstract distance heuristic introduced for HCA*.</i>
<br><br>
I shall explain this for clarity (based on my own reading of the paper and broader understanding), and because it may be potentially useful to apply HCA* and windowed HCA* (WHCA*) in the future (for reasons I shall make clear now). HCA* is just like CA* but with a more sophisticated heuristic, namely the abstract distance heuristic, which is the exact grid distance between a given node and the goal, not accounting for any agents (the paper discusses RRA* as a method to efficiently calculate this heuristic on demand, and the effectiveness of this heuristic is also explored, but I shall not go into it right now, since I am not yet implementing HCA* or WHCA*). If this heuristic is available, then for WCA* (which then becomes WHCA* due to the use of this heuristic), the abstract (i.e. non-cooperative) search that must be done after the window of w time steps is redundant, since nodes in the cooperative part of the agent's would already have been expanded based on what would be most effective considering an optimal path found by abstract search (i.e. A* search without considering agents).
<br><br>
Hence, WCA* would only need to pathfind cooperatively for w time steps using the abstract distance heuristic to achieve the same effectiveness in orienting itself toward the goal. In other words, if we use the abstract distance heuristic in WHCA*, then after the cooperative window, the non-cooperative search is unnecessary because the cooperative steps already used a strong heuristic. Since WHCA* improves orientation toward the goal without extra non-cooperative search, it may be a worthwhile alternative to WCA* in scenarios requiring more scalability or heuristic-driven efficiency.
</p>
</details>

---

WCA\* is an improvement on fixed-priority CA\* for 3 reasons:

<details>
<summary><b>1. Indefinite repeatability</b></summary>
<p>
It provides a structured and repeatable process that can be extended to any current or future configuration of agents and destinations.
</p>
</details>

<details>
<summary><b>2. Simple but crucial extension of fixed-priority CA*</b></summary>
<p>
It builds on fixed-priority CA* while adding the feature of indefinite repeatability, which is a required feature for an indefinite/long-term simulation. Thus, it is a practical next step in progressing toward a minimum viable solution (MVS) that manages cooperative pathfinding within a warehouse simulation.
</p>
</details>

<details>
<summary><b>3. Conflict-resolution and robustness to deadlocks</b></summary>
<p>
While it may produce suboptimal results, it is a more robust solution than fixed-priority CA* as it prevents unresolvable agent reservation orders from remaining unresolved over time; essentially, <b><i>WCA* sacrifices some optimality for repeatability and adaptability in dynamic environments</i></b>.
</p>
</details>

---

Hence, in practice, due to its ability to (1) extend indefinitely across time, (2) provide a sufficiently optimised approach in practice (especially in an environment with a relatively simple arrangement of static obstacles, e.g. a warehouse) and (3) provide a robust yet simple system for managing conflicts and avoiding deadlocks, WCA* offers a structured, repeatable and adaptable alternative to fixed-priority CA\*, making it a promising step toward scalable multi-agent pathfinding.

---

**Reprioritisation methods to consider**:

- **Randomised**: <br> Simple but lacks predictability
- **Round-Robin**: <br> Ensures fairness but may not account for agent workload
- **Dynamic Load Balancing**: <br> More complex but optimizes agent efficiency over time

---

**Considerations**:

- Effect of window size
- (_Related to the above point_) Effect of replanning frequency
