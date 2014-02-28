#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This example shows how to make a scatter plot from an application-oriented
perspective. The results are comparable to the basic_script example, but the
framework is readily extensible for further use.

Relevant tutorial section:
http://docs.enthought.com/chaco/user_manual/chaco_tutorial.html#scatter-plots
"""

from traits.api import HasTraits, Instance
from traitsui.api import View, Item
from chaco.api import Plot, ArrayPlotData
from enable.component_editor import ComponentEditor
from numpy import linspace, sin


class ScatterPlot(HasTraits):

    plot = Instance(Plot)

    traits_view = View(
        Item("plot", editor=ComponentEditor(), show_label=False),
        width=500, height=500, resizable=True, title="Application Scatter Plot")

    def __init__(self):
        super(ScatterPlot, self).__init__()

        x = linspace(-14, 14, 100)
        y = sin(x) * x ** 3
        plotdata = ArrayPlotData(x=x, y=y)

        plot = Plot(plotdata)
        plot.plot(("x", "y"), type="scatter", color="blue")
        plot.title = "sin(x) * x^3"

        self.plot = plot

if __name__ == "__main__":
    ScatterPlot().configure_traits()
