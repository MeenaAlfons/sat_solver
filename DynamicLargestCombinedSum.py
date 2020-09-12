#!/usr/bin/env python
"""Provides DynamicLargestCombinedSum
"""

from VariableOccurrencesPlugin import VariableOccurrencesPlugin
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

class DynamicLargestCombinedSum(BranchDecisionHeuristicInterface, VariableOccurrencesPlugin):

    def chooseVariableAndValue(self, cnfState):
        variable, _ = self.variablesClauseCount.peekitem()
        positiveCount = 0
        if variable in self.variablesPositiveClauseCount:
            positiveCount = -self.variablesPositiveClauseCount[variable]

        negativeCount = 0
        if variable in self.variablesNegativeClauseCount:
            negativeCount = -self.variablesNegativeClauseCount[variable]

        value = positiveCount > negativeCount
        return variable, value
