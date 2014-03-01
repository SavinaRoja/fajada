# -*- coding: utf-8 -*-
"""

"""

#Standard Library modules
import threading

#Non-Standard Library modules
import numpy
import serial

#Chaco modules
from chaco.api import Plot, ArrayPlotData
from chaco.chaco_plot_editor import ChacoPlotItem

#Other Enthought modules
from traits.api import HasTraits, Instance, String, Int, Enum, Float, Array
from traitsui.api import View, Item
from enable.component_editor import ComponentEditor


class Viewer(HasTraits):
    index = Array

    data = Array

    plot_type = Enum("line", "scatter")

    serial_port = String('/dev/ttyACM0')
    serial_baud = Int(115200)
    latest_string = String('ham')

    view = View(
                Item('serial_port', label='Serial Port:'),
                Item('serial_baud', label='Serial Baud:'),
                Item('latest_string', label='Latest String:'),
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
                              width=800,
                              height=380,
                              marker_size=2,
                              show_label=False),
                width=500, height=500, resizable=True)

    def __init__(self, *args, **kwargs):
        super(Viewer, self).__init__(*args, **kwargs)

    def _serial_port_changed(self):
        print(self.serial_port)

    def _serial_baud_changed(self):
        print(self.serial_baud)

    def _latest_string_changed(self):
        print(self.latest_string)


class SerialThread(threading.Thread):
    ser = serial.Serial('/dev/ttyACM0', 115200)
    abort = False
    num_ticks = 0
    max_num_points = 200

    def __init__(self, viewer):
        super(SerialThread, self).__init__()
        self.viewer = viewer

    def run(self):
        while not self.abort:
            line = self.ser.readline().strip()
            roll = float(line.split(' ')[1][:-1])

            self.num_ticks += 1
            cur_data = self.viewer.data
            new_data = numpy.hstack((cur_data[-self.max_num_points + 1:],
                                     [roll]))
            new_index = numpy.arange(self.num_ticks - len(new_data) + 1,
                              self.num_ticks + 0.01)

            self.viewer.index = new_index
            self.viewer.data = new_data


class Fajada(HasTraits):
    viewer = Instance(Viewer, ())
    view = View(
                Item('viewer', style='custom', show_label=False),
                resizable=True, title='Fajada')

    def __init__(self):
        super(Fajada, self).__init__()
        t = SerialThread(self.viewer)
        t.start()

if __name__ == '__main__':
    Fajada().configure_traits()
