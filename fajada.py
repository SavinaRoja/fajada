# -*- coding: utf-8 -*-
"""
I'm not entirely sure what Fajada will be yet. Is it an extended framework which
I am building to help interface with microcontrollers? Is it just a one-off
interface tool for a specific Arduino project? Is it just me tooling around with
Chaco until I learn enough to start *something real*?

What it *is*, for the moment, is an experimental interface to an Arduino-based
electronics project involving several sensors and control systems. We'll see
where things go.

SavinaRoja
"""

#Standard Library modules
from acquisition import SerialThread, FunctionThread

#Non-Standard Library modules
#import numpy
#import serial

#Chaco modules
from chaco.api import Plot, ArrayPlotData, HPlotContainer

#Other Enthought modules
from traits.api import HasTraits, Instance, String, Int, Enum, Float, Array
from traitsui.api import View, Item
from enable.component_editor import ComponentEditor


class Viewer(HasTraits):
    index = Array

    data = Array

    plot = Instance(Plot)

    plot_type = Enum("line", "scatter")

    #num_ticks = Int(0)
    num_ticks = 0

    traits_view = View(Item("plot", editor=ComponentEditor(), show_label=False),
        width=600, height=300, resizable=True,)
        #ChacoPlotItem("index", "data",
                                     #type_trait="plot_type",
                                     #resizable=True,
                                     #x_label="Time",
                                     #y_label="Signal",
                                     #color="blue",
                                     #bgcolor="white",
                                     #border_visible=True,
                                     #border_width=1,
                                     #padding_bg_color="lightgray",
                                     #width=400,
                                     #height=200,
                                     #marker_size=2,
                                     #show_label=True),
                       #width=500, height=500, resizable=True)

    def __init__(self, max_points=200, *args, **kwargs):
        super(Viewer, self).__init__(*args, **kwargs)
        #self.max_points = Int(max_points)
        self.max_points = max_points

        self.plotdata = ArrayPlotData(index=self.index)
        self.plotdata.set_data('y', self.data)
        self.plot = Plot(self.plotdata)
        self.plot.plot(('index', 'y'), type='line', color='blue')

    def _data_changed(self):
        self.plotdata.set_data('y', self.data)
        self.plotdata.set_data('index', self.index)


class Fajada(HasTraits):
    temp = Instance(Viewer, ())
    #roll = Instance(Viewer, ())
    #heading = Instance(Viewer, ())
    #pitch = Instance(Viewer, ())
    view = View(
                Item('temp', style='custom', show_label=False),
                #Item('heading', style='custom', show_label=False),
                #Item('pitch', style='custom', show_label=False),
                #Item('roll', style='custom', show_label=False),
                resizable=True, title='Fajada')
    threads = []

    def __init__(self, ):
        super(Fajada, self).__init__()
        self.serial_threads.append(SerialThread('/dev/ttyACM0', 115200,
                                                plots={'Temp': self.temp}))
        #self.threads.append(FunctionThread(plot=self.temp,
                                           #f_args=(100, 10)))
        self.start_threads()

    def start_threads(self):
        for thread in self.threads:
            thread.start()

    def stop_threads(self):
        for thread in self.threads:
            thread.abort = True

if __name__ == '__main__':
    interface = Fajada()
    interface.configure_traits()
    #After the blocking call of configure_traits stops, close threads
    interface.stop_threads()

