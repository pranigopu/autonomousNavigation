import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np

# Initialize app
app = dash.Dash(__name__)

# Environment parameters
layout_size = (10, 10)
agent_count = 10

# Initialize positions
positions = np.random.rand(agent_count, 2) * layout_size

# Update agent positions
def update_positions():
    global positions
    delta = np.random.uniform(-0.5, 0.5, size=positions.shape)
    positions += delta
    positions = np.clip(positions, 0, layout_size[0])
    return positions

# Layout
app.layout = html.Div([
    dcc.Graph(id='warehouse-simulation'),
    dcc.Interval(id='interval-component', interval=100, n_intervals=0)
])

# Callbacks
@app.callback(
    Output('warehouse-simulation', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    updated_positions = update_positions()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=updated_positions[:, 0],
        y=updated_positions[:, 1],
        mode='markers',
        marker=dict(size=15)
    ))
    fig.update_layout(
        xaxis=dict(range=[0, layout_size[0]]),
        yaxis=dict(range=[0, layout_size[1]]),
        title="Warehouse Simulation"
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
