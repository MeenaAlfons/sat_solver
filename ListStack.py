#!/usr/bin/env python
"""Provides ListStack a stack implementation using list
"""

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class ListStack:
    def __init__(self):
        self.list = []

    def push(self, v):
        self.list.append(v)

    def pop(self):
        return self.list.pop()

    def top(self):
        return self.list[-1]

    def __len__(self):
        return len(self.list)
