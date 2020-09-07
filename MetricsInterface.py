#!/usr/bin/env python
"""Provides MetricsInterface a interface for collecting metrics of SatSolver
"""

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class MetricsInterface:
    def deduce(self):
        print("MetricsInterface.deduce() Not implemented")

    def getDeduceCount(self):
        print("MetricsInterface.getDeduceCount() Not implemented")
        return 0

    def reset(self):
        print("MetricsInterface.reset() Not implemented")
