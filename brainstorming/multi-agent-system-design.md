<h1>MULTI-AGENT SYSTEM DESIGN</h1>

---

**Contents**:

- [Challenge and opportunity](#challenge-and-opportunity)
- [Addressing the challenge](#addressing-the-challenge)
- [Addressing the opportunity](#addressing-the-opportunity)

---

Start date: 2025-02-25

# Challenge and opportunity
Multi-agent purpose-driven systems present a unique challenge and opportunity: the challenge is the management of dynamic, non-linear but non-random collision paths, and the opportunity is the coordination between agents to satisfy their combined goals more efficiently (e.g. by distributing an order to multiple agents based on their proximity to the items, by using an agent to pick items for another agent's order on its way to a common meeting point, decreasing the combined time of both agents in picking the items even though the first agent's time increases, by enabling the implemention batch picking, wave/cluster picking, etc.).

# Addressing the challenge
- Dynamic collision avoidance
    - Does not restructure single-agent pathfinding
    - Reacts and adapts to short-term projected collisions
    - Only focuses on local optimisation
- Planned collision avoidance
    - Restructures pathfinding for all agents
    - Proactively plans for long-term projected collisions
    - Focuses on global optimisation

Dynamic collision avoidance may result in admissible performance, at least for a smaller scale, but due to its myopic (i.e. locally-focused) approach, it cannot reliably be expected to address the challenge in every use-case, especially for larger-scale use-cases, since it cannot consider how locally-focused decisions affect goals in a broader context. Note that this limitation is not mere speculation but a demonstrable shortcoming compared to pre-planning. For example, when 2 or more agents need to access racks in the same aisle, dynamic collision avoidance may lead to excessive movement, backtracking, and potentially even jams (observe real-life traffic jams to get an idea). Pre-planning, if done right, can mitigate or even eliminate this, e.g. by assigning priorities and ensuring only non-conflicting paths are taken simultaneously. In addition, pre-planning provides transparency, logical precision, and thus logical and mathematical verifiability, whereas unplanned approaches involve unknowns that remain unresolved until new information becomes available at some often unpredictable point in time.

Thus, pre-planning offers:

- Potentially greater efficiency (in time and/or energy used)
- Reliability of solutions, especially in complex environments
- Ensures that a valid resolution of conflicting paths exists <br> _Unplanned approaches cannot necessarily ensure this_

This being said, pre-planning is much more computationally intensive, since it integrates a much more extensive range of factors (e.g. agent sizes, movements (planned or otherwise), speeds, goal prioritisations, etc.) that affect the quality of results across time. Furthermore, there may still be unpredictable factors (e.g. movement of people, unexpected drop of items, unregistered layout change/discrepancies between the stored layout map and the real-time layout information, etc.) that the agents must adapt to, thus needing dynamic collision avoidance. Hence, to address the challenge completely, I propose the addressal of both dynamic and planned collision avoidance. Furthermore, in addressing either method, it is key to focus on logical, memory and computational optimisation (i.e. optimisation at both a _conceptual and technical_ level) for the sake of (1) effectiveness, (2) usability and reliability across hardware and software platforms, and (3) demonstrability.

---

Related brainstorming notes:

- [Multi-Agent Path Planning](./multi-agent-path-planning.md)

# Addressing the opportunity
As of now, for a minimally viable and demonstrable solution, I regard collision avoidance as a priority for the following reasons: (1) collisions impair the very ability to complete tasks, whereas optimising tasks is only effective if the tasks can actually be completed, and (2) it is easier to demonstrate effective collision avoidance than effective task optimisation, since the former is more concrete (agents waiting, rerouting, etc.) whereas the latter requires the integration of more data (i.e. what orders where placed, where the items are located, how the agents' coordination reduces combined time, etc.). By ensuring robust collision avoidance first, we lay the groundwork for seamless future integration of task optimization strategies, ensuring that efficiency gains are not undermined by avoidable conflicts. Hence, for now, I shall not focus on addressing the opportunity; however, it is important to make sure my upcoming solutions can be easily extended to address the opportunity in the future.
