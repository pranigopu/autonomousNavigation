import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import random
import time

# Dash app setup
app = dash.Dash(__name__)

# Number of agents
N_AGENTS = 5
MAX_WAYPOINTS = 20  # Maximum waypoints per agent
STEP_SIZE = 0.05  # Movement step size

# Generate initial random paths
def generate_path():
    return 10 * np.random.rand(np.random.randint(2, MAX_WAYPOINTS), 2)

def generate_agents():
    return [{'path': generate_path(), 'index': 0} for _ in range(N_AGENTS)]

agents = generate_agents()

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
    global agents
    
    traces = []
    status_texts = []
    for i, agent in enumerate(agents):
        path = agent['path']
        index = agent['index']
        
        # Move agent along the path
        if index < len(path) - 1:
            agent['index'] += 1
        else:
            agent['path'] = generate_path()  # New path when finished
            agent['index'] = 0
        
        pos = path[agent['index']]
        traces.append(go.Scatter(x=[pos[0]], y=[pos[1]], mode='markers', marker=dict(size=10), name=f'Agent {i}'))
        status_texts.append(f'Agent {i}: Progress {agent["index"]}/{len(agent["path"])}')
    
    figure = go.Figure(traces)
    figure.update_layout(title='Multi-Agent Movement', xaxis=dict(range=[-1, 11]), yaxis=dict(range=[-1, 11]))
    
    return figure, '\n'.join(status_texts)

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
