import pandas as pd
import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer
from utils.helpers import load_data


def get_pyg_renderer() -> "StreamlitRenderer":
    data = load_data()
    df = pd.DataFrame(data)
    return StreamlitRenderer(df)


def main():
    # Configure page layout
    st.set_page_config(layout="wide")

    # Option 1
    renderer = get_pyg_renderer()
    renderer.explorer()


main()
