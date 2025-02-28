<h1>SETTING UP MULTI-AGENT SIM</h1>

---

**Contents**:

- [Priorities](#priorities)
- [Problem definition](#problem-definition)
- [Design solutions for problem definition](#design-solutions-for-problem-definition)
- [Suggested approach](#suggested-approach)

---

Start date: 2025-01-03

---

_Check_ [_here_](../work-logs/2025-01.md#2025-01-03) _to see how it fits with the project's objectives and with what has been achieved so far._

---

**Suggestion**: _Keep agent behaviour independent of environment representation. In other words, you must be able to change the environment representation as needed (in case a more effective representation is found) without needing to alter agent behaviour code. This means the same interface between the agent and the environment must be maintained._

# Priorities
_Taken from work log_

- Identifying the next deliverables <br> _Being relatively concrete, it comes after conceptual problem definition_
- Defining the problem in conceptual terms
- Identifying potential design solutions
- _Understand the needs for a minimal viable solution (MVS)_

**NOTE**: _Once the MVS is made, it can be iteratively improved._

_The code will come only after the above are clear._

---

**NOTE**:

Focus on the MVS enables me to:

- Test functionality in real-world-like scenarios ASAP <br> _Note that early testing will:_
    - Help reveal practical issues not obvious in conceptual design
    - Provide immediate feedback on real-world performance
    - Allow you to make quick adjustments before adding complexity
- Identify weaknesses in the design or behavior of the agents
- Add complexity in a simplified, step-by-step process
- Present solid progress while working on improvements

---

**Task Prioritisation**: _Focus first on core functionality, leaving features like advanced logging or stress-testing for later iterations._

# Problem definition
The problem can be defined in 6 layers of increasing abstraction:

**NOTE**: _The environment is considered as 2D unless specified._

<details>
<summary><b>1. <code>Perception</code></b></summary>
<i>By default, assume 100% accuracy for simulation</i>
<table>
<tr>
<th>Section</th>
<th>Description</th>
</tr>
<tr>
<td><code>Detection</code></td>
<td>
<ul>
<li>Static obstacle</li>
<li>Dynamic obstacle</li>
<li>Proximity sensing</li>
</ul>
</td>
</tr>
<tr>
<td><code>Odometry</code></td>
<td>
<ul>
<li>Helps identify current and desired locations</li>
<li>Includes position and orientation relative to start</li>
</ul>
</td>
</tr>
<tr>
<td><code>Vision</code></td>
<td>Helps identify obstacle types</td>
</tr>
</table>
</details>

<details>
<summary><b>2. <code>Action</code></b></summary>
<table>
<tr>
<th>Section</th>
<th>Description</th>
</tr>
<tr>
<td><code>Movement</code></td>
<td>
<ul>
<li>Translation2D</li>
<li>Rotation2D (i.e., turning)</li>
</ul>
</td>
</tr>
<tr>
<td><code>Handling</code></td>
<td>
<ul>
<li>Picking</li>
<li>Placing</li>
</ul>
</td>
</tr>
</table>
</details>

<details>
<summary><b>3. <code>Navigation</code></b></summary>
<i>Integrates</i>
<ul>
<li><code>Perception</code></li>
<li><code>Action.Movement</code></li>
</ul>
<table>
<tr>
<th>Section</th>
<th>Description</th>
</tr>
<tr>
<td><code>Avoidance</code></td>
<td>
<ul>
<li>Static obstacle</li>
<li>Dynamic obstacle
<ul>
    <li>Reactive avoidance</li>
    <li>Predictive avoidance</li>
</ul>
</li>
</ul>
</td>
</tr>
<tr>
<td>
<code>Seeking</code> <br> <i>Ties to</i>
<ul>
<li><code>Perception.Odometry</code></li>
<li><code>Perception.Vision</code></li>
</ul>
</td>
<td>
<ul>
<li>Position seeking <br> <i>Ties to</i> <code>Perception.Odometry</code></li>
<li>Item seeking <br> <i>Ties to</i> <code>Perception.Vision</code></li>
</ul>
</td>
</tr>
</table>
</details>

<details>
<summary><b>4. <code>GoalDefinition</code></b></summary>
<table>
<tr>
<th>Section</th>
<th>Description</th>
</tr>
<tr>
<td><code>Processing</code></td>
<td>Via appropriate data formats</td>
</tr>
<tr>
<td><code>Representation</code></td>
<td>Via appropriate data structures</td>
</tr>
</table>
</details>

<details>
<summary><b>5. <code>DecisionMaking</code></b></summary>
<i>Integrates</i>
<ul>
<li><code>Navigation</code></li>
<li><code>GoalDefinition</code></li>
</ul>
<table>
<tr>
<th>Section</th>
<th>Description</th>
</tr>
<tr>
<td><code>GoalPrioritisation</code></td>
<td>
With respect to:
<ul>
<li>Efficiency</li>
<li>Urgency*</li>
</ul>
</td>
</tr>
<tr>
<td><code>GoalOptimisation</code></td>
<td></td>
</tr>
</table>
</details>

<details>
<summary><b>6. <code>Tasking</code></b></summary>
<i>Integrates</i>
<ul>
<li><code>DecisionMaking</code></li>
<li><code>Action</code></li>
</ul>
<table>
<tr>
<th>Section</th>
<th>Description</th>
</tr>
<tr>
<td><code>OrderPicking</code></td>
<td><code>DecisionMaking</code> + <code>Action.Picking</code></td>
</tr>
<tr>
<td><code>Putaway</code></td>
<td><code>DecisionMaking</code> + <code>Action.Placing</code></td>
</tr>
<tr>
<td><code>Sorting</code></td>
<td><code>DecisionMaking</code> + <code>Action</code></td>
</tr>
<tr>
<td><code>TaskCoordination</code></td>
<td>Extends from + refines <code>DecisionMaking</code>*</td>
</tr>
</table>
</details>

\* _Can wait for now._

---

**NOTE: `Navigation` in relation to `GoalDefinition` + `DecisionMaking`**: <br> `Navigation`, specifically `Navigation.Seeking`, involves elements of both `GoalDefinition` and `DecisionMaking`, due to destination-seeking and path optimisation, which are key to navigation. This aligns with the above presentation, since the layers go from more concrete to more abstract. Specifically, `GoalDefinition` generalises the destination-seeking and path optimisation aspects of `Navigation`, while `DecisionMaking` generalises the path-planning, collision avoidance and execution aspects of `Navigation`. In short, `Navigation` is `GoalDefinition` + `DecisionMaking` as applied to the specific problem of using environmental inputs.

**NOTE: `Perception.Detection` vs. `Perception.Vision`**: <br> `Detection` focuses on identifying the presence of obstacles (static/dynamic) while `Vision` helps categorise or further interpret them (e.g. obstacles vs. items, racks vs. tables, etc.).

# Design solutions for problem definition
**NOTE**: _MVP stands for "Minimal Viable Product"_

<table>
<tr>
<td><strong>Core Focus</strong></td>
<td>
<ul>
<li>Establish MVP functionality via...</li>
<li>Modular structure for future scalability that...</li>
<li>Integrates the key layers:
<ul>
<li><code>Perception</code></li>
<li><code>Action</code></li>
<li><code>Navigation</code></li>
<li><code>DecisionMaking</code></li>
<li><code>GoalDefinition</code></li>
<li><code>Tasking</code></li>
</ul>
</li>
</ul>
</td>
</tr>
<tr>
<td><strong>Goal Optimisation</strong></td>
<td>
<ul>
<li>Heuristic-based shortest path algorithm <br> <i>For basic optimisation</i></li>
<li>Set foundation for future complex optimisations</li>
</ul>
</td>
</tr>
<tr>
<td><strong>Task Coordination</strong></td>
<td>
<ul>
<li>Sequential task execution <br> <i>One task at a time</i></li>
<li>Single-agent task flow:
<ul>
<li><code>OrderPicking</code></li>
<li><code>Putaway</code></li>
<li><code>Sorting</code></li>
</ul>
</li>
<li>Future support for multi-agent coordination</li>
</ul>
</td>
</tr>
<tr>
<td><strong>Urgency Handling</strong></td>
<td>
<ul>
<li>Heuristics-based task prioritisation <br> <i>E.g. proximity, deadline</i></li>
<li>Supports efficiency/time-sensitive task handling</li>
</ul>
</td>
</tr>
<tr>
<td><strong>Layer Integration</strong></td>
<td>
<ul>
<li>Navigation ties aspects of:
<ul>
<li><code>GoalDefinition</code> <br> <i>Destination seeking</i></li>
<li><code>DecisionMaking</code> <br> <i>Path optimisation, collision avoidance</i></li>
</ul>
</li>
<li>Tasking integrates:
<ul>
<li><code>DecisionMaking</code> with task-specific actions <br> <i>E.g. Picking, Placing, Sorting</i></li>
</ul>
</li>
</ul>
</td>
</tr>
<tr>
<td><strong>Agent Behavior</strong></td>
<td>
<ul>
<li>Agents perceive obstacles <br> <i>Static/dynamic</i></li>
<li>Agents act accordingly <br> <i>Movement, picking, placing</i></li>
<li>Real-time performance metrics <br> <i>For throughput and efficiency evaluation</i></li>
</ul>
</td>
</tr>
</tbody>
</table>

# Suggested approach
_Based on ChatGPT interaction._

<table>
<tr>
<th>Section</th>
<th>Associated Content</th>
</tr>
<tr>
<td><b>1. Env Representation</b></td>
<td>
<details><summary><i>Enhance Flexibility for Dynamic Changes</i></summary>Consider adding a mechanism to log or track dynamic changes (e.g. timestamps for obstacle appearance/removal). This can later be leveraged for debugging or advanced metrics like downtime due to obstacles.</details>
<details><summary><i>Matrix Resolution and Performance</i></summary>Ensure that the customizable resolution of the numerical matrix balances computational efficiency and path-planning precision. Test edge cases with very high or very low resolutions to identify potential bottlenecks.</details>
</td>
</tr>
<tr>
<td><b>2. Sim Interface</b></td>
<td>
<details><summary><i>Prepare for Transition to Dashboard</i></summary>While a simple textual log is fine now, keeping the log data modular (e.g. JSON or CSV format) will simplify transitioning to a live dashboard.</details>
<details><summary><i>Accessible Visualisation</i></summary>Although animations are not a priority, consider using basic markers (e.g. color-coded rectangles or arrows) to differentiate agent states or actions for easier interpretation by users.</details>
</td>
</tr>
<tr>
<td><b>3. Performance Metrics</b></td>
<td>
<details><summary><i>Incremental Refinement</i></summary>Start with simple definitions of throughput, picking efficiency, and navigation efficiency, and gradually refine them based on simulation outcomes. This ensures that metrics remain realistic and relevant.</details>
<details><summary><i>Correlation Analysis</i></summary>Even if metrics-based decision-making is out of scope, collect data in a format that allows future correlation analysis (e.g. between navigation efficiency and throughput).</details>
</td>
</tr>
<tr>
<td><b>4. Algo Integration</b></td>
<td>
<details><summary><i>Interface Standardisation</i></summary>Create a mock template or interface specification for the algorithm classes early. This ensures uniformity and makes integrating multiple algorithms straightforward.</details>
<details><summary><i>Debugging Tools</i></summary>Build a simple mechanism to test individual algorithms in isolation, which will help diagnose issues before full integration into the simulation.</details>
</td>
</tr>
<tr>
<td><b>5. Dev Timeline</b></td>
<td>
<details><summary><i>Day 1-3</i></summary>Finalise the numerical matrix representation and ensure the warehouse layout implementation (via patterns) integrates seamlessly with it.</details>
<details><summary><i>Day 4-6</i></summary>Implement basic agent behaviors, such as obstacle avoidance and path-following.</details>
<details><summary><i>Day 7-10</i></summary>Focus on multi-agent simulation, including collision handling and path optimisation.</details>
<details><summary><i>Day 11-14</i></summary>Validate metrics calculations, test edge cases, and refine the simulation interface for usability.</details>
</td>
</tr>
</table>