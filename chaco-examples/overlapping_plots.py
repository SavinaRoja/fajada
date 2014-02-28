#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This example shows how to draw multiple plots overlayed in a single diagram.
The x array is being used twice, once for each plot.plot() call.

Relevant tutorial section:
http://docs.enthought.com/chaco/user_manual/chaco_tutorial.html#multiple-plots
"""

from traits.api import HasTraits, Instance
from traitsui.api import View, Item
from chaco.api import Plot, ArrayPlotData
from enable.component_editor import ComponentEditor
from numpy import cos, linspace, sin


class OverlappingPlot(HasTraits):

    plot = Instance(Plot)

    traits_view = View(
        Item('plot', editor=ComponentEditor(), show_label=False),
        width=500, height=500, resizable=True, title="Overlapping Plots")

    def __init__(self):
        super(OverlappingPlot, self).__init__()

        x = linspace(-14, 14, 100)
        y = x / 2.0 * sin(x)
        y2 = cos(x)
        plotdata = ArrayPlotData(x=x, y=y, y2=y2)

        plot = Plot(plotdata)
        plot.plot(("x", "y"), type="scatter", color="blue")
        plot.plot(("x", "y2"), type="line", color="red")

        self.plot = plot

if __name__ == "__main__":
    OverlappingPlot().configure_traits()
