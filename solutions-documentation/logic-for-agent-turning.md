<h1>LOGIC FOR AGENT TURNING</h1>

---

**Contents**:

- [Introducing the problem](#introducing-the-problem)
- [Basic setup and image reference](#basic-setup-and-image-reference)
- [Outline](#outline)
  - [Desired quantities](#desired-quantities)
  - [Known quantities](#known-quantities)
- [Derivation](#derivation)
  - [Key relationships](#key-relationships)
  - [Key derived values](#key-derived-values)
  - [Finding coordinates of B and C](#finding-coordinates-of-b-and-c)
  - [Finding the coordinates of A and D](#finding-the-coordinates-of-a-and-d)
- [Organising the results](#organising-the-results)
- [Implementation](#implementation)

---

# Introducing the problem
Consider the following:

- The agent's centre is at $K = (x_0, y_0)$ <br> **NOTE**: $K_x = x_0, K_y = y_0$
- The agent wants to go toward $(x_1, y_1)$
- The agent's dimensions are as follows:
    - Width = $w$
    - Height = $h$

The question is: what should be the coordinates of the agent's corners so that its orientation is the vector connecting $(x_0, y_0)$ and $(x_1, y_1)$, i.e. $(x_1 - x_0, y_1 - y_0)$? Knowing the answer to this question helps us fix the agent's orientation, given its current position and its destination's position. This in turn forms the basis for a turning mechanism; motion along a curve (which would lead to smoother turns) can be broken down as motion along a sequence of line segments that together approximate the curve. Hence, the answer to this question is key in laying a robust and extensible basis for agent movement.

# Basic setup and image reference
Let the agent be the following rectangle ABCD. Note that:

- $AB = l$ (length)
- $BC = w$ (width)

---

![Geometrical Diagram](resources/geometrical-diagram-for-logic-for-agent-turning.png)

# Outline
## Desired quantities
The coordinates of A, B, C and D.

## Known quantities
- $\Delta x = (x_1 - x_0)$
- $\Delta y = (y_1 - y_0)$
- $n = \mid (\Delta x, \Delta y) \mid = \sqrt{\Delta x^2 + \Delta y^2}$ <br> _This quantity is in fact_...
    - Length of line linking $(x_0, y_0)$ and $(x_1, y_1)$
    - Hypotenuse of triangle $((x_0, y_0), (x_1, y_0), (x_1, y_1))$
- $\cos \theta = \Delta x / n$
- $\sin \theta = \Delta y / n$
- $KG = l/2$
- $BG = CG = w/2$

# Derivation
## Key relationships
The following triangles are right angles:

$KFE, KIG, GHC, BJG$

---

The following triangles are similar:

$KFE \sim KIG \sim GHC \sim BJG$

<details><summary>Proof</summary>
<ul>
    <li>At least 2 equal angles between each</li>
    <li><b>HINT</b>: Each of JGI, KGB and KGC forms a right angle</li>
</details>

---

The following triangles are identical:

$GHC \equiv BJG$

<details><summary>Proof</summary>
<ul>
    <li>Equal angles GHC, BJG</li>
    <li>Equal sides BG = GC = w/2 opposite to the equal angles</li>
</details>

## Key derived values
$KG \cos \theta = (l/2) \cos \theta = KI$

$GC \cos \theta = (w/2) \cos \theta = GH = BJ$

$GC \sin \theta = (w/2) \sin \theta = JG = HC$

$KG \sin \theta = (l/2) \sin \theta = GI$

## Finding coordinates of B and C
$x$-coordinate of B:

$K_x - (JG - KI)$

$= K_x - ((w/2) \sin \theta - (l/2) \cos \theta)$

$= K_x - (w/2) \sin \theta + (l/2) \cos \theta$

---

$y$-coordinate of B

$K_y + GI + BJ$

$= K_y + (l/2) \sin \theta + (w/2) \cos \theta$

---

$x$-coordinate of C:

$K_x + KI + HC$

$= K_x + (l/2) \cos \theta + (w/2) \sin \theta$

---

$y$-coordinate of C:

$K_y + HI$

$= K_y + GI - GH$

$= K_y + (l/2) \sin \theta - (w/2) \cos \theta$

## Finding the coordinates of A and D
Note that:

- A mirrors C
- D mirrors B
- Mirroring is along both the $x$ and $y$ axes
- $(x_0, y_0)$ is the mirror pivot

Hence...

---

$x$-coordinate of D:

$K_x - (- (w/2) \sin \theta + (l/2) \cos \theta)$

$= K_x + (w/2) \sin \theta - (l/2) \cos \theta$

---

$y$-coordinate of D:

$K_y - ((l/2) \sin \theta + (w/2) \cos \theta)$

$= K_y - (l/2) \sin \theta - (w/2) \cos \theta$

---

$x$-coordinate of A:

$K_x - ((l/2) \cos \theta + (w/2) \sin \theta)$

$= K_x - (l/2) \cos \theta - (w/2) \sin \theta$

---

$y$-coordinate of A:

$K_y - ((l/2) \sin \theta - (w/2) \cos \theta)$

$= K_y - (l/2) \sin \theta + (w/2) \cos \theta$

---

Hence, we have found the coordinates of each of A, B, C and D, and thereby have found the coordinates of the corners of ABCD required to maintain an orientation from $(x_0, y_0)$ to $(x_1, y_1)$.

# Organising the results
Some reordering of the terms is done to have sines and cosines in the same places. This helps see a pattern more clearly, if there is any. Also, the signs are placed within the multipliers, further helping reveal any underlying pattern. This pattern can then result in efficient and elegant code.

---

| Point | $x$-coordinate | $y$-coordinate |
| --- | --- | --- |
| A | $K_x + (-l/2) \cos \theta + (-w/2) \sin \theta$ | $K_y + (w/2) \cos \theta + (-l/2) \sin \theta$ |
| B | $K_x + (l/2) \cos \theta + (-w/2) \sin \theta$ | $K_y + (w/2) \cos \theta + (l/2) \sin \theta$ |
| C | $K_x + (l/2) \cos \theta + (w/2) \sin \theta$ | $K_y + (-w/2) \cos \theta + (l/2) \sin \theta$ |
| D | $K_x + (-l/2) \cos \theta + (w/2) \sin \theta$ | $K_y + (-w/2) \cos \theta + (-l/2) \sin \theta$ |

# Implementation
**NOTE**: _The actual implementation may differ in specifics._

First, note the following:

- `agent_x` = $K_x$
- `agent_y` = $K_y$
- Agent orientation angle refers to $\theta$
- Some program-specific details are abstracted via elipses (...)

---

```python
agent_x = ...
agent_y = ...

# Calculate agent orientation angle's sine and cosine:
delta_x = end_x - start_x
delta_y = end_y - start_y
h = np.sqrt(delta_x**2 + delta_y**2)
cos_theta = delta_x / h
sin_theta = delta_y / h

#------------------------------------
# CHANGE AGENT ORIENTATION

half_length = agent_dims["length"] / 2
half_width = agent_dims["width"] / 2

# Agent corners, given rightward orientation and centre (0,0):
corners = [
    (-half_length, -half_width),
    (half_length, -half_width),
    (half_length, half_width),
    (-half_length, half_width)]

# Leverage the pattern identifiable before for an elegant loop:
rotated_corners = [
    (
        agent_x + x * cos_theta - y * sin_theta,
        agent_y + x * sin_theta + y * cos_theta,
    )
    for x, y in corners]
```