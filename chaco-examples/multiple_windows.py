#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This example shows how to make multiple plots in an application. The axes are
also connected, as in connected_axial_range, and the plots can be dynamically
flipped in orientation. Note that only one window uses configure_traits(), as
this blocks, so this should always be the last one.

Relevant tutorial section:
http://docs.enthought.com/chaco/user_manual/chaco_tutorial.html#multiple-windows
"""

from traits.api import HasTraits, Instance, Enum
from traitsui.api import View, Item
from chaco.api import Plot, ArrayPlotData
from enable.component_editor import ComponentEditor
from chaco.tools.pan_tool import PanTool
from chaco.tools.zoom_tool import ZoomTool
from numpy import linspace, sin


class PlotEditor(HasTraits):

    plot = Instance(Plot)

    plot_type = Enum("scatter", "line")

    orientation = Enum("horizontal", "vertical")

    traits_view = View(Item('orientation', label="Orientation"),
                       Item('plot', editor=ComponentEditor(),
                            show_label=False),
                       width=500, height=500, resizable=True,
                       title="Multiple Windows")

    def __init__(self, *args, **kwargs):
        super(PlotEditor, self).__init__(*args, **kwargs)

        x = linspace(-14, 14, 100)
        y = sin(x) * x ** 3
        plotdata = ArrayPlotData(x=x, y=y)

        plot = Plot(plotdata)
        plot.plot(("x", "y"), type=self.plot_type, color="blue")

        plot.tools.append(PanTool(plot))
        plot.tools.append(ZoomTool(plot))

        self.plot = plot

    def _orientation_changed(self):
        if self.orientation == "vertical":
            self.plot.orientation = "v"
        else:
            self.plot.orientation = "h"


if __name__ == "__main__":
    # create two plots, one of type "scatter", one of type "line"
    scatter = PlotEditor(plot_type="scatter")
    line = PlotEditor(plot_type="line")

    # connect the axes of the two plots
    scatter.plot.range2d = line.plot.range2d

    # open two windows
    line.edit_traits()
    scatter.configure_traits()
