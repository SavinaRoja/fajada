#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This example shows one how to add interactive tools to a plot. Because the tools
can be added and removed (more on this in tools_example_2), plot interactions
can be readily modularized and dynamically altered by other components of your
interface.

Relevant tutorial section:
http://docs.enthought.com/chaco/user_manual/chaco_tutorial.html#plot-tools-adding-interactions
"""

from traits.api import HasTraits, Instance
from traitsui.api import View, Item
from chaco.api import Plot, ArrayPlotData
from enable.component_editor import ComponentEditor
from chaco.tools.api import PanTool, ZoomTool, DragZoom
from numpy import linspace, sin


class ToolsExample1(HasTraits):

    plot = Instance(Plot)

    traits_view = View(
        Item("plot", editor=ComponentEditor(), show_label=False),
        width=500, height=500, resizable=True, title="Tools Example 1")

    def __init__(self):
        super(ToolsExample1, self).__init__()
        x = linspace(-14, 14, 100)
        y = sin(x) * x ** 3

        plotdata = ArrayPlotData(x=x, y=y)
        plot = Plot(plotdata)
        plot.plot(("x", "y"), type="line", color="blue")

        #append tools to pan, zoom, and drag
        plot.tools.append(PanTool(plot))
        plot.tools.append(ZoomTool(plot))
        plot.tools.append(DragZoom(plot, drag_button="right"))

        self.plot = plot

if __name__ == "__main__":
    ToolsExample1().configure_traits()
