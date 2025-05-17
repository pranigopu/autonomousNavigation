<h1>FIGURE OVERLAP DETECTION</h1>

---

Click [here](../tests.ipynb) to see the associated Jupyter Notebook.

# About
A set of codes to test and implement a mechanism to detect overlaps between a straight-edged figure (1D or 2D) and one or more other straight-edged figures (1D or 2D). The implementation must be able to account for any size, shape and orientation the figures may be in. Note that the most important use-case is for rectangles. However, the solution has been generalised for all straight-edged figures due to the following:

- It is relatively easy to extend the logic
- Makes the code extensible <br> _Especially if we want polygonal figures (e.g. agents and objects)_

That being said, almost all the testing is done for rectangles.

# Contents
**Functionality-providing codes**:

- [`core_functionality.py`](./core_functionality.py)

**Test cases**:

- [`single_test_case.py`](./single_test_case.py)
- [`randomised_test_cases.py`](./randomised_test_cases.py)
- [`systematic_test_cases.py`](./systematic_test_cases.py)
- [`multi_fig_overlap.py`](./multi_fig_overlap.py)

# Possible simplification for rectangles
For making use of the Separating Axis Theorem, what we need are axes parallel to _each_ edge of the figure. However, for a rectangle, its edges exist in parallel pairs, which means only the axes parallel to any 2 adjacent edges are needed. However, in the current implementation, for the sake of generalisability (and because the performance difference is probably negligible), I am not implementing this simplification.
