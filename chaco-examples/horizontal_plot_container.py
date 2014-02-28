#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This example shows how to arrange multiple plots side by side using a Horizontal
Plot Container. There are various other contains to work with as one composes
an interface's layout. This example contains an uncommentable option example
that will adjust the plots to touch in the middle.

Relevant tutorial section:
http://docs.enthought.com/chaco/user_manual/chaco_tutorial.html#containers
"""

from traits.api import HasTraits, Instance
from traitsui.api import View, Item
from chaco.api import HPlotContainer, ArrayPlotData, Plot
from enable.component_editor import ComponentEditor
from numpy import linspace, sin


class ContainerExample(HasTraits):

    plot = Instance(HPlotContainer)

    traits_view = View(Item('plot', editor=ComponentEditor(), show_label=False),
                       width=1000, height=600, resizable=True,
                       title="Horizonta Plot Container")

    def __init__(self):
        super(ContainerExample, self).__init__()

        x = linspace(-14, 14, 100)
        y = sin(x) * x ** 3
        plotdata = ArrayPlotData(x=x, y=y)

        scatter = Plot(plotdata)
        scatter.plot(("x", "y"), type="scatter", color="blue")

        line = Plot(plotdata)
        line.plot(("x", "y"), type="line", color="blue")

        container = HPlotContainer(scatter, line)

        #Making the plots touch in the middle
        container.spacing = 0
        scatter.padding_right = 0
        line.padding_left = 0
        line.y_axis.orientation = "right"

        self.plot = container

if __name__ == "__main__":
    ContainerExample().configure_traits()
