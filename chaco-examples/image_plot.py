#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This example shows how to make an image plot. This actually only works on one of
my computers, and I haven't figured out the relevant differences. In any case,
this is the example code that will display a 3D plot with color as the Z.

Relevant tutorial section:
http://docs.enthought.com/chaco/user_manual/chaco_tutorial.html#image-plots
"""

from traits.api import HasTraits, Instance
from traitsui.api import View, Item
from chaco.api import Plot, ArrayPlotData, jet
from enable.component_editor import ComponentEditor
from numpy import exp, linspace, meshgrid


class ImagePlot(HasTraits):
    plot = Instance(Plot)

    traits_view = View(
        Item('plot', editor=ComponentEditor(), show_label=False),
        width=500, height=500, resizable=True, title="Application Image Plot")

    def __init__(self):
        super(ImagePlot, self).__init__()

        x = linspace(0, 10, 50)
        y = linspace(0, 5, 50)
        xgrid, ygrid = meshgrid(x, y)
        z = exp(-1 * (xgrid * xgrid + ygrid * ygrid) / 100.0)
        plotdata = ArrayPlotData(imagedata=z)

        plot = Plot(plotdata)
        plot.img_plot("imagedata", colormap=jet)

        self.plot = plot

if __name__ == "__main__":
    ImagePlot().configure_traits()
