import numpy as np
import pandas as pd
import streamlit as st
from bokeh.events import MouseMove
from bokeh.layouts import row
from bokeh.models import (
    ColumnDataSource,
    CrosshairTool,
    CustomJS,
    HoverTool,
    LinearAxis,
    Range1d,
)
from bokeh.plotting import figure


def main():
    # Generate sample data
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

    # Create figures
    fig1 = figure(width=400, height=300, x_axis_type="datetime", title="Metrics 1 & 2")
    fig2 = figure(width=400, height=300, x_axis_type="datetime", title="Metrics 3 & 4")
    
    # Setup for the secondary y-axis
    fig1.extra_y_ranges = {"Metric2": Range1d(start=min(data['Metric2']), end=max(data['Metric2']))}
    fig1.add_layout(LinearAxis(y_range_name='Metric2', axis_label='Metric 2'), 'right')
    fig2.extra_y_ranges = {"Metric4": Range1d(start=min(data['Metric4']), end=max(data['Metric4']))}
    fig2.add_layout(LinearAxis(y_range_name='Metric4', axis_label='Metric 4'), 'right')

    # Add lines
    l1 = fig1.line('Date', 'Metric1', source=source, line_width=2, color='blue', legend_label='Metric 1')
    l2 = fig1.line('Date', 'Metric2', source=source, line_width=2, color='green', y_range_name='Metric2', legend_label='Metric 2')
    l3 = fig2.line('Date', 'Metric3', source=source, line_width=2, color='red', legend_label='Metric 3')
    l4 = fig2.line('Date', 'Metric4', source=source, line_width=2, color='purple', y_range_name='Metric4', legend_label='Metric 4')
    
    # Add tooltips
    hover1 = HoverTool(tooltips=[
        ("Date", "@Date{%F}"),
        ("Metric 1", "@Metric1"),
        ("Metric 2", "@Metric2")
    ], formatters={'@Date': 'datetime'}, mode='vline', renderers=[l1])
    hover2 = HoverTool(tooltips=[
        ("Date", "@Date{%F}"),
        ("Metric 3", "@Metric3"),
        ("Metric 4", "@Metric4")
    ], formatters={'@Date': 'datetime'}, mode='vline', renderers=[l3])
    
    fig1.add_tools(hover1)
    fig2.add_tools(hover2)
    
    # Add crosshair tools
    crosshair = CrosshairTool()
    fig1.add_tools(crosshair)
    fig2.add_tools(crosshair)

    # CustomJS for controlling crosshair visibility without looping
    # js_code = """
    # function toggleCrosshair(show) {
    #     fig1.crosshair.visible = show;
    #     fig2.crosshair.visible = show;
    # }

    # fig1.on('mousemove', function() { toggleCrosshair(true); });
    # fig2.on('mousemove', function() { toggleCrosshair(true); });

    # fig1.on('mouseout', function() { toggleCrosshair(false); });
    # fig2.on('mouseout', function() { toggleCrosshair(false); });
    # """

    # js_callback = CustomJS(code=js_code, args=dict(fig1=fig1, fig2=fig2))

    # # Attach the CustomJS callback to mouse events on the plots
    # fig1.js_on_event('mousemove', js_callback)
    # fig2.js_on_event('mousemove', js_callback)
    # fig1.js_on_event('mouseout', js_callback)
    # fig2.js_on_event('mouseout', js_callback)

    # Layout plots side by side
    layout = row(fig1, fig2)
    st.bokeh_chart(layout)

if __name__ == "__main__":
    main()
