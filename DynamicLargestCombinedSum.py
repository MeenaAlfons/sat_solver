#!/usr/bin/env python
"""Provides DynamicLargestCombinedSum
"""

from VariableCountPlugin import VariableCountPlugin
from BranchDecisionHeuristicInterface import BranchDecisionHeuristicInterface
import heapdict
from ListStack import ListStack

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class DynamicLargestCombinedSum(BranchDecisionHeuristicInterface, VariableCountPlugin):
    def initCounts(self, literalCount):
        self.totalCount = heapdict.heapdict()
        self.positiveCount = {}
        self.countStack = ListStack()

        totalChanges = {}
        for literal in literalCount:
            variable = abs(literal)
            if variable in totalChanges:
                totalChanges[variable] += literalCount[literal]
            else:
                totalChanges[variable] = literalCount[literal]

            if literal > 0:
                self.positiveCount[variable] = literalCount[literal]

        # - is used to make a max priority queue
        for variable in totalChanges:
            self.totalCount[variable] = - totalChanges[variable]

    def pushCurrentCountsAndDecrease(self, assignedVariable, literalCount):
        if assignedVariable in literalCount or -assignedVariable in literalCount:
            print("assignedVariable Exists")

        previousTotalCount = 0
        previousPositiveCount = 0
        if assignedVariable in self.totalCount:
            previousTotalCount = self.totalCount[assignedVariable]
            self.totalCount.pop(assignedVariable, None)

        if assignedVariable in self.positiveCount:
            previousPositiveCount = self.positiveCount[assignedVariable]
            self.positiveCount.pop(assignedVariable, None)

        totalChanges = {}
        positiveChanges = {}
        for literal in literalCount:
            variable = abs(literal)
            if variable in totalChanges:
                totalChanges[variable] += literalCount[literal]
            else:
                totalChanges[variable] = literalCount[literal]
            if literal > 0:
                positiveChanges[variable] = literalCount[literal]


        changedVariables = {}
        for variable in totalChanges:
            tc = 0
            pc = 0
            if variable in self.totalCount:
                tc = self.totalCount[variable]
            if variable in self.positiveCount:
                pc = self.positiveCount[variable]
            if pc < 0:
                raise "pc can't be negative"
            changedVariables[variable] = (tc, pc)
            # Apply changes
            # + is used to make a max priority queue
            newValue = self.totalCount[variable] + totalChanges[variable]
            if newValue > 0:
                raise "tc can't be positive"
            if newValue == 0:
                self.totalCount.pop(variable, None)
            else:
                self.totalCount[variable] = newValue

        # Apply changes
        for variable in positiveChanges:
            # - is used to decrease the count
            newValue = self.positiveCount[variable] - positiveChanges[variable]
            if newValue < 0:
                raise "pc can't be negative"
            if newValue == 0:
                self.positiveCount.pop(variable, None)
            else:
                self.positiveCount[variable] = newValue

        self.countStack.push((assignedVariable, previousTotalCount, previousPositiveCount, changedVariables))
        return

    def popCurrentCounts(self):
        assignedVariable, previousTotalCount, previousPositiveCount, changedVariables = self.countStack.pop()

        if previousTotalCount != 0:
            self.totalCount[assignedVariable] = previousTotalCount

        if previousPositiveCount != 0:
            self.positiveCount[assignedVariable] = previousPositiveCount

        for variable in changedVariables:
            tc, pc = changedVariables[variable]
            if tc != 0:
                self.totalCount[variable] = tc
            if pc != 0:
                self.positiveCount[variable] = pc

        return

    def chooseVariableAndValue(self, cnfState):
        variable, tc = self.totalCount.peekitem()
        tc = - tc
        pc = self.positiveCount[variable]
        nc = tc - pc
        if tc <=0 or pc <0 or nc < 0:
            raise "this can't be true"
        value = pc > nc
        return variable, value
