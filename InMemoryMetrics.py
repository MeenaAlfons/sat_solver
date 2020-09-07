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
        self.deduceCount = 0

    def deduce(self):
        self.deduceCount += 1

    def getDeduceCount(self):
        return self.deduceCount

    def reset(self):
        self.deduceCount = 0
