import numpy as np
import pandas as pd
import streamlit as st
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, CrosshairTool, HoverTool, LinearAxis, Range1d
from bokeh.plotting import figure


def setup_figure(source, title, metric1, metric2):
    fig = figure(width=400, height=300, x_axis_type="datetime", title=title)
    fig.extra_y_ranges = {metric2: Range1d(start=min(source.data[metric2]), end=max(source.data[metric2]))}
    fig.add_layout(LinearAxis(y_range_name=metric2, axis_label=metric2), 'right')
    
    # Create lines for metrics
    line1 = fig.line('Date', metric1, source=source, line_width=2, color='blue', legend_label=metric1)
    line2 = fig.line('Date', metric2, source=source, line_width=2, color='green', y_range_name=metric2, legend_label=metric2)
    
    # Define hover tool for the first metric, include data for the second metric in the same tooltip
    hover1 = HoverTool(renderers=[line1], tooltips=[
        ("Date", "@Date{%F}"),
        (metric1, f"@{metric1}"),
        (metric2, f"@{metric2}")
    ], formatters={'@Date': 'datetime'}, mode='vline')

    fig.add_tools(hover1)
    fig.add_tools(CrosshairTool())

    return fig

def main():
    num_days = 100
    base = pd.Timestamp.today()
    date_range = pd.date_range(base - pd.Timedelta(days=num_days - 1), periods=num_days)
    data = pd.DataFrame({
        'Date': date_range,
        'Metric1': np.random.normal(-1.0, 0.5, num_days).cumsum(),
        'Metric2': np.random.normal(1.0, 0.3, num_days).cumsum(),
        'Metric3': np.random.normal(-1.0, 0.4, num_days).cumsum(),
        'Metric4': np.random.normal(1.0, 0.2, num_days).cumsum(),
    })

    source = ColumnDataSource(data)

    fig1 = setup_figure(source, "Metrics 1 & 2", "Metric1", "Metric2")
    fig2 = setup_figure(source, "Metrics 3 & 4", "Metric3", "Metric4")

    layout = row(fig1, fig2)
    st.bokeh_chart(layout)

if __name__ == "__main__":
    main()
