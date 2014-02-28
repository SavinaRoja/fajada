#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This example shows how the tools for a plot may be changed dynamically by other
interface elements, in particular it showcases how to do this with the
CheckListEditor. Each of CheckListEditor's styles are displayed. Note that the
tool classes themselves are not imported here.

Relevant tutorial section:
http://docs.enthought.com/chaco/user_manual/chaco_tutorial.html#dynamically-controlling-interactions
"""

from traits.api import HasTraits, Instance, List
from traitsui.api import View, Item, CheckListEditor
from chaco.api import Plot, ArrayPlotData
from enable.component_editor import ComponentEditor
from numpy import linspace, sin


class ToolsExample2(HasTraits):

    plot = Instance(Plot)

    tools = List(editor=CheckListEditor(values=["PanTool",
                                                "ZoomTool",
                                                "DragZoom"], cols=4))

    traits_view = View(
        Item("tools", label="Default:"),
        Item("tools", label="Simple:", style="simple"),
        Item("tools", label="Data Tools List", style="custom"),
        Item("tools", label="Data Tools List", style="text"),
        Item("tools", label="Data Tools List", style="readonly"),
        Item("plot", editor=ComponentEditor(), show_label=False),
        width=500, height=500, resizable=True, title="Tools Example 2")

    def __init__(self):
        super(ToolsExample2, self).__init__()
        x = linspace(-14, 14, 100)
        y = sin(x) * x ** 3

        plotdata = ArrayPlotData(x=x, y=y)
        plot = Plot(plotdata)
        plot.plot(("x", "y"), type="line", color="blue")

        self.plot = plot

    def _tools_changed(self):
        classes = [eval(class_name) for class_name in self.tools]

        #Remove all tools from the plot
        plot_tools = self.plot.tools
        for tool in plot_tools:
            plot_tools.remove(tool)

        #Create new instances for the selected tool classes
        for cls in classes:
            self.plot.tools.append(cls(self.plot))

if __name__ == "__main__":
    ToolsExample2().configure_traits()
