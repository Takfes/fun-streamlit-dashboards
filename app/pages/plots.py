import numpy as np
import pandas as pd
import streamlit as st
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CrosshairTool, HoverTool, LinearAxis, Range1d
from bokeh.plotting import figure
from utils.helpers import configure_plot, load_data, save_plots


def main():
    # Configure page layout
    st.set_page_config(layout="wide")

    # Load data
    data = load_data()
    df = pd.DataFrame(data)

    # Get list of metrics for the sidebar
    metrics_list = df.columns.tolist()[1:]
    source = ColumnDataSource(data)

    # # Select Axis - Sidebar
    # selected_metric1 = st.sidebar.multiselect('Select Primary Metric for Plot 1', metrics_list, default='Metric1')
    # selected_metric2 = st.sidebar.multiselect('Select Secondary Metric for Plot 1', metrics_list, default='Metric2')
    # selected_metric3 = st.sidebar.multiselect('Select Primary Metric for Plot 2', metrics_list, default='Metric3')
    # selected_metric4 = st.sidebar.multiselect('Select Secondary Metric for Plot 2', metrics_list, default='Metric4')

    # Select Axis for Plots
    width_allocation = [0.5, 0.5]
    label_visibility = 'collapsed'
    vertical_alignment_nested = 'top'

    with st.container(border=False):
        col1, col2 = st.columns(width_allocation, gap='small')

        with col1:
            col1_1, col1_2, col1_3 = st.columns(3, vertical_alignment=vertical_alignment_nested)
            with col1_1:
                selected_metric1 = st.multiselect('Select Primary Metric for Plot 1', metrics_list, default=metrics_list[0], label_visibility=label_visibility)
            with col1_2:
                selected_metric2 = st.multiselect('Select Secondary Metric for Plot 1', metrics_list, default=metrics_list[1], label_visibility=label_visibility)
            with col1_3:
                if st.button('💾 save', key='save_plot_1'):
                    save_plots(selected_metric1, selected_metric2, verbose=True)

        with col2:
            col2_1, col2_2, col2_3 = st.columns(3, vertical_alignment=vertical_alignment_nested)
            with col2_1:
                selected_metric3 = st.multiselect('Select Primary Metric for Plot 2', metrics_list, default=metrics_list[2], label_visibility=label_visibility)
            with col2_2:
                selected_metric4 = st.multiselect('Select Secondary Metric for Plot 2', metrics_list, default=metrics_list[3], label_visibility=label_visibility)
            with col2_3:
                if st.button('💾 save', key='save_plot_2'):
                    save_plots(selected_metric3, selected_metric4, verbose=True)

    # Establish crosshair tool
    crosshair = CrosshairTool()

    # Prepare Plots
    width = 550
    height = 300

    # Prepare Plot 1
    if selected_metric1 and selected_metric2:
        fig1 = configure_plot(selected_metric1, selected_metric2, df, source, crosshair, width=width, height=height)
    else:
        st.warning('Please select metrics for Plot 1')

    # Prepare Plot 2
    if selected_metric3 and selected_metric4:
        fig2 = configure_plot(selected_metric3, selected_metric4, df, source, crosshair, width=width, height=height)
    else:
        st.warning('Please select metrics for Plot 2')

    # Render Plots
    if (selected_metric1 and selected_metric2 and selected_metric3 and selected_metric4):
        layout = row(fig1, fig2, sizing_mode='scale_width')
        st.bokeh_chart(layout)


main()
