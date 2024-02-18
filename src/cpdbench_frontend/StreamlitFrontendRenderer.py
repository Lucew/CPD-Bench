import pandas as pd
import subprocess
import json
from dash import Dash, html, dcc
import plotly.express as px

from cpdbench_frontend.FrontendRenderer import FrontendRenderer
from cpdbench.control import CPDFullResult


class StreamlitFrontendRenderer(FrontendRenderer):
    """Frontend renderer which renders the results using the Streamlit library.
    The interface is displayed in a web browser via a local web server.
    """

    def show_results(self, results: CPDFullResult) -> None:
        # subprocess.run("ls")
        app = Dash(__name__)

        # assume you have a "long-form" data frame
        # see https://plotly.com/python/px-arguments/ for more options
        df = pd.DataFrame({
            "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
            "Amount": [4, 1, 2, 2, 4, 5],
            "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
        })

        fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
        fig.write_html("test.html")

        app.layout = html.Div(children=[
            html.H1(children='Hello Dash'),

            html.Div(children='''
                Dash: A web application framework for your data.
            '''),

            dcc.Graph(
                id='example-graph',
                figure=fig
            )
        ])

        app.run(debug=True)


if __name__ == "__main__":
    StreamlitFrontendRenderer().show_results(0)

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#
# app = Dash(__name__, external_stylesheets=external_stylesheets)
#
# styles = {
#     'pre': {
#         'border': 'thin lightgrey solid',
#         'overflowX': 'scroll',
#         'color': 'black'
#     },
#     'div': {
#         'padding': '.3rem',
#         'width': '80%',
#         'margin': 'auto',
#         'boxShadow': 'dimgrey 4px 4px 2px',
#         'border-radius': '10px',
#         'backgroundColor': 'white',
#         'marginTop': '1rem',
#     },
#     'dropdown': {
#         'margin': 'auto',
#         'width': '50%',
#         'border-radius': '10px',
#         'color': 'black'
#     }
# }
#
# app.layout = html.Div([
#     html.Div(children=[
#         html.H1(f'Change Point Scatter Plot',
#                 style={'fontSize': 40},
#                 id='header'),
#     ],
#         style=styles['div']
#     ),
#     html.Div([
#         dcc.Markdown("""
#                     **Selection Data**
#
#                     Choose the lasso or rectangle tool in the graph's menu
#                     bar and then select points in the graph.
#
#                 """),
#         html.Pre(id='selected-data', style=styles['pre'])],
#         style=styles['div'],
#         hidden=False,
#         id='selected-data-container'
#     )
# ])
