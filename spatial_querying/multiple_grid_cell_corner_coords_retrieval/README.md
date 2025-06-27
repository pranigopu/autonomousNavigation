<h1>MULTIPLE GRID CELL CORNER COORDINATES RETRIEVAL</h1>

---

# About
This set of programs aims to retreive the corner coordinates of multiple grid cells together.

# Purpose
This is useful in collision detection, since it forms the basis of checking whether an agent overlaps with any obstacle grids around it.

# Contents
- [`display_functionality.py`](./display_functionality.py): *Functionality for displaying results*
- [`input_grid_positions_list.py`](./input_grid_positions_list.py): *Code for retrieving corner coordinates of a list of positions*
- [`input_grid_position_cluster.py`](./input_grid_position_cluster.py): *Code for retrieving corner coordinates for index ranges (cell clusters)*
- [`input_grid_position_cluster_optimised.py`](./input_grid_position_cluster_optimised.py): *The above but optimised using NumPy arrays*
