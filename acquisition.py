# -*- coding: utf-8 -*-
"""
Defines special methods for data acquisition.
"""

#Standard Library modules
import threading
from keyword import iskeyword

#Non-Standard Library modules
import numpy
import serial


class SerialThread(threading.Thread):
    """
    The SerialThread class is made to listen on a single serial port. Other
    SerialThreads will have to be instantiated to work on other ports.

    The SerialThread parses serial input by lines, then divides the line into
    fields by splitting on semicolons. Each field should have a name and a value
    separated by a colon. If the SerialThread instance detects that it has an
    attribute lower(name), then it will attempt to update the data of that
    attribute with the new value.

    Use of SerialThread by example:
        Some widget tracks temperature and humidity, sending lines of text
        along serial port /dev/ttyACm0 (11520 baud) like the following:
            temp: 25.03; humi: 11.59
        The SerialThread should be instantiated thus:
            SerialThread('/dev/ttyACM0',
                         115200,
                         temp=temperature_plot,
                         humi=humidity_plot)
        When it is time to shut down the SerialThread, set its abort attribute
        to True.

    When initializing the SerialThread, it will check the keywords in kwargs
    and will issue a warning if there is a name conflict with pre-existing
    attributes or standard python keywords. Conflicting keywords will not be
    assigned as attributes.

    This object is still prototypical and feature-sparse as I learn more and
    decide what options are valuable
    """
    abort = False
    num_ticks = 0
    max_num_points = 200

    def __init__(self, port, baud=9600, *args, **kwargs):
        super(SerialThread, self).__init__()
        self.ser = serial.Serial(port, baud)
        for kwarg in kwargs:
            l_kwarg = kwarg.lower()
            if iskeyword(l_kwarg):
                print('{0} is not allowed: python keyword'.format(l_kwarg))
            elif l_kwarg in self.__dict__:
                print('{0} is not allowed: already attribute'.format(l_kwarg))
            else:
                self.__dict__[l_kwarg] = kwargs[kwarg]

    def run(self):
        #These are for serial reading safety, make sure we get past junk
        self.ser.readline()
        self.ser.readline()
        while not self.abort:
            line = self.ser.readline().rstrip()
            fields = line.split(';')
            for field in fields:
                name, value = field.split(':')
                name = name.lower()
                value = float(value)
                try:
                    plot = self.__dict__[name]
                except KeyError:
                    continue
                else:
                    self.num_ticks += 1
                    cur_data = plot.data
                    new_data = numpy.hstack((cur_data[-self.max_num_points + 1:],
                                             [value]))
                    new_index = numpy.arange(self.num_ticks - len(new_data) + 1,
                                             self.num_ticks + 0.01)
                    plot.index = new_index
                    plot.data = new_data