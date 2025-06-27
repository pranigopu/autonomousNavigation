import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import random
import time

# Dash app setup
app = dash.Dash(__name__)

# Number of waypoints and movement parameters
N_WAYPOINTS = 5  # Key waypoints
STEP_DIVISIONS = 10  # Number of steps per line segment
STEP_SIZE = 0.05  # Movement step size

# Generate initial random path
def generate_path():
    waypoints = np.cumsum(np.random.randn(N_WAYPOINTS, 2), axis=0)  # Main waypoints
    path = []
    for i in range(len(waypoints) - 1):
        segment = np.linspace(waypoints[i], waypoints[i + 1], STEP_DIVISIONS)
        path.extend(segment)
    return np.array(path)

# Initialize single agent
agent = {'path': generate_path(), 'index': 0, 'wait_time': 0, 'waiting': False}

# Layout
app.layout = html.Div([
    dcc.Graph(id='live-graph', style={'height': '80vh'}),
    dcc.Interval(id='interval', interval=100, n_intervals=0),  # Update every 100ms
    html.Pre(id='agent-status', style={'white-space': 'pre-wrap'})
])

# Update function
@app.callback(
    [Output('live-graph', 'figure'), Output('agent-status', 'children')],
    Input('interval', 'n_intervals')
)
def update_graph(n):
    global agent
    
    path = agent['path']
    index = agent['index']
    
    # Handle waiting
    if agent['waiting']:
        agent['wait_time'] -= 1
        if agent['wait_time'] <= 0:
            agent['waiting'] = False
    else:
        # Move agent along the path
        if index < len(path) - 1:
            agent['index'] += 1
            
            # If reached a waypoint, initiate a random wait
            if agent['index'] % STEP_DIVISIONS == 0:
                agent['waiting'] = True
                agent['wait_time'] = random.randint(5, 20)  # Random wait time
        else:
            agent['path'] = generate_path()  # New path when finished
            agent['index'] = 0
    
    pos = path[agent['index']]
    trace = go.Scatter(x=[pos[0]], y=[pos[1]], mode='markers', marker=dict(size=10), name='Agent')
    
    figure = go.Figure([trace])
    figure.update_layout(title='Single Agent Movement', xaxis=dict(range=[-10, 10]), yaxis=dict(range=[-10, 10]))
    
    status_text = f'Agent Progress: {agent["index"]}/{len(agent["path"])} - Waiting: {agent["waiting"]}'
    
    return figure, status_text

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
