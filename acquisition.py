# -*- coding: utf-8 -*-
"""
Defines special methods for data acquisition.
"""

#Standard Library modules
import threading

#Non-Standard Library modules
import numpy
import serial


class Acquisition(threading.Thread):

    def __init__(self):
        super(Acquisition, self).__init__()
        self.abort = False

    def run(self):
        while not self.abort:
            self._run()

    def _run(self):
        """
        This is meant to be overridden by sub-classes. It should define the
        action of the thread.
        """
        pass

    def update_data(self, plot, value, adv_time=False):
        cur_data = plot.data
        max_points = plot.max_points
        num_ticks = plot.num_ticks

        new_data = numpy.hstack((cur_data[-max_points + 1:],
                                 [value]))
        new_index = numpy.arange(num_ticks - len(new_data) + 1,
                                 num_ticks + 0.01)

        plot.index = new_index
        plot.data = new_data
        #plot.num_ticks += 1


class SerialThread(Acquisition):
    """
    The SerialThread class is made to listen on a single serial port. Other
    SerialThreads will have to be instantiated to work on other ports.

    The SerialThread parses serial input by lines, then divides the line into
    fields by splitting on semicolons. Each field should have a name and a value
    separated by a colon. If the SerialThread finds the name as a valid key in
    its plots dictionary, then the value will be added to the data of the plot
    associated with that key in the dictionary. Keys are case sensitive.

    Use of SerialThread by example:
        Some widget tracks temperature and humidity, sending lines of text
        along serial port /dev/ttyACM0 (11520 baud) like the following:
            temp:25.03;humi:11.59
        The SerialThread should be instantiated thus:
            SerialThread('/dev/ttyACM0',
                         115200,
                         plots={'Temp': temperature_plot
                                'humi': humidity_plot})
        When it is time to shut down the SerialThread, set its abort attribute
        to True.

    This object is still prototypical and feature-sparse as I learn more and
    decide what options are valuable.
    """

    def __init__(self, port, baud=9600, plots={}):
        super(SerialThread, self).__init__()
        self.ser = serial.Serial(port, baud)
        self.plots = plots

        #These are here to make sure we get past random startup junk
        #self.ser.readline()
        #self.ser.readline()

    def _run(self):
        try:
            line = self.ser.readline().rstrip()
            fields = line.split(';')
            for field in fields:
                name, value = field.split(':')
                if name not in self.plots:
                    continue
                self.update_data(self.plots[name], float(value))
        except Exception as e:
            print(e)


class FunctionThread(Acquisition):
    """
    Useful for simulating data acquisition.
    """

    def __init__(self):
        super(FunctionThread, self).__init__()
