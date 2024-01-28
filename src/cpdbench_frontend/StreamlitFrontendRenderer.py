import pandas as pd
import subprocess
import json

from cpdbench_frontend.FrontendRenderer import FrontendRenderer
from cpdbench.control import CPDFullResult


class StreamlitFrontendRenderer(FrontendRenderer):
    """Frontend renderer which renders the results using the Streamlit library.
    The interface is displayed in a web browser via a local web server.
    """

    def show_results(self, results: CPDFullResult) -> None:
        # subprocess.run("ls")
        subprocess.run(["python", "-m", "streamlit", "run", __file__])


if __name__ == "__main__":
    df = pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
    })
    df
