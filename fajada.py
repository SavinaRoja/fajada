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
import numpy
from collections import deque
#import serial

#Chaco modules
from chaco.api import Plot, ArrayPlotData, HPlotContainer

#Other Enthought modules
from traits.api import HasTraits, Instance, String, Int, Enum, Float, Array
from traitsui.api import View, Item
from enable.component_editor import ComponentEditor


class Viewer(HasTraits):
    container = None

    index = Array

    data = Array

    plot = Instance(Plot)

    plot_type = Enum("line", "scatter")

    #num_ticks = Int(0)
    num_ticks = 0

    traits_view = View(Item("plot", editor=ComponentEditor(), show_label=False),
        width=300, height=300, resizable=False,)

    def __init__(self, max_points=200, advance_time=False, *args, **kwargs):
        super(Viewer, self).__init__(*args, **kwargs)
        self.advance_time = advance_time
        self.max_points = Int(max_points)

        self.plotdata = ArrayPlotData(index=self.index)
        self.plotdata.set_data('y', self.data)
        self.plot = Plot(self.plotdata)
        self.plot.plot(('index', 'y'), type='line', color='blue')

    def update(self, value):
        current_data = deque(self.data, self.max_points.default_value)
        num_ticks = self.num_ticks

        current_data.append(value)
        new_data = numpy.array(current_data)
        new_index = numpy.arange(num_ticks - len(new_data) + 1,
                                 num_ticks + 0.01)

        self.index = new_index
        self.data = new_data

        if self.advance_time:
            self.num_ticks += 1

    def _data_changed(self):
        self.plotdata.set_data('y', self.data)
        self.plotdata.set_data('index', self.index)


class Fajada(HasTraits):

    plot = Instance(HPlotContainer, ())

    temp1 = Instance(Viewer, ({'advance_time': 0.01}))
    temp2 = Instance(Viewer, ())

    traits_view = View(Item('plot', editor=ComponentEditor(), show_label=False),
                       width=1000, height=600, resizable=True,
                       title="Horizontal Plot Container")

    #temp = Instance(Viewer, ({'advance_time': 0.01}))
    #view = View(
                #Item('temp', style='custom', show_label=False),
                ##Item('heading', style='custom', show_label=False),
                ##Item('pitch', style='custom', show_label=False),
                ##Item('roll', style='custom', show_label=False),
                #resizable=True, title='Fajada')
    threads = []

    def __init__(self, ):
        super(Fajada, self).__init__()
        #self.threads.append(SerialThread('/dev/ttyACM0', 115200,
                                                #plots={'Temp': self.temp}))
        self.threads.append(FunctionThread(plot=self.temp1,
                                           f_args=(100, 10)))
        self.threads.append(FunctionThread(plot=self.temp2,
                                           f_args=(100, 10)))
        self.start_threads()

        self.temp1.plot.plot(('index', 'y'), type='line', color='blue')
        self.temp2.plot.plot(('index', 'y'), type='line', color='red')

        container = HPlotContainer(self.temp1, self.temp2)
        self.plot = container

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

