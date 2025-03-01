from dash import html, dcc, callback_context, Input, Output, State, Dash
import numpy as np
import plotly.graph_objects as go

#############################################################
# WAREHOUSE LAYOUT
#############################################################

# Parameters for warehouse layout:
warehouse_width = 40
warehouse_height = 30

# Generate basic layout elements:
shelves = [
    {'x': [5, 5, 10, 10], 'y': [5, 10, 10, 5]},  # Shelf 1
    {'x': [15, 15, 20, 20], 'y': [5, 10, 10, 5]}, # Shelf 2
    {'x': [5, 5, 10, 10], 'y': [15, 20, 20, 15]}, # Shelf 3
    {'x': [15, 15, 20, 20], 'y': [15, 20, 20, 15]} # Shelf 4
]

obstacles = [
    {'x': [25, 25, 28, 28], 'y': [8, 12, 12, 8]},  # Static obstacle 1
    {'x': [30, 30, 34, 34], 'y': [18, 22, 22, 18]} # Static obstacle 2
]

entry_points = [(2, 2), (2, 28)]  # Warehouse entry points
exit_points = [(38, 2), (38, 28)] # Warehouse exit points

# Define figure:
environment_layout_fig = go.Figure()

# Plot warehouse boundary:
environment_layout_fig.add_trace(go.Scatter(
    x=[0, warehouse_width, warehouse_width, 0, 0],
    y=[0, 0, warehouse_height, warehouse_height, 0],
    mode='lines',
    line=dict(color='black', width=2),
    name='Warehouse Boundary'))

# Plot shelves:
for shelf in shelves:
    environment_layout_fig.add_trace(go.Scatter(
        x=shelf['x'] + [shelf['x'][0]],
        y=shelf['y'] + [shelf['y'][0]],
        fill='toself',
        fillcolor='blue',
        mode='lines',
        line=dict(color='blue'),
        name='Shelf'))

# Plot obstacles:
for obstacle in obstacles:
    environment_layout_fig.add_trace(go.Scatter(
        x=obstacle['x'] + [obstacle['x'][0]],
        y=obstacle['y'] + [obstacle['y'][0]],
        fill='toself',
        fillcolor='red',
        mode='lines',
        line=dict(color='red'),
        name='Obstacle'))

environment_layout_fig.add_shape(type="rect", x0=0, y0=0, x1=0, y1=0)

# Set layout:
environment_layout_fig.update_layout(
    title='Simplified Warehouse Environment',
    xaxis=dict(title='X Coordinate', range=[0, warehouse_width]),
    yaxis=dict(title='Y Coordinate', range=[0, warehouse_height]),
    showlegend=True,
    width=800,
    height=600)

#############################################################
# NON-CALLBACK HELPERS
#############################################################

def get_new_path_and_related_params(start_x, end_x, start_y, end_y, num_frames, step, agent_dims):
    # Obtaining required x and y step sizes so that total step size equals `step`:
    delta_x = end_x - start_x
    delta_y = end_y - start_y
    length = np.sqrt(delta_x**2 + delta_y**2)
    x_step = step * delta_x / length
    y_step = step * delta_y / length
    '''
    REASONING FOR THE ABOVE:

    ---
    We must have x and y steps such that:

    x_step^2 + y_step^2 = step^2 ... (1)

    Furthermore, (x_step, y_step) should move the agent along the
    vector (delta_x, delta_y) at a constant rate. Hence, we have:
    
    x_step = k*delta_x and y_step = k*delta_y ... (2)

    ---
    Hence, from (1):

    k^2*delta_x^2 + k^2*delta_y^2 = step^2
    => k = sqrt(step^2 / (delta_x^2 + delta_y^2))
    => k = step / sqrt(delta_x^2 + delta_y^2)

    For convenience, put:
    
    length = sqrt(delta_x^2 + delta_y^2)
    => k = step / length

    ---
    Hence, we have:

    x_step
    = k*delta_x
    = (step / length) * delta_x
    = step * delta_x / length

    y_step
    = k*delta_y
    = (step / length) * delta_y
    = step * delta_y / length
    '''

    #------------------------------------
    # Set the path:

    # 1. Use `np.arange` to define the path between start and end points:
    path_x = np.arange(start_x, end_x, x_step)
    path_y = np.arange(start_y, end_y, y_step)

    # 2. Obtain the number of frames as the minimum length of the above two:
    # NOTE: This ensures that `path_x` and `path_y` are of the same size despite small precision issues (if any)
    num_frames = min(len(path_x), len(path_y))
    path_x = path_x[:num_frames]
    path_y = path_y[:num_frames]
    path = {'x': path_x.tolist(), 'y': path_y.tolist()}

    # 3. Calculate agent orientation angle's sine and cosine:
    cos_theta = delta_x / length
    sin_theta = delta_y / length

    #------------------------------------
    # Change agent orientation:

    # 1. Get the halves of the width and height of the agent's rectangle:
    w_by_2 = agent_dims["width"] / 2
    h_by_2 = agent_dims["height"] / 2

    # 2. Relative corners, given rightward orientation and centre (0,0):
    multipliers = [
        [-w_by_2, -h_by_2],
        [w_by_2, -h_by_2],
        [w_by_2, h_by_2],
        [-w_by_2, h_by_2]]
    agent_rect_relative_corners = [
        (
            x_mult * cos_theta - y_mult * sin_theta,
            x_mult * sin_theta + y_mult * cos_theta
        )
        for x_mult, y_mult in multipliers]
    
    return path, num_frames, agent_rect_relative_corners

#================================================
def get_figure_with_agent(agent_rect_corners, layout_dims):
    agent_shape = {
        "type": "path",
        "path": f"M {agent_rect_corners[0][0]} {agent_rect_corners[0][1]} "
                f"L {agent_rect_corners[1][0]} {agent_rect_corners[1][1]} "
                f"L {agent_rect_corners[2][0]} {agent_rect_corners[2][1]} "
                f"L {agent_rect_corners[3][0]} {agent_rect_corners[3][1]} Z",
        "line": {"color": "blue"},
        "fillcolor": "blue",
        "opacity": 0.7}
    
    environment_layout_fig["layout"]["shapes"][-1].update(agent_shape)
    return environment_layout_fig

#================================================
def get_figure_without_agent(layout_dims):
    environment_layout_fig["layout"]["shapes"][-1].update(type="rect", x0=0, y0=0, x1=0, y1=0)
    return environment_layout_fig

#############################################################
# LAYOUT
#############################################################

default_agent_width = 2
default_agent_height = 1
default_layout_width = 50
default_layout_height = 50

app = Dash(__name__)
app.layout = html.Div([
    # Coordinates sequence input:
    dcc.Input(id="coords-seq", type="text", placeholder="Enter coordinate sequence"),
    # Interactive controls:
    html.Button("Start/Pause", id="start-pause-button"),
    html.Button("Restart", id="restart-button"),
    html.Button("Reset", id="reset-button"),
    dcc.Slider(id="increment-slider", min=1, max=50, step=1, value=2, marks={i: f'{i}' for i in range(1, 51, 2)}),
    dcc.Slider(id="time-gap-slider", min=50, max=500, step=1, value=50, marks={i: f'{i}' for i in range(50, 501, 10)}),
    dcc.Slider(id="step-slider", min=0.05, max=1, step=0.05, value=0.1, marks={i: f'{i}' for i in range(0, 2, 1)}),
    # Status display:
    html.P(id="display-sim-status"),
    # Storage:
    dcc.Store(id="store-button-controlled-sim-status", data="stopped"),
    dcc.Store(id="store-interval-controlled-sim-status", data="stopped"),
    dcc.Store(id="store-coords-seq"),
    dcc.Store(id="store-path"),
    dcc.Store(id="store-num-frames", data=0),
    dcc.Store(id="store-index-for-coords-seq", data=0),
    dcc.Store(id="store-layout-dims", data={"width": default_layout_width, "height": default_layout_height}),
    dcc.Store(id="store-agent-dims", data={"width": default_agent_width, "height": default_agent_height}),
    dcc.Store(id="store-agent-rect-relative-corners"),
    # Interval component for automatic live updates:
    dcc.Interval(id="interval", interval=1000, n_intervals=0, disabled=True),
    # Graph to display the simulation in:
    dcc.Graph(id="warehouse-layout", figure=get_figure_without_agent({"width": default_layout_width, "height": default_layout_height}))])

#############################################################
# CALLBACK HELPER FUNCTIONS
#############################################################

# Update coordinate sequence:
@app.callback(
    Output("store-coords-seq", "data"),
    Input("coords-seq", "value"),
    prevent_initial_call=True)
def update_coords_seq(coords_seq):
    try:
        coords = [tuple(map(float, pair.split(','))) for pair in coords_seq.split('|')]
        return coords
    except Exception:
        print("Invalid format. Use x,y|x,y|...")

#================================================
@app.callback(
    [Output("display-sim-status", "children"),
     Output("store-button-controlled-sim-status", "data")],
    [Input("store-button-controlled-sim-status", "data"),
     Input("store-interval-controlled-sim-status", "data")])
def display_sim_status(bc_sim_status, ic_sim_status):
    if ic_sim_status == "ended":
        bc_sim_status = "ended"
    return f"Simulation Status = \"{bc_sim_status}\"", bc_sim_status

#================================================
# Toggle start/pause:
@app.callback(
    Output("store-button-controlled-sim-status", "data", allow_duplicate=True),
    Input("start-pause-button", "n_clicks"),
    State("store-button-controlled-sim-status", "data"),
    prevent_initial_call=True)
def toggle_simulation(_, sim_status):
    if sim_status == "running":
        new_status = "paused"
    else:
        new_status = "running"
    return new_status

#================================================
# Restart/reset simulation:
@app.callback(
    [Output("store-button-controlled-sim-status", "data", allow_duplicate=True),
     Output("store-num-frames", "data", allow_duplicate=True),
     Output("store-index-for-coords-seq", "data", allow_duplicate=True),
     Output("interval", "n_intervals", allow_duplicate=True)],
    [Input("restart-button", "n_clicks"),
     Input("reset-button", "n_clicks")],
    prevent_initial_call=True)
def restart_or_restart_simulation(_a, _b):
    ctx = callback_context
    triggered_id = ctx.triggered_id

    if triggered_id == "restart-button":
        return "running", 0, 0, 0
    if triggered_id == "reset-button":
        return "stopped", 0, 0, 0

#############################################################
# MAIN SIMULATION UPDATE FUNCTION
#############################################################

# Update simulation:
@app.callback(
    # OUTPUTS:
    [Output("warehouse-layout", "figure"),
     Output("store-agent-rect-relative-corners", "data"),
     #............
     Output("store-path", "data"),
     Output("store-num-frames", "data", allow_duplicate=True),
     Output("store-index-for-coords-seq", "data", allow_duplicate=True),
     #............
     Output("store-interval-controlled-sim-status", "data"),
     #............
     Output("interval", "n_intervals"),
     Output("interval", "interval"),
     Output("interval", "disabled")],
    
    # INPUTS:
    [Input("interval", "n_intervals"),
     Input("start-pause-button", "n_clicks")],
    
    # STATES:
    [State("store-coords-seq", "data"),
     State("store-path", "data"),
     #............
     State("increment-slider", "value"),
     State("time-gap-slider", "value"),
     State("step-slider", "value"),
     State("store-num-frames", "data"),
     #............
     State("store-index-for-coords-seq", "data"),
     State("store-layout-dims", "data"),
     State("store-agent-dims", "data"),
     State("store-button-controlled-sim-status", "data"),
     #............
     State("warehouse-layout", "figure"),
     State("store-agent-rect-relative-corners", "data")],
     prevent_initial_call=True)
def update_simulation(
    # INPUTS:
    n_intervals,
    n_clicks,
    
    # STATES:
    coords_seq,
    path,
    #............
    di,
    dt,
    step,
    num_frames,
    #............
    index,
    layout_dims,
    agent_dims,
    sim_status,
    #............
    fig,
    agent_rect_relative_corners):

    #------------------------------------
    # SETTING UP INDICATORS

    # Early return flag:
    early_return = False
    '''
    The purpose of using an "early return" flag is to avoid excessive
    return statements, especially due to the high number of returns.
    '''

    # Set the "disabled" indicator:
    disabled = False
    # NOTE: This is associated with the interval component

    #------------------------------------
    # IN CASE OF START BUTTON PRESS

    # Identify which input triggered the callback:
    ctx = callback_context
    triggered_id = ctx.triggered_id

    if triggered_id == "start-pause-button":
        sim_status, early_return = "running", True

    #------------------------------------
    # CHECK SIMULATION STOP/EARLY RETURN CONDITIONS
    
    if sim_status == "stopped":
        fig, disabled = get_figure_without_agent(layout_dims), True
    if sim_status != "running":
        disabled = True
    if coords_seq is None or index >= len(coords_seq) - 1:
        sim_status, disabled = "ended", True

    # If the interval component has to be disabled now, do not progress any further:
    if disabled:
        early_return = True
    
    #------------------------------------
    # Run the following if `early_return` is `False`...

    is_new_path = False
    
    if not early_return:
        #________________________
        # RESET INTERVAL COUNTER IF IT EXCEEDS ITS LIMIT
        if num_frames == 0:
            is_new_path = True
        elif n_intervals >= num_frames - 1:
            index += 1
            is_new_path = True
            n_intervals = 0

        #________________________
        # IDENTIFY PATH

        # Calculate agent path:
        try:
            start_x, end_x = coords_seq[index][0], coords_seq[index + 1][0]
            start_y, end_y = coords_seq[index][1], coords_seq[index + 1][1]
        except IndexError:
            early_return = True 
        
        #________________________
        # CREATE NEW PATH IF REQUIRED
        
        if is_new_path and not early_return:
            path, num_frames, agent_rect_relative_corners = get_new_path_and_related_params(start_x, end_x, start_y, end_y, num_frames, step, agent_dims)

    #------------------------------------
    # Return the following if `early_return` is true...

    if early_return:
        return fig, agent_rect_relative_corners, path, num_frames, index, sim_status, n_intervals, dt, disabled

    #------------------------------------
    # IDENTIFY CURRENT POSITION AND ORIENTATION

    # Current agent position:
    agent_x = path['x'][min(n_intervals, num_frames - 1)]
    agent_y = path['y'][min(n_intervals, num_frames - 1)]
    n_intervals += di

    # Fix current rectangle corner coordinates, as per current position and orientation:
    agent_rect_corners = [(agent_x + x, agent_y + y) for x, y in agent_rect_relative_corners]

    #------------------------------------
    # UPDATE FIGURE WITH AGENT
    
    fig = get_figure_with_agent(agent_rect_corners, layout_dims)

    return fig, agent_rect_relative_corners, path, num_frames, index, sim_status, n_intervals, dt, disabled

#================================================
# Run the app:
if __name__ == "__main__":
    app.run_server(debug=True)