#!/usr/bin/env python
"""Provides InMemoryMetrics
"""

import statistics
from collections import Counter

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
        self.observations = {}

    def getCounters(self):
        return self.counters

    def incrementCounter(self, name):
        if name in self.counters:
            self.counters[name] +=1
        else:
            self.counters[name] = 1

    def observe(self, name, value):
        if name in self.observations:
            self.observations[name].append(value)
        else:
            self.observations[name] = [value]

    def observeMany(self, observations):
        for name in observations:
            self.observe(name, observations[name])

    def printCounters(self):
        line = "counters:"
        for name in self.counters:
            line += " " + name + "=" + str(self.counters[name])
        print(line)

    def printObservations(self):
        for name in self.observations:
            candidate = self.observations[name][0]
            if isinstance(candidate, (str, bool)):
                counts = Counter(self.observations[name])
                line = "{}:".format(name)
                for key in counts:
                    line += " {}={}".format(key, counts[key])
                print(line)
            else:
                mean = statistics.mean(self.observations[name])
                maxVal = max(self.observations[name])
                minVal = min(self.observations[name])
                print("{}: min={} mean={} max={}".format(name, minVal, mean, maxVal))