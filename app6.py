import numpy as np
import pandas as pd
import streamlit as st
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, CrosshairTool, HoverTool, LinearAxis, Range1d
from bokeh.plotting import figure


def setup_figure(source, title, metric_primary, metric_secondary):
    fig = figure(width=400, height=300, x_axis_type="datetime", title=title)
    fig.extra_y_ranges = {metric_secondary: Range1d(start=min(source.data[metric_secondary]), end=max(source.data[metric_secondary]))}
    fig.add_layout(LinearAxis(y_range_name=metric_secondary, axis_label=metric_secondary), 'right')
    
    # Create lines for metrics
    line1 = fig.line('Date', metric_primary, source=source, line_width=2, color='blue', legend_label=metric_primary)
    line2 = fig.line('Date', metric_secondary, source=source, line_width=2, color='green', y_range_name=metric_secondary, legend_label=metric_secondary)
    
    # Define hover tool
    hover = HoverTool(tooltips=[
        ("Date", "@Date{%F}"),
        (metric_primary, f"@{metric_primary}"),
        (metric_secondary, f"@{metric_secondary}")
    ], formatters={'@Date': 'datetime'}, mode='vline',renderers=[line1])
    fig.add_tools(hover)
    fig.add_tools(CrosshairTool())

    return fig

def main():
    num_days = 100
    base = pd.Timestamp.today()
    date_range = pd.date_range(base - pd.Timedelta(days=num_days - 1), periods=num_days)
    data = {
        'Date': date_range,
        'Metric1': np.random.normal(-1.0, 0.5, num_days).cumsum(),
        'Metric2': np.random.normal(1.0, 0.3, num_days).cumsum(),
        'Metric3': np.random.normal(-1.0, 0.4, num_days).cumsum(),
        'Metric4': np.random.normal(1.0, 0.2, num_days).cumsum(),
        'Metric5': np.random.normal(0.5, 0.3, num_days),
        'Metric6': np.random.normal(-0.5, 0.2, num_days),
        'Metric7': np.random.normal(1.5, 0.4, num_days).cumsum(),
        'Metric8': np.random.normal(-1.5, 0.3, num_days).cumsum(),
    }

    source = ColumnDataSource(data)

    # Streamlit multiselect for metric selection
    metrics_list = ['Metric1', 'Metric2', 'Metric3', 'Metric4', 'Metric5', 'Metric6', 'Metric7', 'Metric8']
    selected_metric1 = st.sidebar.multiselect('Select Primary Metric for Plot 1', metrics_list, default='Metric1')
    selected_metric2 = st.sidebar.multiselect('Select Secondary Metric for Plot 1', metrics_list, default='Metric2')
    selected_metric3 = st.sidebar.multiselect('Select Primary Metric for Plot 2', metrics_list, default='Metric3')
    selected_metric4 = st.sidebar.multiselect('Select Secondary Metric for Plot 2', metrics_list, default='Metric4')

    # Ensure there's a selection before plotting
    if selected_metric1 and selected_metric2 and selected_metric3 and selected_metric4:
        fig1 = setup_figure(source, "Metrics for Plot 1", selected_metric1[0], selected_metric2[0])
        fig2 = setup_figure(source, "Metrics for Plot 2", selected_metric3[0], selected_metric4[0])
        fig1.add_tools(CrosshairTool())
        fig2.add_tools(CrosshairTool())
        layout = row(fig1, fig2)
        st.bokeh_chart(layout)
    else:
        st.error("Please select metrics for all axes.")

if __name__ == "__main__":
    main()
