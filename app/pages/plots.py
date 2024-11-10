import numpy as np
import pandas as pd
import streamlit as st
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CrosshairTool, HoverTool, LinearAxis, Range1d
from bokeh.plotting import figure
from utils.helpers import configure_plot, load_data


def main():
    # Configure page layout
    st.set_page_config(layout="wide")

    # Load data
    data = load_data()
    df = pd.DataFrame(data)

    # Get list of metrics for the sidebar
    metrics_list = df.columns.tolist()[1:]
    source = ColumnDataSource(data)

    # Sidebar
    selected_metric1 = st.sidebar.multiselect('Select Primary Metric for Plot 1', metrics_list, default='Metric1')
    selected_metric2 = st.sidebar.multiselect('Select Secondary Metric for Plot 1', metrics_list, default='Metric2')
    selected_metric3 = st.sidebar.multiselect('Select Primary Metric for Plot 2', metrics_list, default='Metric3')
    selected_metric4 = st.sidebar.multiselect('Select Secondary Metric for Plot 2', metrics_list, default='Metric4')

    # Establish crosshair tool
    crosshair = CrosshairTool()

    # Display Plots in 2x3 Grid
    fig1 = configure_plot(selected_metric1, selected_metric2, df, source, crosshair)
    fig2 = configure_plot(selected_metric3, selected_metric4, df, source, crosshair)

    width_allocation = [0.9, 0.1]
    with st.container():
        col1, col2 = st.columns(width_allocation)
        with col1:
            layout = column(fig1, fig2)
            st.bokeh_chart(layout)    
        with col2:
            st.button('💾 Save', key='save_plot_1')

    with st.container():
        col3, col4 = st.columns(width_allocation)
        with col3:
            pass
        with col4:
            st.button('💾 Save', key='save_plot_2')


main()
