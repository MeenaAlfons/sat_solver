#!/usr/bin/env python
"""Provides JeroslowWangOneSided
"""

import heapdict

from JeroslowWangPlugin import JeroslowWangPlugin
from ListStack import ListStack
from BranchDecisionHeuristicInterface import BranchDecisionHeuristicInterface

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class JeroslowWangOneSided(BranchDecisionHeuristicInterface, JeroslowWangPlugin):

    def initCounts(self, literalScore):
        self.literalScore = heapdict.heapdict()
        self.countStack = ListStack()

        for literal in literalScore:
            # - is used to make a max priority queue
            self.literalScore[literal] = -literalScore[literal]
        return

    def pushCurrentCountsAndDecrease(self, assignedVariable, literalScore):
        if assignedVariable in literalScore or -assignedVariable in literalScore:
            raise "assignedVariable Exists"

        positiveScore = 0
        if assignedVariable in self.literalScore:
            positiveScore = self.literalScore[assignedVariable]
            self.literalScore.pop(assignedVariable, None)

        negativeScore = 0
        if -assignedVariable in self.literalScore:
            negativeScore = self.literalScore[-assignedVariable]
            self.literalScore.pop(-assignedVariable, None)

        changedLiterals = {}
        for literal in literalScore:
            score = self.literalScore[literal]
            changedLiterals[literal] = score
            # + is used to decrease the count
            newValue = self.literalScore[literal] + literalScore[literal]
            if newValue > 0:
                raise "newValue can't be positive"
            if abs(newValue) < 0.000001 and newValue != 0:
                raise "very small"
            if newValue == 0:
                self.literalScore.pop(literal, None)
            else:
                self.literalScore[literal] = newValue

        self.countStack.push((assignedVariable, positiveScore, negativeScore, changedLiterals))
        return

    def popCurrentCounts(self):
        assignedVariable, positiveScore, negativeScore, changedLiterals = self.countStack.pop()

        if positiveScore != 0:
            self.literalScore[assignedVariable] = positiveScore

        if negativeScore != 0:
            self.literalScore[-assignedVariable] = negativeScore

        for literal in changedLiterals:
            score = changedLiterals[literal]
            if score != 0:
                self.literalScore[literal] = score

        return

    def chooseVariableAndValue(self, cnfState):
        literal, score = self.literalScore.peekitem()
        score = - score
        if score <= 0:
            raise "this can't be true"
        variable = abs(literal)
        value = literal > 0
        return variable, value

