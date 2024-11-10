import pandas as pd
import streamlit as st
from bokeh.layouts import column, gridplot, row
from bokeh.models import ColumnDataSource, CrosshairTool
from streamlit_elements import dashboard, elements, html, mui, nivo
from utils.helpers import configure_plot, load_data


def main():
    st.set_page_config(layout="wide")

    # Initialize the session state
    if 'plots' not in st.session_state:
        st.session_state.plots = {}

    # if session state is not empty
    if len(st.session_state.plots.keys()) == 0:
        st.write('No saved plots yet')

    else:
        # # maintain counter for plots
        # plot_counter = len(st.session_state.plots.keys())
        # st.write(f'Number of saved plots: {plot_counter}')

        # prepare for plotting
        data = load_data()
        df = pd.DataFrame(data)
        source = ColumnDataSource(data)
        crosshair = CrosshairTool()
        width = 500
        height = 200

        # create a list of plots
        plots = []
        for k, v in st.session_state.plots.items():
            plots.append(configure_plot(v['primary'], v['secondary'], df, source, crosshair, width, height))

        # Calculate the number of rows needed for 3 columns
        n_cols = 3
        # n_rows = -(-len(plots) // n_cols)  # Ceiling division

        # Create the grid layout
        grid = gridplot(plots, ncols=n_cols, plot_width=300, plot_height=height, sizing_mode='scale_width')

        # Display the grid in Streamlit
        st.bokeh_chart(grid)


main()
