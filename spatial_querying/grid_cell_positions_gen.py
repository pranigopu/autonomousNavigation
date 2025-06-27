import numpy as np

def generate_index_pairs(i_1: int, i_2: int, j_1: int, j_2: int) -> np.ndarray:
    '''
    Generate an array of all pairs (i, j) for given ranges i_1:i_2 and j_1:j_2.

    Args:
    - `i_1` (int): Start of the range for i (inclusive)
    - `i_2` (int): End of the range for i (exclusive)
    - `j_1` (int): Start of the range for j (inclusive)
    - `j_2` (int): End of the range for j (exclusive)

    Returns:
    - (np.ndarray): Array of shape (N, 2) where N is the no. of pairs
    '''
    i_values = np.arange(i_1, i_2)
    j_values = np.arange(j_1, j_2)

    # Efficiently form all combinations using broadcasting
    i_grid, j_grid = np.meshgrid(i_values, j_values, indexing='ij')
    pairs = np.stack([i_grid.ravel(), j_grid.ravel()], axis=-1)
    return pairs


# Example Usage
pairs = generate_index_pairs(0, 3, 2, 5)
print("Generated pairs:")
print(pairs)