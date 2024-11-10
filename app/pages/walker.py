import pandas as pd
import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer
from utils.helpers import load_data


def get_pyg_renderer() -> "StreamlitRenderer":
    data = load_data()
    df = pd.DataFrame(data)
    return StreamlitRenderer(df)


# Configure page layout
st.set_page_config(layout="wide")

# Option 1
renderer = get_pyg_renderer()
renderer.explorer()

# # Option 2
# import pygwalker as pyg
# import streamlit.components.v1 as components

# df = pd.DataFrame(load_data())
# pyg_html = pyg.walk(df, return_html=True)
# components.html(pyg_html, height=1000, scrolling=True)
