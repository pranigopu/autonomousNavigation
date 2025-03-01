import numpy as np

#================================================
def get_edges(corners:np.ndarray):
    '''
    Gets 2 mutually perpendicular edges from the figure's corners.

    ---

    PARAMETERS:
    - `corners` (np.ndarray): Corner coordinates

    RETURNS:
    - (list[np.ndarray): Edges

    ---

    NOTE: Each edge is represented as a vector connecting the 2 corners.
    '''
    
    num_corners = len(corners)
    return [corners[i] - corners[(i + 1) % num_corners] for i in range(num_corners)]

#================================================
def project_to_axis(corners, axis):
    '''
    Projects a figure (whose corners are given) onto the given axis.

    ---

    PARAMETERS:
    - `corners` (np.ndarray): Corner coordinates of a figure

    RETURNS:
    - (tuple[np.ndarray): Minimum and maximum projections \n
      This obtains the extremeties of the figure's projection
    '''
    
    projections = [np.dot(corner, axis) for corner in corners]
    return min(projections), max(projections)

#================================================
def get_axes(edges:np.ndarray):
    '''
    Get unit vectors (axes) parallel to edges.

    Hence, it is just a function that normalises given edge vectors.

    ---

    PARAMETERS:
    - `edges` (np.ndarray): Edges

    RETURNS:
    - (np.ndarray): Normalised edges
    '''

    return edges / np.linalg.norm(edges, axis=1, keepdims=True)
    # NOTE: The above essentially divides each edge vector by its magnitude, i.e. by the Euclidean distance between its endpoints

#================================================
# PAIRWISE OVERLAP DETECTION

def detect_overlap(fig1_corner_coords:np.ndarray, fig2_corner_coords:np.ndarray) -> bool:
    '''
    Detects if an overlap exists between 2 figures.

    ---

    PARAMETERS:
    - `fig1_corner_coords` (np.ndarray): Fig 1's corners's coordinates
    - `fig2_corner_coords` (np.ndarray): Fig 2's corners's coordinates

    RETURNS:
    - (bool): True if overlapping, False if not
    '''
    
    fig1_edges = get_edges(fig1_corner_coords)
    fig2_edges = get_edges(fig2_corner_coords)
    axes = get_axes(fig1_edges + fig2_edges)

    for axis in axes:
        fig1_min, fig1_max = project_to_axis(fig1_corner_coords, axis)
        fig2_min, fig2_max = project_to_axis(fig2_corner_coords, axis)

        if fig1_max < fig2_min or fig2_max < fig1_min:
            return False
    return True

#================================================
# MULTIPLE OVERLAP DETECTION

def detect_overlapping_figs(figs:list[str, np.ndarray], target_corners:np.ndarray):
    '''
    Find figures that overlap with the target figure.

    ---

    PARAMETERS:
    - `figs` (list[str, np.ndarray]): List of figures; for each entry:
        - The 1st element is the figure label
        - The 2nd element is the figure's corners' coordinates
    - `target_corners` (np.ndarray): Target's corners's coordinates
    
    RETURNS:
    - (list[str]): List of labels of figures overlapping with target
    '''
    
    overlapping_labels = []
    
    # Compute target rectangle edges and axes:
    target_edges = get_edges(target_corners)
    target_axes = get_axes(target_edges)
    
    for label, fig_corners in figs:
        # Combine target and current rectangle axes:
        fig_edges = get_edges(fig_corners)
        fig_axes = get_axes(fig_edges)
        
        # Collect axes for Separating Axis Theorem check:
        # NOTE: The pairwise overlap detection function also uses the same theorem, of course
        axes = np.vstack((target_axes, fig_axes))
        
        # Check for overlaps on all axes:
        has_separating_axis = False
        for axis in axes:
            fig_min, fig_max = project_to_axis(fig_corners, axis)
            target_min, target_max = project_to_axis(target_corners, axis)
            if fig_max < target_min or target_max < fig_min:
                has_separating_axis = True
                break
        
        if not has_separating_axis:
            overlapping_labels.append(label)
    
    return overlapping_labels