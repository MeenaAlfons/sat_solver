#!/usr/bin/env python
"""Provides VariableCountPlugin
"""

from PluginInterface import PluginInterface
from ListStack import ListStack
import heapdict

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class VariableCountPlugin(PluginInterface):
    def construct(self, cnfState):
        literalCount = {}
        for clause in cnfState.clauses:
            for literal in clause:
                if literal in literalCount:
                    literalCount[literal] += 1
                else:
                    literalCount[literal] = 1

        self.initCounts(literalCount)
        pass

    def satisfiedClausesPushed(self, cnfState, assignedVariable, satisfiedClausesPriorities):
        # clauses removed from remaining clauses
        # counts need to be decreased

        # no need to decrease assignedVarialbe
        # no need to decrease variable that currently does not exist in remaining variables

        literalCount = {}
        for clauseID in satisfiedClausesPriorities:
            clauseIdx = clauseID-1
            clause = cnfState.clauses[clauseIdx]
            for literal in clause:
                variable = abs(literal)
                if variable != assignedVariable and variable in cnfState.getRemainingVariablesSet():
                    if literal in literalCount:
                        literalCount[literal] += 1
                    else:
                        literalCount[literal] = 1

        self.pushCurrentCountsAndDecrease(assignedVariable, literalCount)
        return

    def satisfiedClausesPoped(self, cnfState, assignedVariable, satisfiedClausesPriorities):
        self.popCurrentCounts()
        return


    def initCounts(self, literalCount):
        return

    def pushCurrentCountsAndDecrease(self, assignedVariable, literalCount):
        return

    def popCurrentCounts(self):
        return
