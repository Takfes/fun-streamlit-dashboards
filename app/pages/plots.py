import numpy as np
import pandas as pd
import streamlit as st
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CrosshairTool, HoverTool, LinearAxis, Range1d
from bokeh.plotting import figure


def string_to_color_code(input_string):
    import hashlib

    # Hash the input string using MD5
    hasher = hashlib.md5()
    hasher.update(input_string.encode('utf-8'))
    hash_digest = hasher.hexdigest()

    # Extract the first 6 digits of the hash to create a color code
    color_code = '#' + hash_digest[:6]
    return color_code


@st.cache_data
def load_data():
    # Generate sample data
    num_days = 100
    base = pd.Timestamp.today()
    date_range = pd.date_range(base - pd.Timedelta(days=num_days - 1), periods=num_days)
    data = {
        'Date': date_range,
        'Metric1': np.random.normal(-10.0, 0.5, num_days).cumsum(),
        'Metric2': np.random.normal(1.0, 0.3, num_days).cumsum(),
        'Metric3': np.random.normal(-1.0, 0.4, num_days).cumsum(),
        'Metric4': np.random.normal(1.0, 0.2, num_days).cumsum(),
        'Metric5': np.random.normal(0.5, 0.3, num_days).cumsum(),
        'Metric6': np.random.normal(-0.5, 0.2, num_days).cumsum(),
        'Metric7': np.random.normal(1.5, 0.4, num_days).cumsum(),
        'Metric8': np.random.normal(-1.5, 0.3, num_days).cumsum(),
    }
    return data


def configure_plot(primary_metrics, secondary_metrics, dataframe, source, crosshair, width=750, height=250):
    # Chart titles
    title1 = f"{primary_metrics} vs {secondary_metrics}"
    secondary_axis_min = dataframe[secondary_metrics].min(axis=1).min()
    secondary_axis_max = dataframe[secondary_metrics].max(axis=1).max()

    # Create Figure
    fig = figure(width=width, height=height, x_axis_type="datetime", title=title1)
    fig.extra_y_ranges = {"Secondary-Axis": Range1d(start=secondary_axis_min, end=secondary_axis_max)}
    fig.add_layout(LinearAxis(y_range_name='Secondary-Axis', axis_label='secondary'), 'right')

    # Add lines to Fiture
    # Primary Axis
    for m in reversed(primary_metrics):
        l1 = fig.line('Date', m, source=source, line_width=2, color=string_to_color_code(m), legend_label=m)
    # Secondary Axis
    for m in reversed(secondary_metrics):
        fig.line('Date', m, source=source, line_width=2, color=string_to_color_code(m), legend_label=m)

    # Prepare tooltips
    tooltip1 = [(x, f"@{x}") for x in primary_metrics + secondary_metrics]
    tooltip1.insert(0, ('Date', '@Date{%F}'))

    # Add tooltips
    hover1 = HoverTool(tooltips=tooltip1, formatters={'@Date': 'datetime'}, mode='vline', renderers=[l1])
    fig.add_tools(hover1)

    # Add crosshair tools
    fig.add_tools(crosshair)
    return fig

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
