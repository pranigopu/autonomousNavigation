from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import math

app = Dash(__name__)

app.layout = html.Div([
    html.H4("Rotate a Rectangle"),
    dcc.Slider(0, 360, step=1, value=0, id='angle-slider', marks={0: '0°', 90: '90°', 180: '180°', 270: '270°', 360: '360°'}),
    dcc.Graph(id='rotating-rectangle', config={'displayModeBar': False}),
])

def get_rotated_rectangle(angle):
    """
    Compute the coordinates of a rectangle rotated by a given angle.
    :param angle: Rotation angle in degrees
    :return: SVG path string for the rotated rectangle
    """
    # Rectangle dimensions
    half_width = 1
    half_height = 0.5

    # Rectangle corners before rotation
    corners = [
        (-half_width, -half_height),  # Bottom-left
        (half_width, -half_height),  # Bottom-right
        (half_width, half_height),   # Top-right
        (-half_width, half_height),  # Top-left
    ]

    # Convert angle to radians
    theta = math.radians(angle)

    # Rotate corners
    rotated_corners = [
        (
            x * math.cos(theta) - y * math.sin(theta),
            x * math.sin(theta) + y * math.cos(theta)
        )
        for x, y in corners
    ]

    # Construct SVG path
    path = (
        f"M {rotated_corners[0][0]} {rotated_corners[0][1]} "
        f"L {rotated_corners[1][0]} {rotated_corners[1][1]} "
        f"L {rotated_corners[2][0]} {rotated_corners[2][1]} "
        f"L {rotated_corners[3][0]} {rotated_corners[3][1]} Z"
    )

    return path

@app.callback(
    Output('rotating-rectangle', 'figure'),
    Input('angle-slider', 'value')
)
def update_rectangle(angle):
    # Get the rotated rectangle path
    rectangle_path = get_rotated_rectangle(angle)

    # Define the rectangle as a shape
    rectangle = {
        "type": "path",
        "path": rectangle_path,
        "line": {"color": "blue"},
        "fillcolor": "lightblue",
        "opacity": 0.7,
    }

    # Create the figure
    fig = go.Figure()
    fig.add_shape(rectangle)
    fig.update_layout(
        title=f"Rectangle Rotated by {angle}°",
        xaxis={"range": [-2, 2], "title": "X-axis"},
        yaxis={"range": [-2, 2], "title": "Y-axis", "scaleanchor": "x", "scaleratio": 1},
        height=600,
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
