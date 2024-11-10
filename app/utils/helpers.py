import numpy as np
import pandas as pd
import streamlit as st
from bokeh.models import HoverTool, LinearAxis, Range1d
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


def save_plots(cor, aux, verbose=False):
    if 'plots' not in st.session_state:
        st.session_state.plots = {}

    primary = ",".join(sorted(cor))
    secondary = ",".join(sorted(aux))
    st.session_state.plots[f'plot-{primary}-{secondary}'] = {'primary': cor, 'secondary': aux}

    if verbose:
        st.info(f'Plot saved {primary}-{secondary}')


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
    fig.add_layout(LinearAxis(y_range_name='Secondary-Axis'), 'right')

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

    # Adjust legend options
    fig.legend.location = "bottom_center"  # Options include "top_center", "bottom_center", etc.
    fig.legend.orientation = "horizontal"  # This makes the legend items align horizontally
    fig.legend.background_fill_color = "white"
    fig.legend.background_fill_alpha = 0.6
    fig.legend.label_text_font = "arial"
    fig.legend.label_standoff = 1  # Distance between label and glyph
    fig.legend.spacing = 1  # Spacing between entries
    fig.legend.padding = 1  # Padding inside the legend
    fig.legend.margin = 1  # Margin around the legend
    fig.legend.label_text_font_size = "8pt"
    fig.legend.label_text_color = "black"
    fig.title.text_font_size = '9pt'
    # fig.legend.border_line_color = "black"

    # Add crosshair tools
    fig.add_tools(crosshair)
    return fig
