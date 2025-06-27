import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Input(id='coordinate-input', type='text', placeholder="Enter coordinates as (x1, y1), (x2, y2), ..."),
    html.Button('Parse Coordinates', id='parse-button', n_clicks=0),
    html.Div(id='output-tuple')
])

# Callback to parse the input and display the numerical tuples
@app.callback(
    Output('output-tuple', 'children'),
    [Input('parse-button', 'n_clicks')],
    [State('coordinate-input', 'value')]
)
def parse_coordinates(n_clicks, coord_str):
    if coord_str is None or coord_str == '':
        return "Please enter valid coordinate tuples."
    
    # Split the input into individual tuples
    try:
        coords = [tuple(map(float, pair.split(','))) for pair in coord_str.split('|')]
        print(coords)
        return str(coords)
    except ValueError:
        return "Invalid format. Ensure input is in the form (x, y), (x, y), ..."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
