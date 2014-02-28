#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This example shows how to make two plots which share axial control. The axes are
connected so that when one is changed, the other will change along with it.
The axial connection may be: x-only, y-only, x and y. Try seeing what happens
when applying a vertical orientationto one of the lines.

Relevant tutorial section:
http://docs.enthought.com/chaco/user_manual/chaco_tutorial.html#connected-plots
"""

from traits.api import HasTraits, Instance
from traitsui.api import View, Item
from chaco.api import Plot, ArrayPlotData, HPlotContainer
from enable.component_editor import ComponentEditor
from chaco.tools.pan_tool import PanTool
from chaco.tools.zoom_tool import ZoomTool
from numpy import linspace, sin


class ConnectedRange(HasTraits):

    container = Instance(HPlotContainer)
    traits_view = View(Item('container', editor=ComponentEditor(),
                            show_label=False),
                       width=1000, height=600, resizable=True,
                       title="Connected Range")

    def __init__(self):
        super(ConnectedRange, self).__init__()
        x = linspace(-14, 14, 100)
        y = sin(x) * x ** 3
        plotdata = ArrayPlotData(x=x, y=y)

        scatter = Plot(plotdata)
        scatter.plot(("x", "y"), type="scatter", color="blue")

        line = Plot(plotdata)
        #line = Plot(plotdata, orientation="v", default_origin="top left")
        line.plot(("x", "y"), type="line", color="red")

        self.container = HPlotContainer(scatter, line)

        scatter.tools.append(PanTool(scatter))
        scatter.tools.append(ZoomTool(scatter))

        line.tools.append(PanTool(line))
        line.tools.append(ZoomTool(line))

        #Axis link options, try them out
        #scatter.value_range = line.value_range  # Link y-axis only
        #scatter.index_range = line.index_range  # Link x-axis only
        scatter.range2d = line.range2d  # Link both axes


if __name__ == "__main__":
    ConnectedRange().configure_traits()
