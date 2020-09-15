#!/usr/bin/env python
"""Provides DummyBranchDecision
"""

from BranchDecisionHeuristicInterface import BranchDecisionHeuristicInterface
import heapdict

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class DummyBranchDecision(BranchDecisionHeuristicInterface):

    def chooseVariableAndValue(self, cnfState):
        variable = next(iter(cnfState.getRemainingVariablesDict()))
        value = False
        return variable, value
