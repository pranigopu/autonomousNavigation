from dash import Dash, html, dcc, Input, Output, State
import plotly.graph_objs as go
import numpy as np

app = Dash(__name__)

# Layout
app.layout = html.Div([
    dcc.Input(id="coords-seq", type="text", placeholder="Enter coordinate sequence"),
    html.Button("Start/Stop", id="start-stop-button"),
    dcc.Slider(id="increment-slider", min=1, max=50, step=1, value=2, marks={i: f'{i}' for i in range(1, 51, 2)}),
    dcc.Slider(id="time-gap-slider", min=10, max=500, step=1, value=50, marks={i: f'{i}' for i in range(10, 501, 10)}),
    dcc.Slider(id="num-frames-slider", min=50, max=1000, step=1, value=200, marks={i: f'{i}' for i in range(50, 1001, 50)}),
    dcc.Store(id="store-stop-status", data=True),
    dcc.Store(id="store-coords-seq"),
    dcc.Store(id="store-path"),
    dcc.Store(id="store-agent-shape"),
    dcc.Store(id="store-index-for-coords-seq", data=0),
    dcc.Store(id="store-layout-dims", data={"width": 10, "height": 10}),
    dcc.Store(id="store-agent-dims", data={"width": 2, "height": 1}),
    dcc.Interval(id="interval", interval=1000, n_intervals=0, disabled=True),
    dcc.Graph(id="warehouse-layout", figure=go.Figure()),
])

# Update coordinate sequence
@app.callback(
    Output("store-coords-seq", "data"),
    Input("coords-seq", "value"),
    prevent_initial_call=True)
def update_coords_seq(coords_seq):
    try:
        coords = [tuple(map(float, pair.split(','))) for pair in coords_seq.split('|')]
        return coords
    except Exception:
        raise ValueError("Invalid format. Use x,y|x,y|...")

# Toggle simulation start/stop and manage interval
@app.callback(
    [Output("store-stop-status", "data", allow_duplicate=True),
     Output("interval", "disabled", allow_duplicate=True)],
    Input("start-stop-button", "n_clicks"),
    State("store-stop-status", "data"),
    prevent_initial_call=True)
def toggle_simulation(_, stop_status):
    new_status = not stop_status
    return new_status, new_status

# Update simulation
@app.callback(
    [Output("warehouse-layout", "figure"),
     Output("store-path", "data"),
     Output("store-agent-shape", "data"),
     Output("store-index-for-coords-seq", "data"),
     Output("interval", "n_intervals"),
     Output("interval", "interval"),
     Output("interval", "disabled"),
     Output("store-stop-status", "data")],
    [Input("interval", "n_intervals")],
    [State("store-coords-seq", "data"),
     State("store-path", "data"),
     State("store-agent-shape", "data"),
     State("increment-slider", "value"),
     State("time-gap-slider", "value"),
     State("num-frames-slider", "value"),
     State("store-index-for-coords-seq", "data"),
     State("store-layout-dims", "data"),
     State("store-agent-dims", "data"),
     State("store-stop-status", "data"),
     State("warehouse-layout", "figure")]
)
def update_simulation(
    n_intervals,
    coords_seq,
    path,
    agent_shape,
    di,
    dt,
    num_frames,
    index_for_coords_seq,
    layout_dims,
    agent_dims,
    stop_status,
    stored_fig):
    stop_return = (stored_fig, path, agent_shape, 0, 0, dt, True, True)

    if stop_status or not coords_seq:
        return stop_return

    if index_for_coords_seq >= len(coords_seq) - 1:
        return stop_return

    if n_intervals >= num_frames - 1:
        index_for_coords_seq += 1
        n_intervals = 0

    # Calculate agent path
    try:
        start_x, end_x = coords_seq[index_for_coords_seq][0], coords_seq[index_for_coords_seq + 1][0]
        start_y, end_y = coords_seq[index_for_coords_seq][1], coords_seq[index_for_coords_seq + 1][1]
    except IndexError:
        return stop_return

    path_x = np.linspace(start_x, end_x, num_frames)
    path_y = np.linspace(start_y, end_y, num_frames)

    # Current agent position
    agent_x = path_x[min(n_intervals, len(path_x) - 1)]
    agent_y = path_y[min(n_intervals, len(path_y) - 1)]

    # Calculate orientation angle's sine and cosine
    dx = end_x - start_x
    dy = end_y - start_y
    h = np.sqrt(dx**2 + dy**2)
    cosine_of_agent_angle = dx / h
    sine_of_agent_angle = dy / h

    # Rotate agent orientation
    half_width = agent_dims["width"] / 2
    half_height = agent_dims["height"] / 2

    # Relative coordinates of agent's bounding box corners, considering the agent's centre as the origin (0, 0):
    corners = [
        (-half_width, -half_height),
        (half_width, -half_height),
        (half_width, half_height),
        (-half_width, half_height),
    ]

    rotated_corners = [
        (
            agent_x + x * cosine_of_agent_angle - y * sine_of_agent_angle,
            agent_y + x * sine_of_agent_angle + y * cosine_of_agent_angle,
        )
        for x, y in corners]

    agent_shape = {
        "type": "path",
        "path": f"M {rotated_corners[0][0]} {rotated_corners[0][1]} "
                f"L {rotated_corners[1][0]} {rotated_corners[1][1]} "
                f"L {rotated_corners[2][0]} {rotated_corners[2][1]} "
                f"L {rotated_corners[3][0]} {rotated_corners[3][1]} Z",
        "line": {"color": "blue"},
        "fillcolor": "blue",
        "opacity": 0.7}

    # Update figure
    figure = go.Figure(
        layout=go.Layout(
            title="Warehouse Agent Movement",
            xaxis={"range": [0, layout_dims["width"]], "title": "X-axis"},
            yaxis={"range": [0, layout_dims["height"]], "title": "Y-axis", "scaleanchor": "x", "scaleratio": 1},
            shapes=[agent_shape]))

    return figure, {"x": path_x.tolist(), "y": path_y.tolist()}, agent_shape, index_for_coords_seq, n_intervals + di, dt, False, False

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
