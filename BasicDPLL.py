#!/usr/bin/env python
"""Provides BasicDPLL basic implementation for DPLL algorithm
"""

import time

from SatSolverInterface import SatSolverInterface
from CNFState import CNFState
from ListStack import ListStack
from DynamicLargestCombinedSum import DynamicLargestCombinedSum
from DynamicLargestIndividualSum import DynamicLargestIndividualSum

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class BasicDPLL(SatSolverInterface):
    # Assume cnf is an array of arrays
    def __init__(self, cnf, numOfVars, branchDecisionHeuristic, metrics):
        self.cnf = cnf
        self.numOfVars = numOfVars
        self.metrics = metrics
        self.branchDecisionHeuristic = branchDecisionHeuristic

    # Solve tries to find a satisfying assignment for
    # the CNF statement given in the constructor
    def solve(self):
        if len(self.cnf) == 0:
            return self.SAT({})

        plugins = [
            self.branchDecisionHeuristic
        ]
        self.cnfState = CNFState(self.cnf, self.numOfVars, plugins, self.metrics)
        if self.cnfState.getStatus() == "SAT":
            return self.SAT(self.cnfState.getModel())

        ignoreChildBranches = False
        while True:
            self.metrics.incrementCounter("loop")

            # status = {CONFLICT, SAT, UNDETERMINED}
            status, _, _ = self.chooseNextAssignment(ignoreChildBranches)
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
            variable, value = self.branchDecisionHeuristic.chooseVariableAndValue(self.cnfState)
            status,variable,value = self.cnfState.pushAssignment(variable, value)
        else:
            _, _, state = self.cnfState.lastAssignment()
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
            if state == "BRANCH":
                if ignoreChildBranches:
                    # Flip current variable
                    action = "FLIP"
                    pass
                elif len(self.cnfState.getRemainingVariablesDict()) > 0:
                    # Go down = add one more variable
                    action = "DOWN"
                    pass
                else:
                    # Flip current variable
                    action = "FLIP"
                    pass
            else: # state == "FLIPPED"
                if ignoreChildBranches:
                    # Go up until the first encountered unflipped variable
                    # Flip that variable
                    action = "UP"
                    pass
                elif len(self.cnfState.getRemainingVariablesDict()) > 0:
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
                variable, value = self.branchDecisionHeuristic.chooseVariableAndValue(self.cnfState)
                status, variable, value = self.cnfState.pushAssignment(variable,value)
            elif action == "UP":
                status = self.cnfState.backtrackUntilUnflipped()
                if status == "UNSAT":
                    return "UNSAT", None, None

                status, variable, value = self.cnfState.flipLastAssignment()
            else:
                raise "Not Implemented"

        return status, variable, value
