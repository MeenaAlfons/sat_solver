#!/usr/bin/env python
"""Provides DynamicLargestCombinedSum
"""

from PluginInterface import PluginInterface
import heapdict

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class DynamicLargestCombinedSum(PluginInterface):
    def construct(self, cnfState):
        totalCount = {}
        positiveCount = {}
        negativeCount = {}
        for clause in cnfState.clauses:
            for literal in clause:
                self.increaseLiteralCount(literal, totalCount, positiveCount, negativeCount)

        self.variablesClauseCount = heapdict.heapdict()
        self.variablesPositiveClauseCount = heapdict.heapdict()
        self.variablesNegativeClauseCount = heapdict.heapdict()
        self.applyCountChanges(totalCount, positiveCount, negativeCount)
        return

    def assignmentPushed(self, cnfState, variable, value):
        self.variablesClauseCount.pop(variable, None)
        self.variablesPositiveClauseCount.pop(variable, None)
        self.variablesNegativeClauseCount.pop(variable, None)
        return

    def assignmentPoped(self, cnfState, variable, value):
        return

    def satisfiedClausesPushed(self, cnfState, satisfiedClausesPriorities):
        totalCount = {}
        positiveCount = {}
        negativeCount = {}
        for clauseID in satisfiedClausesPriorities:
            clauseIdx = clauseID-1
            clause = cnfState.clauses[clauseIdx]
            for literal in clause:
                self.decreaseLiteralCount(literal, totalCount, positiveCount, negativeCount)

        self.applyCountChanges(totalCount, positiveCount, negativeCount)
        return

    def satisfiedClausesPoped(self, cnfState, satisfiedClausesPriorities):
        totalCount = {}
        positiveCount = {}
        negativeCount = {}
        for clauseID in satisfiedClausesPriorities:
            clauseIdx = clauseID-1
            clause = cnfState.clauses[clauseIdx]
            for literal in clause:
                innerVariable = abs(literal)
                # Not all variables in the returned clause are remaining variable
                if innerVariable in cnfState.remaininVariables:
                    self.increaseLiteralCount(literal, totalCount, positiveCount, negativeCount)

        self.applyCountChanges(totalCount, positiveCount, negativeCount)
        return

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

    def increaseLiteralCount(self, literal, totalDict, positiveDict, negativeDict):
        variable = abs(literal)
        if variable in totalDict:
            totalDict[variable] += -1
        else:
            totalDict[variable] = -1

        if literal > 0:
            if variable in positiveDict:
                positiveDict[variable] += -1
            else:
                positiveDict[variable] = -1
        else:
            if variable in negativeDict:
                negativeDict[variable] += -1
            else:
                negativeDict[variable] = -1

    def decreaseLiteralCount(self, literal, totalDict, positiveDict, negativeDict):
        variable = abs(literal)
        if variable in totalDict:
            totalDict[variable] += 1
        else:
            totalDict[variable] = 1

        if literal > 0:
            if variable in positiveDict:
                positiveDict[variable] += 1
            else:
                positiveDict[variable] = 1
        else:
            if variable in negativeDict:
                negativeDict[variable] += 1
            else:
                negativeDict[variable] = 1

    def applyCountChanges(self, totalCount, positiveCount, negativeCount):
        for variable in totalCount:
            if variable in self.variablesClauseCount:
                newValue = self.variablesClauseCount[variable] + totalCount[variable]
                if newValue == 0:
                    self.variablesClauseCount.pop(variable, None)
                else:
                    self.variablesClauseCount[variable] = newValue
            else:
                self.variablesClauseCount[variable] = totalCount[variable]

        for variable in positiveCount:
            if variable in self.variablesPositiveClauseCount:
                newValue = self.variablesPositiveClauseCount[variable] + positiveCount[variable]
                if newValue == 0:
                    self.variablesPositiveClauseCount.pop(variable, None)
                else:
                    self.variablesPositiveClauseCount[variable] = newValue
            else:
                self.variablesPositiveClauseCount[variable] = positiveCount[variable]

        for variable in negativeCount:
            if variable in self.variablesNegativeClauseCount:
                newValue = self.variablesNegativeClauseCount[variable] + negativeCount[variable]
                if newValue == 0:
                    self.variablesNegativeClauseCount.pop(variable, None)
                else:
                    self.variablesNegativeClauseCount[variable] = newValue
            else:
                self.variablesNegativeClauseCount[variable] = negativeCount[variable]
