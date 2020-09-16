#!/usr/bin/env python
"""Provides CNFState which implements efficient datastructure and operations on CNF
"""

import time

from ListStack import ListStack
from MaxPriorityDecorator import MaxPriorityDecorator
import heapdict

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

####################
# Design Decisions #
####################

# Deduction Step
# /Find/ remaining clauses which contain currentVariable
# (preferably from the least to the highest in terms of unsatisfied literals)
# do either:
# - if literal value is True => /Remove/ that clause from remaining clauses
# - if literal value is False => /Reduce/ the number of unsatisfied literals
# Removed clausess are put in satisfiedClausesStack

# Unit Propagation
# /Find clause with the least number/ of unsatisfied literals
# if the number of unsatisfied literal is 1
# /Remove/ this clause, assign a proper value to the varialbe,
# Then go back to Deduce step

# Backtracking
# 1- A variable become undetermined, /Find/ remaining clauses which has this variable and /increase/ the number of unsatisfied literals.
# 2- /Add/ previously satisfied clauses to the remaining clauses

# Required operations:
# - Map(variable => clauses)
# - Remove clause
# - Decrease priority
# - Find minimum
# - Remove minimum
# - Increase priority
# - Add (clause, priority)

# Proposed solution:
# - keep clauses in a static array and use their index as an id for the clause.
# - make a dictionary from variable to an array of clause ids.
# - Use heapdict to make a priority queue where the key is the clause id
#   and the priority is the number of unsatisfied literals.

# Required operations:
#                            | Proposed solution
# - Map(variable => clauses) | Yes (using the dictionary)
# - Remove clause            | Yes (using heapdict.pop(clauseID))
# - Decrease priority        | Yes (using heapdict[clauseID] = new_priority)
# - Find minimum             | Yes (using heapdict.peakitem())
# - Remove minimum           | Yes (using heapdict.popitem())
# - Increase priority        | Yes (using heapdict[clauseID] = new_priority)
# - Add (clause, priority)   | Yes (using heapdict[clauseID] = priority)

class CNFState():
    # - self.remainingClauses: an array of clauses has unassigned variables
    # - self.satisfiedClausesStack: a stack of satisfied clauses at each step
    # - self.assignmentStack: a running stack of variable assignment
    def __init__(self, cnf, numOfVars, plugins, metrics):
        self.plugins = plugins
        self.metrics = metrics
        self.assignmentStack = ListStack()
        self.externalAssignmentStack = ListStack()
        self.satisfiedClausesStack = ListStack()
        self.model = {}
        self.status = "UNDETERMINED"

        self.clauses = cnf
        self.remainingClausesHeap = heapdict.heapdict()
        self.variableSignedClausesDict = {}
        for clauseIdx in range(len(self.clauses)):
            clause = self.clauses[clauseIdx]
            clauseID = clauseIdx + 1
            # Fill heap
            self.remainingClausesHeap[clauseID] = len(clause)

            # Fill variable => clauses dictionary
            for literal in clause:
                variable = abs(literal)
                signedClauseID = clauseID if literal > 0 else -clauseID
                if variable in self.variableSignedClausesDict:
                    self.variableSignedClausesDict[variable].append(signedClauseID)
                else:
                    self.variableSignedClausesDict[variable] = [signedClauseID]

        self.remaininVariables = {}
        for clause in cnf:
            for literal in clause:
                variable = abs(literal)
                self.remaininVariables[variable] = True

        for plugin in self.plugins:
            plugin.construct(self)

        # TODO We need to make sure that every variable exists once in each clause
        # if it exists twice with same polarity reduce one of them
        # else status = UNSAT !!

        self.unitPropagation()


    def getRemainingVariablesDict(self):
        return self.remaininVariables

    def assignmentLength(self):
        return len(self.externalAssignmentStack)

    def getModel(self):
        return self.model

    def getStatus(self):
        return self.status

    def lastAssignment(self):
        variable, value, state = self.externalAssignmentStack.top()
        return variable, value, state

    def pushAssignment(self, variable, value):
        self.externalAssignmentStack.push((variable, value, "BRANCH"))
        self.pushAssignmentInternal(variable, value, "BRANCH")
        self.unitPropagation()
        return self.status, variable, value

    def pushAssignmentInternal(self, variable, value, state):
        self.assignmentStack.push((variable, value, state))
        self.model[variable] = value
        self.remaininVariables.pop(variable, None)

        for plugin in self.plugins:
            plugin.assignmentPushed(self, variable, value)

        # we need to deduce
        self.deduceNewVariable(variable, value)

        return self.status, variable, value

    def flipLastAssignment(self):
        self.metrics.incrementCounter("flip")
        variable, value = self.popLastAssignment()
        value = not value
        self.externalAssignmentStack.push((variable, value, "FLIPPED"))
        self.pushAssignmentInternal(variable, value, "FLIPPED")
        self.unitPropagation()
        return self.status, variable, value

    def backtrackUntilUnflipped(self):
        self.metrics.incrementCounter("backtrack")
        while len(self.externalAssignmentStack) > 0:
            _, _ = self.popLastAssignment()
            if len(self.externalAssignmentStack) == 0 :
                break
            _, _, state = self.externalAssignmentStack.top()
            if state == "BRANCH": # unflipped
                break

        if len(self.externalAssignmentStack) == 0:
            self.status = "UNSAT"

        return self.status

    # The new variable is already added
    def deduceNewVariable(self, variable, value):
        # Deduction Step
        # /Find/ remaining clauses which contain currentVariable
        # (preferably from the least to the highest in terms of unsatisfied literals)
        # do either:
        # - if literal value is True => /Remove/ that clause from remaining clauses
        # - if literal value is False => /Reduce/ the number of unsatisfied literals
        # Removed clausess are put in satisfiedClausesStack

        variableSignedClauseIDs = self.variableSignedClausesDict[variable]
        satisfiedClauseIDs = []
        newPriorities = {}
        for signedClauseID in variableSignedClauseIDs:
            clauseID = abs(signedClauseID)
            if clauseID in self.remainingClausesHeap:
                if (value == True and signedClauseID > 0) or (value == False and signedClauseID < 0):
                    satisfiedClauseIDs.append(clauseID)
                else:
                    newPriorities[clauseID] = self.remainingClausesHeap[clauseID] - 1
                    if newPriorities[clauseID] == 0:
                        self.status = "CONFLICT"
                        return

        satisfiedClausesPriorities = {}
        for clauseID in satisfiedClauseIDs:
            satisfiedClausesPriorities[clauseID] = self.remainingClausesHeap[clauseID]
            self.remainingClausesHeap.pop(clauseID)

        self.satisfiedClausesStack.push(satisfiedClausesPriorities)

        for plugin in self.plugins:
            plugin.satisfiedClausesPushed(self, variable, satisfiedClausesPriorities)

        for clauseID in newPriorities:
            self.remainingClausesHeap[clauseID] = newPriorities[clauseID]

        if len(self.remainingClausesHeap) == 0:
            self.status = "SAT"
            return

        self.status = "UNDETERMINED"

    def popLastAssignment(self):
        while len(self.assignmentStack) > 0:
            variable, value, state = self.assignmentStack.pop()
            self.model.pop(variable, None)
            self.remaininVariables[variable] = True

            for plugin in self.plugins:
                plugin.assignmentPoped(self, variable, value)

            if self.status != "CONFLICT":
                variableSignedClauseIDs = self.variableSignedClausesDict[variable]
                # For clauses inside remainingClausesHeap, their priority need to be increased
                for signedClauseID in variableSignedClauseIDs:
                    clauseID = abs(signedClauseID)
                    if clauseID in self.remainingClausesHeap:
                        self.remainingClausesHeap[clauseID] = self.remainingClausesHeap[clauseID] + 1

                # Then add previously satisfied clauses from satisfiedClausesStack
                # which will come with the correct previous priority
                satisfiedClausesPriorities = self.satisfiedClausesStack.pop()
                for clauseID in satisfiedClausesPriorities:
                    self.remainingClausesHeap[clauseID] = satisfiedClausesPriorities[clauseID]

                for plugin in self.plugins:
                    plugin.satisfiedClausesPoped(self, variable, satisfiedClausesPriorities)

            self.status = "UNDETERMINED"
            if state != "UNIT":
                self.externalAssignmentStack.pop()
                break

        self.status = "UNDETERMINED"
        return variable, value

    def unitPropagation(self):
        # Unit Propagation
        # /Find clause with the least number/ of unsatisfied literals
        # if the number of unsatisfied literal is 1
        # /Remove/ this clause, assign a proper value to the varialbe,
        # Then go back to Deduce step
        if self.status == "CONFLICT":
            return

        while len(self.remainingClausesHeap) > 0 and self.status != "CONFLICT":
            clauseID, priority = self.remainingClausesHeap.peekitem()
            if priority > 1:
                break
            self.metrics.incrementCounter("unit")
            clauseIdx = clauseID - 1
            # Which variable is unassigned?
            for literal in self.clauses[clauseIdx]:
                variable = abs(literal)
                if variable in self.model:
                    pass
                else:
                    # unassigned variable
                    # choose a value for it to satisfy the clause
                    value = True if literal > 0 else False
                    self.pushAssignmentInternal(variable, value, "UNIT")
                    break

        return
