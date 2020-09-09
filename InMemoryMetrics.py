#!/usr/bin/env python
"""Provides InMemoryMetrics
"""

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class InMemoryMetrics:
    def __init__(self):
        self.counters = {}

    def incrementCounter(self, name):
        if name in self.counters:
            self.counters[name] +=1
        else:
            self.counters[name] = 1

        if self.counters[name] % 10000 == 0:
            self.print()

    def print(self):
        line = "counters:"
        for name in self.counters:
            line += " " + name + "=" + str(self.counters[name])
        print(line)