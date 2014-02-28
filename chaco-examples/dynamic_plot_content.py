#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This example shows how to modify the data shown in a plot using an Enumerated
list. The data_name attribute is set by the interface field, which then triggers
replacement of the plot data by dictionary key access.

Relevant tutorial section:
http://docs.enthought.com/chaco/user_manual/chaco_tutorial.html#dynamically-changing-plot-content
"""

from traits.api import HasTraits, Instance, Enum
from traitsui.api import View, Item
from chaco.api import Plot, ArrayPlotData
from enable.component_editor import ComponentEditor
from numpy import linspace
from scipy.special import jn


class DataChooser(HasTraits):

    plot = Instance(Plot)

    data_name = Enum("jn0", "jn1", "jn2")

    traits_view = View(
        Item("data_name", label="Y data"),
        Item("plot", editor=ComponentEditor(), show_label=False),
        width=800, height=600, resizable=True,
        title="Dynamic Plot Content")

    def __init__(self):
        super(DataChooser, self).__init__()
        x = linspace(-5, 10, 100)

        #jn is the Bessel function
        self.data = {"jn0": jn(0, x),
                     "jn1": jn(1, x),
                     "jn2": jn(2, x)}

        self.plotdata = ArrayPlotData(x=x, y=self.data["jn0"])

        plot = Plot(self.plotdata)
        plot.plot(("x", "y"), type="line", color="blue")
        self.plot = plot

    def _data_name_changed(self):
        self.plotdata.set_data("y", self.data[self.data_name])

if __name__ == "__main__":
    DataChooser().configure_traits()
