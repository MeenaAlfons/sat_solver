#!/usr/bin/env python
"""Provides BranchDecisionHeuristicInterface
"""

from PluginInterface import PluginInterface

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class BranchDecisionHeuristicInterface(PluginInterface):
    def chooseVariableAndValue(self, cnfState):
        # example
        variable = 1
        value = False
        return variable, value
