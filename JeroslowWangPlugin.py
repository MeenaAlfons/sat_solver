#!/usr/bin/env python
"""Provides JeroslowWangPlugin
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

class JeroslowWangPlugin(PluginInterface):
    def construct(self, cnfState):
        literalScore = {}
        for clause in cnfState.clauses:
            clauseScore = pow(2,-len(clause))
            for literal in clause:
                if literal in literalScore:
                    literalScore[literal] += clauseScore
                else:
                    literalScore[literal] = clauseScore

        self.initCounts(literalScore)
        pass

    def satisfiedClausesPushed(self, cnfState, assignedVariable, satisfiedClausesPriorities):
        # clauses removed from remaining clauses
        # counts need to be decreased

        # no need to decrease assignedVarialbe
        # no need to decrease variable that currently does not exist in remaining variables

        literalScore = {}
        for clauseID in satisfiedClausesPriorities:
            clauseIdx = clauseID-1
            clause = cnfState.clauses[clauseIdx]
            clauseScore = pow(2, -len(clause))
            for literal in clause:
                variable = abs(literal)
                if variable != assignedVariable and variable in cnfState.getRemainingVariablesSet():
                    if literal in literalScore:
                        literalScore[literal] += clauseScore
                    else:
                        literalScore[literal] = clauseScore

        self.pushCurrentCountsAndDecrease(assignedVariable, literalScore)
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
