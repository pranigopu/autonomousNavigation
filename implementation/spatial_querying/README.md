<h1>SPATIAL QUERYING</h1>

---

Click [here](./tests.ipynb) to see the associated Jupyter Notebook.

# About
Spatial querying refers to seeking and retrieving information about the environment, such as:

- Cell coordinates for a cell position
- Cell positions within a specified cluster
- Corner coordinates for a set or cluster of cell positions
- Overlaps between figures within the environment

---

> **Key theoretical references**:
>
> - [*Collision Detection*, **Autonomous Navigation**, **pranigopu.github.io**](https://pranigopu.github.io/autonomous-navigation/collision-detection.html)
> - [*Overlap Detection for Straight-Edged Convex Figures*, **Autonomous Navigation**, **pranigopu.github.io**](https://pranigopu.github.io/autonomous-navigation/overlap-detection-for-straight-edged-convex-figures.html)

# Purpose
Spatial querying forms the framework for collision detection and avoidance, useful for:

- Path planning
- Dynamic navigation

# Contents
- [`figure_overlap_detection`](./figure_overlap_detection/): *Codes for straight-edged convex figure overlap detection*
- [`multiple_grid_cell_corner_coords_retrieval`](./multiple_grid_cell_corner_coords_retrieval)
- [`axis_aligned_bbox_for_box.py`](./axis_aligned_bbox_for_box.py): *Code to identify an axis-aligned bounding box minimally covering a figure*
- [`grid_cell_cluster_filtering_for_obstacles.py`](./grid_cell_cluster_filtering_for_obstacles.py): *Code to filter grid cell clusters for obstacle-containing cells*
- [`grid_cell_positions_gen.py`](./grid_cell_positions_gen.py): *Code to generate cell positions corresponding to an index range*
- [`tests.ipynb`](./tests.ipynb): *Jupyter Notebook presenting tests for all the above*
