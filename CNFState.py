#!/usr/bin/env python
"""Provides CNFState which implements efficient datastructure and operations on CNF
"""

import time

from ListStack import ListStack

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class CNFState():
    def __init__(self, cnf, numOfVars, metrics):
        self.cnf = cnf
        self.metrics = metrics
        self.remainingClauses = self.cnf
        self.assignmentStack = ListStack()
        self.satisfiedClausesStack = ListStack()
        self.model = {}
        self.status = "UNDETERMINED"

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

        #TODO we need to deduce
        self.deduceNewVariable()

        return self.status, variable, value

    def flipLastAssignment(self):
        currentVariable, currentValue = self.assignmentStack.pop()
        variable = currentVariable
        value = not currentValue
        self.assignmentStack.push((variable, value))
        self.model[variable] = value

        #TODO we need to deduce
        # Make sure to unwind the satisfiedClausesStack and push the newly satisfiedClauses
        # more efficient ways could exist
        self.deduceFlip()

        return self.status, variable, value

    def backtrackUntilUnflipped(self):
        poppedVariables = []
        while len(self.assignmentStack) > 0:
            var, _ = self.assignmentStack.pop()
            self.model.pop(var, None)
            poppedVariables.append(var)
            _, previousValue = self.assignmentStack.top()
            #TODO we need to store something to know whether is variable is unflipped or not
            if previousValue == False: # unflipped
                break

        if len(self.assignmentStack) == 0:
            return "UNSAT", poppedVariables

        # Unwind the satisfiedClausesStack until it contains len(assignmentStack)-1
        while len(self.satisfiedClausesStack) > len(self.assignmentStack):
            clauses = self.satisfiedClausesStack.pop()
            self.remainingClauses.extend(clauses)

        # No need to deduce this case because we did deduce it before.
        # The caller will probably choose to flip this variable next.
        # Status need to change to undertermined
        self.status = "UNDETERMINED"
        return self.status, poppedVariables

    def lastAssignment(self):
        variable, value = self.assignmentStack.top()
        return variable, value

    # The new variable is already added
    def deduceNewVariable(self):
        satisfiedClauses = []
        localRemainingClauses = []

        for clause in self.remainingClauses:
            sat = False
            numOfFalseValues = 0
            for literal in clause:
                variable = abs(literal)
                if variable in self.model:
                    varValue = self.model[variable]
                    literalValue = varValue if literal > 0 else not varValue
                    if literalValue == True:
                        sat = True
                        break
                    else:
                        numOfFalseValues = numOfFalseValues + 1

            if sat:
                satisfiedClauses.append(clause)
            elif numOfFalseValues == len(clause):
                self.status = "CONFLICT"
                return
            else:
                localRemainingClauses.append(clause)

        self.satisfiedClausesStack.push(satisfiedClauses)
        self.remainingClauses = localRemainingClauses

        if len(self.remainingClauses) == 0:
            self.status = "SAT"
            return

        self.status = "UNDETERMINED"

    # A last variable is already flipped
    def deduceFlip(self):
        if self.status != "CONFLICT":
            clauses = self.satisfiedClausesStack.pop()
            self.remainingClauses.extend(clauses)
        self.deduceNewVariable()