import numpy as np
import pandas as pd
import streamlit as st
from bokeh.events import MouseMove
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, CrosshairTool, CustomJS, LinearAxis, Range1d
from bokeh.plotting import figure


def main():
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
    
    # Metrics 1 & 2 on primary and secondary y-axes in fig1
    fig1.line('Date', 'Metric1', source=source, line_width=2, color='blue', legend_label='Metric 1')
    fig1.extra_y_ranges = {'Metric2': Range1d(start=min(data['Metric2']), end=max(data['Metric2']))}
    fig1.add_layout(LinearAxis(y_range_name='Metric2', axis_label='Metric 2'), 'right')
    fig1.line('Date', 'Metric2', source=source, line_width=2, color='green', y_range_name='Metric2', legend_label='Metric 2')

    # Metrics 3 & 4 on primary and secondary y-axes in fig2
    fig2.line('Date', 'Metric3', source=source, line_width=2, color='red', legend_label='Metric 3')
    fig2.extra_y_ranges = {'Metric4': Range1d(start=min(data['Metric4']), end=max(data['Metric4']))}
    fig2.add_layout(LinearAxis(y_range_name='Metric4', axis_label='Metric 4'), 'right')
    fig2.line('Date', 'Metric4', source=source, line_width=2, color='purple', y_range_name='Metric4', legend_label='Metric 4')
    
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
    main()
