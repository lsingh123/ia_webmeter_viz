#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 11:35:29 2019

@author: lavanyasingh
"""

from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.charts import Bar
from bokeh.models.sources import ColumnDataSource
from bokeh.embed import components

def create_bar_chart(data, title, x_name, y_name, x_label, y_label, hover_tool=None,
                     width=1200, height=500):
    """Creates a bar chart plot with the exact styling for the centcom
       dashboard. Pass in data as a dictionary, desired plot title,
       name of x axis, y axis and the hover tool HTML.
    """
    source = ColumnDataSource(data)
    xdr = FactorRange(factors=data[x_name])
    ydr = Range1d(start=0,end=max(data[y_name])*1.5)

    tools = []
    if hover_tool:
        tools = [hover_tool,]

    plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=width,
                  plot_height=height, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  sizing_mode='scale_width', outline_line_color="#666666")

    glyph = VBar(x=x_name, top=y_name, bottom=0, width=.8,
                 fill_color="#141d99")
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.title.text_font_size = '15pt'
    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#999999"
    plot.yaxis.axis_label = y_label
    plot.yaxis.axis_label_text_font_size = '15pt'
    plot.yaxis.major_label_text_font_size = '12pt'
    plot.ygrid.grid_line_alpha = 0.1
    plot.xaxis.axis_label = x_label
    plot.xaxis.major_label_orientation = 1
    plot.xaxis.axis_label_text_font_size = '15pt'
    plot.xaxis.major_label_text_font_size = '12pt'

    return plot

def create_hover_tool(y_key):
    """Generates the HTML for the Bokeh's hover data tool on our graph."""
    hover_html = """
      <div>
        <span class="hover-tooltip" style="font-size: 20px; font-weight: bold;">$x</span>
      </div>
      <div>
        <span class="hover-tooltip" style="font-size: 20px; font-weight: bold;">@""" + y_key + """ captures</span>
      </div>
    """
    return HoverTool(tooltips=hover_html)

def make_data(vals, x_key, y_key): 
    """ formats data into a dictionary with given keys """
    data_x = list(vals.keys())
    data_y = list(vals.values())
    data = {x_key: data_x, y_key: data_y}
    return data