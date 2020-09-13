#!/usr/bin/env python
"""Provides VariableOccurrencesPlugin
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

class VariableOccurrencesPlugin(PluginInterface):
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

        self.countStack = ListStack()
        return

    def assignmentPushed(self, cnfState, variable, value):
        return

    def assignmentPoped(self, cnfState, variable, value):
        return

    def satisfiedClausesPushed(self, cnfState, assignedVariable, satisfiedClausesPriorities):
        # assignedVariable is a variable which was recently assigned.
        # That means this variable is not a remaining variable any more
        # it is now on the assignment stack
        # The satisfiedClauses are only the ones with both the following conditions:
        # - contianed the assignedVariable
        # - became completely satisfied as a result of assignming this variable
        # the assignedVariable may still exists in other clauses

        # What needs to be done here is:
        # - remove the assignedVariable from the current count because it should not be considered for the next choice from the priority queue
        # - However its current count need to be saved and later resotred which this variable is poped.
        # - We also need to decrease the count of the variable existing in the satisfied clauses.
        # - However we only need to decrease those which exist in the count because of those variables may have previously assigned and removed from the count

        # There is a caveat here:
        # - Some variables will not be decrease because they don't exist in the current count
        # - Come other variables will be decreased to 0 which will result in poping them from the current count
        # There comes a time to restore those satisfied clauses in satisfiedClausesPoped
        # - if all the variables in the restored clauses are increased in the count this will increase variables which actually didn't exist in the decrease process.
        # - if we only increased the variables exisiting in the current count then we are ignoring those variables whihch got decreased to 0 and poped!

        previousTotalCount = 0
        previousPositiveCount = 0
        previousNegativeCount = 0
        if assignedVariable in self.variablesClauseCount:
            previousTotalCount = self.variablesClauseCount[assignedVariable]
        if assignedVariable in self.variablesPositiveClauseCount:
            previousPositiveCount = self.variablesPositiveClauseCount[assignedVariable]
        if assignedVariable in self.variablesNegativeClauseCount:
            previousNegativeCount = self.variablesNegativeClauseCount[assignedVariable]

        self.variablesClauseCount.pop(assignedVariable, None)
        self.variablesPositiveClauseCount.pop(assignedVariable, None)
        self.variablesNegativeClauseCount.pop(assignedVariable, None)

        totalCount = {}
        positiveCount = {}
        negativeCount = {}
        for clauseID in satisfiedClausesPriorities:
            clauseIdx = clauseID-1
            clause = cnfState.clauses[clauseIdx]
            for literal in clause:
                variable = abs(literal)
                # Only decrease variables which currently exist in the count
                if variable in self.variablesClauseCount:
                    self.decreaseLiteralCount(literal, totalCount, positiveCount, negativeCount)

        changedVariables = {}
        for variable in totalCount:
            tc = 0
            pc = 0
            nc = 0
            if variable in self.variablesClauseCount:
                tc = self.variablesClauseCount[variable]
            if variable in self.variablesPositiveClauseCount:
                pc = self.variablesPositiveClauseCount[variable]
            if variable in self.variablesNegativeClauseCount:
                nc = self.variablesNegativeClauseCount[variable]
            changedVariables[variable] = (tc,pc,nc)

        self.countStack.push((assignedVariable, previousTotalCount, previousPositiveCount, previousNegativeCount, changedVariables))

        self.applyCountChanges(totalCount, positiveCount, negativeCount)
        return

    def satisfiedClausesPoped(self, cnfState, assignedVariable, satisfiedClausesPriorities):

        variable1, previousTotalCount, previousPositiveCount, previousNegativeCount, changedVariables = self.countStack.pop()
        if variable1 != assignedVariable:
            raise "Something is wrong"

        if previousTotalCount != 0:
            self.variablesClauseCount[assignedVariable] = previousTotalCount
        if previousPositiveCount != 0:
            self.variablesPositiveClauseCount[assignedVariable] = previousPositiveCount
        if previousNegativeCount != 0:
            self.variablesNegativeClauseCount[assignedVariable] = previousNegativeCount

        for variable in changedVariables:
            tc, pc, nc = changedVariables[variable]
            if tc != 0:
                self.variablesClauseCount[variable] = tc
            if pc != 0:
                self.variablesPositiveClauseCount[variable] = pc
            if nc != 0:
                self.variablesNegativeClauseCount[variable] = nc
        return

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
                if newValue > 0 :
                    print("Wrong")
                if newValue == 0:
                    self.variablesClauseCount.pop(variable, None)
                else:
                    self.variablesClauseCount[variable] = newValue
            else:
                if totalCount[variable] >= 0:
                    print("Wrong")
                self.variablesClauseCount[variable] = totalCount[variable]

        for variable in positiveCount:
            if variable in self.variablesPositiveClauseCount:
                newValue = self.variablesPositiveClauseCount[variable] + positiveCount[variable]
                if newValue > 0 :
                    print("Wrong")
                if newValue == 0:
                    self.variablesPositiveClauseCount.pop(variable, None)
                else:
                    self.variablesPositiveClauseCount[variable] = newValue
            else:
                if totalCount[variable] >= 0:
                    print("Wrong")
                self.variablesPositiveClauseCount[variable] = positiveCount[variable]

        for variable in negativeCount:
            if variable in self.variablesNegativeClauseCount:
                newValue = self.variablesNegativeClauseCount[variable] + negativeCount[variable]
                if newValue > 0 :
                    print("Wrong")
                if newValue == 0:
                    self.variablesNegativeClauseCount.pop(variable, None)
                else:
                    self.variablesNegativeClauseCount[variable] = newValue
            else:
                if totalCount[variable] >= 0:
                    print("Wrong")
                self.variablesNegativeClauseCount[variable] = negativeCount[variable]
