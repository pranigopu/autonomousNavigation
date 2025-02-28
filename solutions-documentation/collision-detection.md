<h1>COLLISION DETECTION</h1>

Click [here](../brainstorming/collision-detection-accounting-for-agent-dims.md) for brainstorming notes.

---

**Contents**:

- [Problem significance](#problem-significance)
- [Problem statement](#problem-statement)
- [Solution approach](#solution-approach)
- [Sub-solutions](#sub-solutions)
  - [1. Detect overlaps between rectangles](#1-detect-overlaps-between-rectangles)
  - [2. Obtain agent and grid cell BBoxes](#2-obtain-agent-and-grid-cell-bboxes)
    - [2.1 Agent BBox](#21-agent-bbox)
    - [2.2. Grid cell BBox](#22-grid-cell-bbox)
  - [3. Identify the grid cells covering the agent BBox](#3-identify-the-grid-cells-covering-the-agent-bbox)
  - [4. Filter covering grid cells for obstacle-containing cells](#4-filter-covering-grid-cells-for-obstacle-containing-cells)
- [Extending to collision detection between agents](#extending-to-collision-detection-between-agents)

---

# Problem significance
Collision detection enables path planning that:

- Accounts for agent dimensions
- Is flexible regardless of the agent's turning capabilities

# Problem statement
Given the agent's projected bounding box (BBox) (derived from the agent's projected position and dimensions), and given the cell dimensions, how to efficiently query the environment to determine whether the agent's projected BBox overlaps/collides with the BBox(es) of any obstacle cells?

---

**IMPORTANT CLARIFICATION**:

We are considering $x$ and $y$ axes such that the origin is at the top-left of the graph. Hence, $y = 0$ indicates the line at the top of the graph. Note also that we are not considering negative coordinates here; the grid must be defined within a positive coordinate space.

# Solution approach
Define mechanisms to:

1. Detect overlaps between rectangles \* <br> _Forms the basis for identifying potential collisions between rectangles_
2. Obtain agent and grid cell BBoxes
3. Identify the grid cells covering the agent BBox
4. Filter covering grid cells for obstacle-containing cells

\* _The derived solution generalises for all straight-edged convex figures, including but not limited to rectangles. This generalisation was done because (1) it was quite easy to extend the solution, and (2) the solution is extensible to any future decisions regarding agent and obstacle shapes._

---

The last step gives us collision detection:

- One or more obstacle-containing cells means collision
- No obstacle-containing cells means no collision

# Sub-solutions
## 1. Detect overlaps between rectangles
See [Overlap Detection for Straight-Edged Convex Figures](overlap-detection-for-straight-edged-convex-figures.md).

## 2. Obtain agent and grid cell BBoxes
### 2.1 Agent BBox
Solution is as follows:

- Inputs current position and target position
- Thereby identifies the agent's orientation
- Obtains rectangle corners using [Logic for Agent Turning](logic-for-agent-turning.md)

**NOTE**: _Agent dimensions are known._

### 2.2. Grid cell BBox
A cell's BBoxes are axis-aligned, so the above approach is overkill. Plus, we shall be querying a lot of cells for their corner coordinates, which means the more efficient the cell BBox retrieval, the better. As it turns out, a BBox being axis-aligned makes identifying its corners very straightforward.

---

Consider the following:

- A grid cell with row and column indices $i$ and $j$ <br> **NOTE**: _Indices start from_ 0
- Cell top-left coordinates (unknown) are $(x, y)$
- Cell width = $w$ (one column width)
- Cell length = $l$ (one row length)

---

The solution is as follows:

**Step 1**:

Obtain $(x, y)$ from $(i, j)$ as follows:

- $x = j \times w$
- $y = i \times l$

**Step 2**:

Get the grid cell's corner coordinates as follows:

- $(x, y)$ (top-left)
- $(x + w, y)$ (top-right)
- $(x + w, y + l)$ (bottom-right)
- $(x, y + l)$ (bottom-left)

## 3. Identify the grid cells covering the agent BBox
The most straightforward solution to this:

- Obtain the axis-aligned BBox (AABB) for the agent
- Convert the above into a range of row and column indices

**NOTE**: _Identifying cells covering an AABB is much easier than identifying cells covering a BBox with any other orientation. This is why this is the most straightforward solution._

---

Let the agent BBox have the following corner coordinates:

$((x_1, y_2), (x_2, y_2),  (x_3, y_3),  (x_4, y_4))$

Then, the AABB of the agent is as follows:

- Top-left corner $(x, y) = (\min(x_1 ... x_4), \min(y_1 ... y_4))$
- Width $w = \max(x_1 ... x_4) - x$
- Length $l = \max(y_1 ... y_4) - y$

**NOTE**: _Width and length for an agent BBox in general is defined as: width being the size of the edge of the BBox that faces a target position, length being the size of the edge adjacent to this. However, width and length for an AABB is defined as: width being the x-axis extension, length being the y-axis extension._

---

Hence, the AABB of the agent has the corners:

- $(x, y)$ (top-left)
- $(x + w, y)$ (top-right)
- $(x + w, y + l)$ (bottom-right)
- $(x, y + l)$ (bottom-left)

**NOTE**: _Using corners for AABB may not be necessary, since it is easier to identify the row and column indices of the range of cells covering an AABB using the AABB's top-left coordinates, width and length._

## 4. Filter covering grid cells for obstacle-containing cells
This is a matter of filtering the cells corresponding to the row and column index ranges obtained in the [previous step](#identify-the-grid-cells-covering-the-agent-bbox). This is a more technical solution that involves knowledge of the array-handling tools used (NumPy, in my case). The NumPy-based implementation for this can be seen [here](../implementation/trials/spatial_querying/grid_cell_cluster_filtering_for_obstacles.py).

# Extending to collision detection between agents
Instead of querying all the grid cells covering the axis-aligned bounding box of a given agent, collision detection between agents is simply a matter of checking for overlaps between the bounding boxes (not axis-aligned) of a given agent against all other agents. Note how this is conceptually simpler than detecting collisions between agents and their environment.