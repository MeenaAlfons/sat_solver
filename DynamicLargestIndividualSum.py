#!/usr/bin/env python
"""Provides DynamicLargestIndividualSum
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

class DynamicLargestIndividualSum(BranchDecisionHeuristicInterface, VariableCountPlugin):
    def __init__(self, polarity):
        self.polarity = polarity

    def initCounts(self, literalCount):
        self.totalCount = {}
        self.signCount = heapdict.heapdict()
        self.countStack = ListStack()

        totalChanges = {}
        for literal in literalCount:
            variable = abs(literal)
            if variable in totalChanges:
                totalChanges[variable] += literalCount[literal]
            else:
                totalChanges[variable] = literalCount[literal]

            if self.polarity == (literal > 0): # XNOR
                # - is used to make a max priority queue
                self.signCount[variable] = - literalCount[literal]

        for variable in totalChanges:
            self.totalCount[variable] = totalChanges[variable]

    def pushCurrentCountsAndDecrease(self, assignedVariable, literalCount):
        if assignedVariable in literalCount or -assignedVariable in literalCount:
            print("assignedVariable Exists")

        previousTotalCount = 0
        previousSignCount = 0
        if assignedVariable in self.totalCount:
            previousTotalCount = self.totalCount[assignedVariable]
            self.totalCount.pop(assignedVariable, None)

        if assignedVariable in self.signCount:
            previousSignCount = self.signCount[assignedVariable]
            self.signCount.pop(assignedVariable, None)

        totalChanges = {}
        positiveChanges = {}
        for literal in literalCount:
            variable = abs(literal)
            if variable in totalChanges:
                totalChanges[variable] += literalCount[literal]
            else:
                totalChanges[variable] = literalCount[literal]
            if self.polarity == (literal > 0): # XNOR
                positiveChanges[variable] = literalCount[literal]


        changedVariables = {}
        for variable in totalChanges:
            tc = 0
            sc = 0
            if variable in self.totalCount:
                tc = self.totalCount[variable]
            if variable in self.signCount:
                sc = self.signCount[variable]
            if sc > 0:
                raise "sc can't be positive"
            if tc < 0:
                raise "sc can't be negative"
            changedVariables[variable] = (tc, sc)
            # Apply changes
            # - is used to decrease the count
            newValue = self.totalCount[variable] - totalChanges[variable]
            if newValue < 0:
                raise "newValue can't be negative"
            if newValue == 0:
                self.totalCount.pop(variable, None)
            else:
                self.totalCount[variable] = newValue

        # Apply changes
        for variable in positiveChanges:
            # + is used to make a max priority queue
            newValue = self.signCount[variable] + positiveChanges[variable]
            if newValue > 0:
                raise "newValue can't be positive"
            if newValue == 0:
                self.signCount.pop(variable, None)
            else:
                self.signCount[variable] = newValue

        self.countStack.push((assignedVariable, previousTotalCount, previousSignCount, changedVariables))
        return

    def popCurrentCounts(self):
        assignedVariable, previousTotalCount, previousSignCount, changedVariables = self.countStack.pop()

        if previousTotalCount != 0:
            self.totalCount[assignedVariable] = previousTotalCount

        if previousSignCount != 0:
            self.signCount[assignedVariable] = previousSignCount

        for variable in changedVariables:
            tc, sc = changedVariables[variable]
            if tc != 0:
                self.totalCount[variable] = tc
            if sc != 0:
                self.signCount[variable] = sc

        return

    def chooseVariableAndValue(self, cnfState):
        variable, signCount = self.signCount.peekitem()
        signCount = - signCount
        tc = self.totalCount[variable]
        otherSignCount = tc - signCount

        if tc <=0 or signCount <0 or otherSignCount < 0:
            raise "this can't be true"
        value = self.polarity if signCount > otherSignCount else not self.polarity
        return variable, value
