#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This example shows how a (very) basic script can show a plot.

Relevant tutorial section:
http://docs.enthought.com/chaco/user_manual/chaco_tutorial.html#script-oriented-plotting
"""

import numpy as np
from chaco.shell import *

x = np.linspace(-2 * np.pi, 2 * np.pi, 100)
y = np.sin(x)

plot(x, y, "r-")
title("Hello Plot World")
ytitle("sin(x)")
xtitle("x")
show()
