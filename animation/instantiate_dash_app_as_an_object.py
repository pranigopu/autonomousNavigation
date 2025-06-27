import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

class MyDashApp:
    def __init__(self, title="Dynamic Dash App", interval=1000):
        self.title = title
        self.interval = interval
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):
        """Set up the layout of the app"""
        self.app.layout = html.Div([
            html.H1(self.title),
            dcc.Graph(id='graph'),
            dcc.Interval(
                id='interval-update',
                interval=self.interval,  # Update every `interval` milliseconds
                n_intervals=0
            )
        ])

    def setup_callbacks(self):
        """Define the callbacks for the app"""
        @self.app.callback(
            Output('graph', 'figure'),
            Input('interval-update', 'n_intervals')
        )
        def update_graph(n_intervals):
            # Example update function: updates the data in the graph
            return {
                'data': [
                    go.Scatter(
                        x=[n_intervals, n_intervals + 1],
                        y=[n_intervals, n_intervals + 2],
                        mode='lines+markers'
                    )
                ]
            }

    def run(self):
        """Run the Dash app"""
        self.app.run_server(debug=True)

# Create and run the app
if __name__ == '__main__':
    app_instance = MyDashApp(title="Custom Dash App", interval=500)
    app_instance.run()
