import numpy as np
import pandas as pd
import streamlit as st
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CrosshairTool, HoverTool, LinearAxis, Range1d
from bokeh.plotting import figure

st.set_page_config(layout="wide")

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

def main():
    
    # Load data
    data = load_data()
    df = pd.DataFrame(data)
    
    metrics_list = df.columns.tolist()[1:]
    source = ColumnDataSource(data)
    
    # Sidebar
    selected_metric1 = st.sidebar.multiselect('Select Primary Metric for Plot 1', metrics_list, default='Metric1')
    selected_metric2 = st.sidebar.multiselect('Select Secondary Metric for Plot 1', metrics_list, default='Metric2')
    selected_metric3 = st.sidebar.multiselect('Select Primary Metric for Plot 2', metrics_list, default='Metric3')
    selected_metric4 = st.sidebar.multiselect('Select Secondary Metric for Plot 2', metrics_list, default='Metric4')

    # Establish crosshair tool
    crosshair = CrosshairTool()

    # ===================================================
    # Figure 1 
    # ===================================================

    # Chart titles
    title1 = f"{selected_metric1} vs {selected_metric2}"

    # Create Figure
    fig1 = figure(width=800, height=250, x_axis_type="datetime", title=title1)
    fig1.extra_y_ranges = {"Secondary-Axis": Range1d(start=min(data['Metric2']), end=max(data['Metric2']))}
    fig1.add_layout(LinearAxis(y_range_name='Secondary-Axis', axis_label='secondary'), 'right')

    # Add lines to Fiture 1. 
    # Primary Axis
    for m in reversed(selected_metric1):
        l1 = fig1.line('Date', m, source=source, line_width=2, color=string_to_color_code(m), legend_label=m)
    # Secondary Axis
    for m in reversed(selected_metric2):
        fig1.line('Date', m, source=source, line_width=2, color=string_to_color_code(m), legend_label=m)
    
    # Prepare tooltips
    tooltip1 = [(x, f"@{x}") for x in selected_metric1 + selected_metric2]
    tooltip1.insert(0, ('Date', '@Date{%F}'))
    
    # Add tooltips
    hover1 = HoverTool(tooltips=tooltip1, formatters={'@Date': 'datetime'}, mode='vline', renderers=[l1])
    fig1.add_tools(hover1)
    
    # Add crosshair tools
    fig1.add_tools(crosshair)

    # ===================================================
    # Figure 2
    # ===================================================

    # Chart titles
    title2 = f"{selected_metric3} vs {selected_metric4}"
    
    # Create Figure 2.
    fig2 = figure(width=800, height=250, x_axis_type="datetime", title=title2)    
    fig2.extra_y_ranges = {"Secondary-Axis": Range1d(start=min(data['Metric4']), end=max(data['Metric4']))}
    fig2.add_layout(LinearAxis(y_range_name='Secondary-Axis', axis_label='secondary'), 'right')
    
    # Add lines to Fiture 2.
    # Primary Axis
    for m in reversed(selected_metric3):
        l3 = fig2.line('Date', m, source=source, line_width=2, color=string_to_color_code(m), legend_label=m)
    # Secondary Axis
    for m in reversed(selected_metric4):
        fig2.line('Date', m, source=source, line_width=2, color=string_to_color_code(m), legend_label=m)
    
    # Prepare tooltips
    tooltip2 = [(x, f"@{x}") for x in selected_metric3 + selected_metric4]
    tooltip2.insert(0, ('Date', '@Date{%F}'))
    
    # Add tooltips
    hover2 = HoverTool(tooltips=tooltip2, formatters={'@Date': 'datetime'}, mode='vline', renderers=[l3])
    fig2.add_tools(hover2)
    
    # Add crosshair tools
    fig2.add_tools(crosshair)

    # ===================================================
    # Create Figures in Parallel
    # ===================================================

    # # Chart titles
    # title1 = f"{selected_metric1} vs {selected_metric2}"
    # title2 = f"{selected_metric3} vs {selected_metric4}"
    
    # # Create Figure 1.
    # fig1 = figure(width=800, height=250, x_axis_type="datetime", title=title1)
    # fig1.extra_y_ranges = {"Secondary-Axis": Range1d(start=min(data['Metric2']), end=max(data['Metric2']))}
    # fig1.add_layout(LinearAxis(y_range_name='Secondary-Axis', axis_label='secondary'), 'right')
    
    # # Create Figure 2.
    # fig2 = figure(width=800, height=250, x_axis_type="datetime", title=title2)    
    # fig2.extra_y_ranges = {"Secondary-Axis": Range1d(start=min(data['Metric4']), end=max(data['Metric4']))}
    # fig2.add_layout(LinearAxis(y_range_name='Secondary-Axis', axis_label='secondary'), 'right')
    
    # # Add lines : Fiture 1. | Primary Axis
    # for m in reversed(selected_metric1):
    #     l1 = fig1.line('Date', m, source=source, line_width=2, color=string_to_color_code(m), legend_label=m)
    # # Add lines : Fiture 1. | Secondary Axis
    # for m in reversed(selected_metric2):
    #     fig1.line('Date', m, source=source, line_width=2, color=string_to_color_code(m), legend_label=m)
        
    # # Add lines : Fiture 2. | Primary Axis
    # for m in reversed(selected_metric3):
    #     l3 = fig2.line('Date', m, source=source, line_width=2, color=string_to_color_code(m), legend_label=m)
    # # Add lines : Fiture 2. | Secondary Axis
    # for m in reversed(selected_metric4):
    #     fig2.line('Date', m, source=source, line_width=2, color=string_to_color_code(m), legend_label=m)
    
    # # Prepare tooltips
    # tooltip1 = [(x, f"@{x}") for x in selected_metric1 + selected_metric2]
    # tooltip1.insert(0, ('Date', '@Date{%F}'))
    
    # tooltip2 = [(x, f"@{x}") for x in selected_metric3 + selected_metric4]
    # tooltip2.insert(0, ('Date', '@Date{%F}'))
    
    # # Add tooltips
    # hover1 = HoverTool(tooltips=tooltip1, formatters={'@Date': 'datetime'}, mode='vline', renderers=[l1])
    # hover2 = HoverTool(tooltips=tooltip2, formatters={'@Date': 'datetime'}, mode='vline', renderers=[l3])
    # fig1.add_tools(hover1)
    # fig2.add_tools(hover2)
    
    # # Add crosshair tools
    # crosshair = CrosshairTool()
    # fig1.add_tools(crosshair)
    # fig2.add_tools(crosshair)

    # ===================================================
    # Display Plots
    # ===================================================

    # # Layout plots side by side
    # layout = column(fig1, fig2)
    # st.bokeh_chart(layout)
    
    # ===================================================
    # Display Plots in 2x3 Grid
    # ===================================================
    
    width_allocation = [0.9, 0.1]
    with st.container():
        col1, col2 = st.columns(width_allocation)
        with col1:
            layout = column(fig1, fig2)
            st.bokeh_chart(layout)    
        with col2:
            st.button('💾', key='save_plot_1')
    
    with st.container():
        col3, col4 = st.columns(width_allocation)
        with col3:
            pass
        with col4:
            st.button('💾', key='save_plot_2')

    
if __name__ == "__main__":
    main()
