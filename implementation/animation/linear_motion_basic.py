import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Define layout dimensions
layout_width = 10
layout_height = 10

# Initial parameters
start_point = [2, 3]
end_point = [8, 7]
agent_width = 1
agent_height = 2
frames = 100  # Number of animation steps

# Generate the agent's path
path_x = np.linspace(start_point[0], end_point[0], frames)
path_y = np.linspace(start_point[1], end_point[1], frames)

# Create the app layout
app.layout = html.Div([
    dcc.Graph(
        id='warehouse-layout',
        style={'height': '80vh'}
    ),
    html.Div([
        html.Label("Start Point (x, y):"),
        dcc.Input(id='start-x', type='number', value=start_point[0], step=0.1),
        dcc.Input(id='start-y', type='number', value=start_point[1], step=0.1),
        html.Label("End Point (x, y):"),
        dcc.Input(id='end-x', type='number', value=end_point[0], step=0.1),
        dcc.Input(id='end-y', type='number', value=end_point[1], step=0.1),
        html.Button('Update', id='update-button', n_clicks=0)
    ], style={'margin': '20px'}),
    dcc.Interval(id='interval', interval=50, n_intervals=0)  # Animation interval
])

@app.callback(
    [Output('warehouse-layout', 'figure')],
    [Input('interval', 'n_intervals'),
     Input('update-button', 'n_clicks')],
    [dash.State('start-x', 'value'),
     dash.State('start-y', 'value'),
     dash.State('end-x', 'value'),
     dash.State('end-y', 'value')]
)
def update_agent(n_intervals, n_clicks, sx, sy, ex, ey):
    global path_x, path_y, frames
    
    if n_clicks > 0:
        # Update path when user changes start or end points
        path_x = np.linspace(sx, ex, frames)
        path_y = np.linspace(sy, ey, frames)
    
    # Determine current frame
    current_frame = min(n_intervals, frames - 1)
    
    # Compute agent position
    agent_x = path_x[current_frame]
    agent_y = path_y[current_frame]
    
    # Define rectangle (agent) vertices
    agent_rect = {
        'type': 'rect',
        'x0': agent_x - agent_width / 2,
        'x1': agent_x + agent_width / 2,
        'y0': agent_y - agent_height / 2,
        'y1': agent_y + agent_height / 2,
        'line': {'color': 'blue'},
        'fillcolor': 'blue',
        'opacity': 0.7,
    }
    
    # Create figure
    figure = go.Figure(
        layout=go.Layout(
            title="Warehouse Agent Movement",
            xaxis=dict(range=[0, layout_width], title="X-axis"),
            yaxis=dict(range=[0, layout_height], title="Y-axis", scaleanchor="x", scaleratio=1),
            shapes=[agent_rect]
        )
    )
    return [figure]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
