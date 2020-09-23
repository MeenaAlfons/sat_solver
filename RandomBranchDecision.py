#!/usr/bin/env python
"""Provides RandomBranchDecision
"""

from BranchDecisionHeuristicInterface import BranchDecisionHeuristicInterface
import heapdict
import random

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class RandomBranchDecision(BranchDecisionHeuristicInterface):

    def chooseVariableAndValue(self, cnfState):
        variable = random.sample(cnfState.getRemainingVariablesSet(), 1)[0]
        value = random.choice([False, True])
        return variable, value
