#!/usr/bin/env python
"""Provides BasicDPLL basic implementation for DPLL algorithm
"""

import time

from SatSolverInterface import SatSolverInterface
from CNFState import CNFState
from ListStack import ListStack

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class BasicDPLL(SatSolverInterface):
    # The datastructure needed for DPLL will be represented
    # in member variables

    # Assume cnf is an array of arrays
    def __init__(self, cnf, numOfVars, metrics):
        self.cnf = cnf
        self.numOfVars = numOfVars
        self.metrics = metrics

    # Solve tries to find a satisfying assignment for
    # the CNF statement given in the constructor
    #
    # Preconditions:
    # - self.remainingClauses: an array of clauses has unassigned variables
    # - self.satisfiedClausesStack: a stack of satisfied clauses at each step
    # - self.assignmentStack: a running stack of variable assignment
    def solve(self):
        if len(self.cnf) == 0:
            return self.SAT({})

        # self.remainingVars = [i+1 for i in range(self.numOfVars)]
        self.cnfState = CNFState(self.cnf, self.numOfVars, self.metrics)
        variablesClauseCount = self.cnfState.getVariablesClauseCount()
        self.remainingVars = list(variablesClauseCount.keys())

        ignoreChildBranches = False
        while True:
            self.metrics.incrementCounter("loop")
            # status = {CONFLICT, SAT, UNDETERMINED}
            status, variable, value = self.chooseNextAssignment(ignoreChildBranches)
            ignoreChildBranches = False
            if status == "UNSAT":
                return self.UNSAT()
            elif status == "CONFLICT":
                # we need to inform chooseNextAssignment to ignore the subtree
                # of the current branch and choose a branch beyond that
                # (This operation is called bcktrack)
                # in other words: choose next sibling or ancestor branch => ignore child branches
                ignoreChildBranches = True
                pass
            elif status == "SAT":
                return self.SAT(self.cnfState.getModel())
            else:
                # choose another variable
                pass

    def chooseNextAssignment(self, ignoreChildBranches):
        if self.cnfState.assignmentLength() == 0:
            variable = self.remainingVars.pop()
            value = False
            # self.assignmentStack.push((variable, value))
            # self.model[variable] = value
            status,variable,value = self.cnfState.pushAssignment(variable, value)
        else:
            currentVariable, currentValue = self.cnfState.lastAssignment()
            # Here we have a three way decision:
            # 1. Go down the tree (add one more variable)
            # 2. Flip the current variable
            # 3. Go up the tree (remove the current and possibly some previous variables as well)
            #
            # The criteria depends on three things:
            # 1. The value of current variable
            # 2. The value of ignoreChildBranches
            # 3. The length of the remainingVars

            action = ""
            if currentValue == False:
                if ignoreChildBranches:
                    # Flip current variable
                    action = "FLIP"
                    pass
                elif len(self.remainingVars) > 0:
                    # Go down = add one more variable
                    action = "DOWN"
                    pass
                else:
                    # Flip current variable
                    action = "FLIP"
                    pass
            else: # currentValue == True
                if ignoreChildBranches:
                    # Go up until the first encountered unflipped variable
                    # Flip that variable
                    action = "UP"
                    pass
                elif len(self.remainingVars) > 0:
                    # Go down = add one more variable
                    action = "DOWN"
                    pass
                else:
                    # Go up until the first encountered unflipped variable
                    # Flip that variable
                    action = "UP"

            if action == "FLIP":
                status,variable,value = self.cnfState.flipLastAssignment()
            elif action == "DOWN":
                variable = self.remainingVars.pop()
                value = False
                status,variable,value = self.cnfState.pushAssignment(variable,value)
            elif action == "UP":
                status, popedVariables = self.cnfState.backtrackUntilUnflipped()
                if status == "UNSAT":
                    return "UNSAT", None, None
                self.remainingVars.extend(popedVariables)

                status, variable, value = self.cnfState.flipLastAssignment()
            else:
                raise "Not Implemented"

        return status, variable, value
