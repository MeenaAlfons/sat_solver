#!/usr/bin/env python
"""Provides CNFState which implements efficient datastructure and operations on CNF
"""

import time

from ListStack import ListStack
import heapdict

h = heapdict.heapdict()



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
    def __init__(self, cnf, numOfVars, metrics):
        self.metrics = metrics
        self.remainingClauses = cnf
        self.assignmentStack = ListStack()
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


        self.variablesClauseCount = {}
        for clause in cnf:
            for literal in clause:
                variable = abs(literal)
                if variable in self.variablesClauseCount:
                    self.variablesClauseCount[variable] += 1
                else:
                    self.variablesClauseCount[variable] = 1


    def getVariablesClauseCount(self):
        return self.variablesClauseCount

    def assignmentLength(self):
        return len(self.assignmentStack)

    def getModel(self):
        return self.model

    def pushAssignment(self, variable, value):
        self.assignmentStack.push((variable, value))
        self.model[variable] = value

        # we need to deduce
        self.deduceNewVariable(variable, value)

        return self.status, variable, value

    def flipLastAssignment(self):
        variable, value = self.popLastAssignment()
        value = not value
        self.pushAssignment(variable, value)

        # currentVariable, currentValue = self.assignmentStack.pop()
        # variable = currentVariable
        # value = not currentValue
        # self.assignmentStack.push((variable, value))
        # self.model[variable] = value

        # we need to deduce
        # Make sure to unwind the satisfiedClausesStack and push the newly satisfiedClauses
        # more efficient ways could exist
        # self.deduceFlip(variable, value)

        return self.status, variable, value

    def backtrackUntilUnflipped(self):
        poppedVariables = []
        while len(self.assignmentStack) > 0:
            variable, _ = self.popLastAssignment()
            poppedVariables.append(variable)
            _, previousValue = self.assignmentStack.top()
            #TODO we need to store something to know whether is variable is unflipped or not
            if previousValue == False: # unflipped
                break

        if len(self.assignmentStack) == 0:
            self.status = "UNSAT"

        # Unwind the satisfiedClausesStack until it contains len(assignmentStack)-1
        # while len(self.satisfiedClausesStack) > len(self.assignmentStack):
        #     clauses = self.satisfiedClausesStack.pop()
        #     self.remainingClauses.extend(clauses)

        # No need to deduce this case because we did deduce it before.
        # The caller will probably choose to flip this variable next.
        # Status need to change to undertermined
        # self.status = "UNDETERMINED"
        return self.status, poppedVariables

    def lastAssignment(self):
        variable, value = self.assignmentStack.top()
        return variable, value

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

        for clauseID in newPriorities:
            self.remainingClausesHeap[clauseID] = newPriorities[clauseID]

        if len(self.remainingClausesHeap) == 0:
            self.status = "SAT"
            return

        self.status = "UNDETERMINED"


    # A last variable is already flipped
    # def deduceFlip(self, variable, value):
    #     if self.status != "CONFLICT":
    #         variableSignedClauseIDs = self.variableSignedClausesDict[variable]
    #         # For clauses inside remainingClausesHeap, their priority need to be increased
    #         for signedClauseID in variableSignedClauseIDs:
    #             clauseID = abs(signedClauseID)
    #             if clauseID in self.remainingClausesHeap:
    #                 self.remainingClausesHeap[clauseID] = self.remainingClausesHeap[clauseID] + 1

    #         # Then add previously satisfied clauses from satisfiedClausesStack
    #         # which will come with the correct previous priority
    #         satisfiedClausesPriorities = self.satisfiedClausesStack.pop()
    #         for clauseID in satisfiedClausesPriorities:
    #             self.remainingClausesHeap[clauseID] = satisfiedClausesPriorities[clauseID]

    #     self.deduceNewVariable(variable, value)

    def popLastAssignment(self):
        variable, value = self.assignmentStack.pop()
        self.model.pop(variable, None)
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

        self.status = "UNDETERMINED"
        return variable, value