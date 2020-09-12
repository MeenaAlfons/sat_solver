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

class DynamicLargestIndividualSum(BranchDecisionHeuristicInterface, VariableOccurrencesPlugin):
    def __init__(self, positive):
        self.positive = positive

    def chooseVariableAndValue(self, cnfState):
        positiveCount = 0
        negativeCount = 0
        if self.positive:
            variable, positiveCount = self.variablesPositiveClauseCount.peekitem()
            if variable in self.variablesNegativeClauseCount:
                negativeCount = -self.variablesNegativeClauseCount[variable]
        else:
            variable, negativeCount = self.variablesNegativeClauseCount.peekitem()
            if variable in self.variablesPositiveClauseCount:
                positiveCount = -self.variablesPositiveClauseCount[variable]

        value = positiveCount > negativeCount
        return variable, value
