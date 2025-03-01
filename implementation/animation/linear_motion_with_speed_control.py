import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Initial parameters
default_frames = 1000  # Default number of animation steps
ms_per_step = 50  # ms/step for updates
increment_per_step = 2  # increment/step for updates

# Key parameter to register stop buttom clicks:
stopped = False

# App layout
app.layout = html.Div([
    dcc.Graph(
        id='warehouse-layout',
        style={'height': '80vh'}
    ),
    html.Div([
        html.Button('Start Simulation', id='start-button', n_clicks=0),
        html.Button('Stop Simulation', id='stop-button', n_clicks=0, style={'margin-left': '10px'}),
        html.Br(),
        html.Br(),
        html.Label("Start Point (x, y):"),
        dcc.Input(id='start-x', type='number', value=2, step=0.1),
        dcc.Input(id='start-y', type='number', value=3, step=0.1),
        html.Label("End Point (x, y):"),
        dcc.Input(id='end-x', type='number', value=8, step=0.1),
        dcc.Input(id='end-y', type='number', value=7, step=0.1),
        html.Br(),
        html.Label("Layout Dims:"),
        dcc.Input(id='layout-width', type='number', value=10, step=0.1),
        dcc.Input(id='layout-height', type='number', value=10, step=0.1),
        html.Label("Agent Dims:"),
        dcc.Input(id='agent-width', type='number', value=1, step=0.1),
        dcc.Input(id='agent-height', type='number', value=2, step=0.1),
        html.Br(),
        html.Label("Interval Increment (increment/step):"),
        dcc.Slider(
            id='increment-slider',
            min=1, max=50, step=1, value=increment_per_step,
            marks={i: f'{i}' for i in range(5, 51, 5)}
        ),
        html.Label("Interval Size (ms/step):"),
        dcc.Slider(
            id='size-slider',
            min=10, max=100, step=10, value=ms_per_step,
            marks={i: f'{i}' for i in range(10, 101, 10)}
        ),
    ], style={'margin': '20px'}),
    dcc.Interval(id='interval', interval=ms_per_step, n_intervals=0, disabled=True),
    html.Output(id='stop', hidden=True)
])


# Function to ensure that the stop button is registered at any point:
@app.callback(Output('stop', 'hidden'), [Input('stop-button', 'n_clicks')])
def stop_sim(stop_clicks):
    global stopped
    stopped = True
    return True

@app.callback(
    [Output('warehouse-layout', 'figure'),
     Output('interval', 'interval'),
     Output('interval', 'n_intervals'),
     Output('interval', 'disabled')],
    [Input('start-button', 'n_clicks'),
     Input('interval', 'n_intervals')],
    [State('layout-width', 'value'),
     State('layout-height', 'value'),
     State('agent-width', 'value'),
     State('agent-height', 'value'),
    State('start-x', 'value'),
     State('start-y', 'value'),
     State('end-x', 'value'),
     State('end-y', 'value'),
     State('increment-slider', 'value'),
     State('size-slider', 'value')]
)
def update_simulation(start_clicks, n_intervals, lw, lh, aw, ah, sx, sy, ex, ey, increment, ms):
    global stopped
    
    ctx = dash.callback_context

    # Identify which input triggered the callback
    triggered_id = ctx.triggered_id

    # Initialise variables
    frames = default_frames
    path_x = np.linspace(sx, ex, frames)
    path_y = np.linspace(sy, ey, frames)

    # Start simulation
    if triggered_id == 'start-button':
        stopped = False
        figure = go.Figure(layout=go.Layout(title="Warehouse Agent Movement: Running", xaxis=dict(range=[0, lw], title="X-axis"), yaxis=dict(range=[0, lh], title="Y-axis", scaleanchor="x", scaleratio=1)))
        return figure, ms, 0, False

    # Stop simulation
    if stopped or triggered_id == 'stop-button':
        figure = go.Figure(layout=go.Layout(title="Warehouse Agent Movement: Stopped", xaxis=dict(range=[0, lw], title="X-axis"), yaxis=dict(range=[0, lh], title="Y-axis", scaleanchor="x", scaleratio=1)))
        return figure, ms, 0, True

    # Update agent position during simulation
    if triggered_id == 'interval' and n_intervals < frames:
        agent_x = path_x[n_intervals]
        agent_y = path_y[n_intervals]
        if aw is None:
            aw = 0
        if ah is None:
            ah = 0
        # Define rectangle (agent) vertices
        agent_rect = {
            'type': 'rect',
            'x0': agent_x - aw / 2,
            'x1': agent_x + aw / 2,
            'y0': agent_y - ah / 2,
            'y1': agent_y + ah / 2,
            'line': {'color': 'blue'},
            'fillcolor': 'blue',
            'opacity': 0.7,
        }

        # Create figure
        figure = go.Figure(layout=go.Layout(title="Warehouse Agent Movement: Running", xaxis=dict(range=[0, lw], title="X-axis"), yaxis=dict(range=[0, lh], title="Y-axis", scaleanchor="x", scaleratio=1), shapes=[agent_rect]))
        return figure, ms, n_intervals + increment, False

    # Stop simulation when it reaches the end
    stopped = True
    return go.Figure(), ms, 0, True

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)