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
from bokeh.plotting import figure, show


def main1():
    # Generate sample data
    num_days = 100
    base = pd.Timestamp.today()
    date_range = pd.date_range(base - pd.Timedelta(days=num_days - 1), periods=num_days)
    data = pd.DataFrame({
        'Date': date_range,
        'Metric1': np.random.normal(1.0, 0.5, num_days).cumsum(),
        'Metric2': np.random.normal(0.5, 0.3, num_days).cumsum(),
        'Metric3': np.random.normal(0.5, 0.5, num_days).cumsum() + 20,
        'Metric4': np.random.normal(0.4, 0.2, num_days).cumsum() + 40,
    })

    # Create a ColumnDataSource
    source = ColumnDataSource(data)

    # Create figures
    fig1 = figure(width=400, height=300, x_axis_type="datetime", title="Metric 1")
    fig2 = figure(width=400, height=300, x_axis_type="datetime", title="Metric 2")
    
    # Add lines
    fig1.line('Date', 'Metric1', source=source, line_width=2, color='blue')
    fig2.line('Date', 'Metric2', source=source, line_width=2, color='green')
    
    # Add crosshair tools
    crosshair = CrosshairTool()
    fig1.add_tools(crosshair)
    fig2.add_tools(crosshair)

    # CustomJS for synchronized crosshairs
    js_code = """
    const crosshairs = [fig1, fig2];
    const indices = cb_data.index.indices;
    if (indices.length > 0) {
        const datetime = cb_data.source.data['Date'][indices[0]];
        crosshairs.forEach(function (fig) {
            fig.x_range.start = datetime - 86400000; // 1 day in milliseconds
            fig.x_range.end = datetime + 86400000; // 1 day in milliseconds
        });
    }
    """
    js_callback = CustomJS(args=dict(fig1=fig1, fig2=fig2), code=js_code)
    
    # Connect the crosshair move event to the CustomJS callback
    fig1.js_on_event(MouseMove, js_callback)
    fig2.js_on_event(MouseMove, js_callback)

    # Layout plots side by side
    layout = row(fig1, fig2)
    st.bokeh_chart(layout)

def main2():
    # Generate sample data
    num_days = 100
    base = pd.Timestamp.today()
    date_range = pd.date_range(base - pd.Timedelta(days=num_days - 1), periods=num_days)
    data = pd.DataFrame({
        'Date': date_range,
        'Metric1': np.random.normal(1.0, 0.5, num_days).cumsum() + 50,
        'Metric2': np.random.normal(0.5, 0.3, num_days).cumsum() + 30,
        'Metric3': np.random.normal(0.5, 0.5, num_days).cumsum() + 20,
        'Metric4': np.random.normal(0.4, 0.2, num_days).cumsum() + 40,
    })

    source = ColumnDataSource(data)

    def create_figure(title, x, y0, y1):
        p = figure(width=500, height=300, x_axis_type="datetime", title=title)
        p.line(x=x, y=y0, source=source, line_width=2, color='blue', legend_label=y0)
        
        p.extra_y_ranges = {"y1": Range1d(start=data[y1].min(), end=data[y1].max())}
        p.add_layout(LinearAxis(y_range_name="y1"), 'right')
        p.line(x=x, y=y1, source=source, line_width=2, color='green', y_range_name="y1", legend_label=y1)

        crosshair = CrosshairTool(dimensions='height')
        p.add_tools(crosshair)

        hover = HoverTool(
            tooltips=[
                ("Date", "@Date{%F}"),
                (y0, f"@{y0}"),
                (y1, f"@{y1}")
            ],
            formatters={'@Date': 'datetime'},
            mode='vline'
        )
        p.add_tools(hover)

        return p

    fig1 = create_figure("Metrics 1 & 2", 'Date', 'Metric1', 'Metric2')
    fig2 = create_figure("Metrics 3 & 4", 'Date', 'Metric3', 'Metric4')

    # CustomJS for synchronizing crosshairs
    js_code = """
        const data = cb_obj['cb_data']['geometry'];
        fig2.x_range.start = fig1.x_range.start = data['x'] - 1000000;
        fig2.x_range.end = fig1.x_range.end = data['x'] + 1000000;
    """

    js_callback = CustomJS(args=dict(fig1=fig1, fig2=fig2), code=js_code)
    fig1.js_on_event('mousemove', js_callback)
    fig2.js_on_event('mousemove', js_callback)

    layout = row(fig1, fig2)
    st.bokeh_chart(layout)
    
def main3():
    # Generate sample data
    num_days = 100
    base = pd.Timestamp.today()
    date_range = pd.date_range(base - pd.Timedelta(days=num_days - 1), periods=num_days)
    data = pd.DataFrame({
        'Date': date_range,
        'Metric1': np.random.normal(1.0, 0.5, num_days).cumsum(),
        'Metric2': np.random.normal(0.5, 0.3, num_days).cumsum(),
        'Metric3': np.random.normal(0.6, 0.4, num_days).cumsum(),
        'Metric4': np.random.normal(0.4, 0.2, num_days).cumsum(),
    })

    source = ColumnDataSource(data)

    # Create figures
    fig1 = figure(width=400, height=300, x_axis_type="datetime", title="Metrics 1 & 2")
    fig2 = figure(width=400, height=300, x_axis_type="datetime", title="Metrics 3 & 4")
    
    # Add lines for Metrics 1 & 2 in fig1
    fig1.line('Date', 'Metric1', source=source, line_width=2, color='blue')
    fig1.line('Date', 'Metric2', source=source, line_width=2, color='green')

    # Add lines for Metrics 3 & 4 in fig2
    fig2.line('Date', 'Metric3', source=source, line_width=2, color='red')
    fig2.line('Date', 'Metric4', source=source, line_width=2, color='purple')
    
    # Add crosshair tools
    crosshair = CrosshairTool()
    fig1.add_tools(crosshair)
    fig2.add_tools(crosshair)

    # CustomJS for synchronized crosshairs
    js_code = """
    const crosshairs = [fig1, fig2];
    const indices = cb_data.index.indices;
    if (indices.length > 0) {
        const datetime = cb_data.source.data['Date'][indices[0]];
        crosshairs.forEach(function (fig) {
            fig.x_range.start = datetime - 86400000; // 1 day in milliseconds
            fig.x_range.end = datetime + 86400000; // 1 day in milliseconds
        });
    }
    """
    js_callback = CustomJS(args=dict(fig1=fig1, fig2=fig2), code=js_code)
    
    # Connect the crosshair move event to the CustomJS callback
    fig1.js_on_event(MouseMove, js_callback)
    fig2.js_on_event(MouseMove, js_callback)

    # Layout plots side by side
    layout = row(fig1, fig2)
    st.bokeh_chart(layout)

if __name__ == "__main__":
    main3()
