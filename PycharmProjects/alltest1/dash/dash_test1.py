import dash
from dash import dcc
from dash import html
import numpy

x = numpy.linspace(0, 2 * numpy.pi, 100)
y = 10 * 2 * numpy.cos(x)

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='Testme'),
    dcc.Graph(
        id='curve',
        figure={
            'data': [
                {'x': x, 'y': y, 'type': 'Scatter', 'name': 'Testme'},
            ],
            'layout': {
                'title': 'Test Curve'
            }})
])

if __name__ == '__main__':
    app.run_server(debug=True)