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
