# -*- coding: utf-8 -*-
"""

"""

#Standard Library modules
from acquisition import SerialThread

#Non-Standard Library modules
#import numpy
#import serial

#Chaco modules
from chaco.api import Plot, ArrayPlotData, HPlotContainer
from chaco.chaco_plot_editor import ChacoPlotItem

#Other Enthought modules
from traits.api import HasTraits, Instance, String, Int, Enum, Float, Array
from traitsui.api import View, Item
from enable.component_editor import ComponentEditor


class Viewer(HasTraits):
    index = Array

    data = Array

    plot_type = Enum("line", "scatter")

    #serial_port = String('/dev/ttyACM0')
    #serial_baud = Int(115200)
    #latest_string = String('ham')
    #h_container =

    traits_view = View(
                #Item('serial_port', label='Serial Port:'),
                #Item('serial_baud', label='Serial Baud:'),
                #Item('latest_string', label='Latest String:'),
                ChacoPlotItem("index", "data",
                              type_trait="plot_type",
                              resizable=True,
                              x_label="Time",
                              y_label="Signal",
                              color="blue",
                              bgcolor="white",
                              border_visible=True,
                              border_width=1,
                              padding_bg_color="lightgray",
                              width=200,
                              height=200,
                              marker_size=2,
                              show_label=True),
                width=500, height=500, resizable=True)

    def __init__(self, *args, **kwargs):
        super(Viewer, self).__init__(*args, **kwargs)

    def _serial_port_changed(self):
        print(self.serial_port)

    def _serial_baud_changed(self):
        print(self.serial_baud)

    def _latest_string_changed(self):
        print(self.latest_string)


class Fajada(HasTraits):
    temp = Instance(Viewer, ())
    roll = Instance(Viewer, ())
    thermobaro = HPlotContainer()
    view = View(Item('thermobaro', editor=ComponentEditor(), show_label=False),
                #Item('temp', style='custom', show_label=False),
                #Item('roll', style='custom', show_label=False),
                resizable=True, title='Fajada')
    serial_threads = []

    def __init__(self, ):
        super(Fajada, self).__init__()
        self.serial_threads.append(SerialThread('/dev/ttyACM0', 115200,
                                                temp=self.temp,
                                                roll=self.roll))
        self.start_threads()

    def start_threads(self):
        for thread in self.serial_threads:
            thread.start()

    def stop_threads(self):
        for thread in self.serial_threads:
            thread.abort = True

if __name__ == '__main__':
    interface = Fajada()
    interface.configure_traits()
    #After the blocking call of configure_traits stops, close threads
    interface.stop_threads()

