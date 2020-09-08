#!/usr/bin/env python
"""Provides BasicDPLL basic implementation for DPLL algorithm
"""

from SatSolverInterface import SatSolverInterface
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
        self.remainingClauses = self.cnf
        self.remainingVars = [i+1 for i in range(self.numOfVars)]
        self.assignmentStack = ListStack()
        self.satisfiedClausesStack = ListStack()
        self.model = {}

        if len(self.remainingClauses) == 0:
            return self.SAT({})

        # unit propagation
        # take first unit clause
        while True:
            remaining_uc = False
            for clause in self.remainingClauses:
                if len(clause) == 1:
                    # remove uc from remaining clauses
                    self.remainingClauses.remove(clause)
                    # remove var from remaining vars
                    self.remainingVars.remove(clause[0])
                    # add correct polarity to assignment stack
                    if clause[0] < 0:
                        value = False
                    else:
                        value = True
                    self.assignmentStack.push((abs(clause[0]), value))

                    # propagate to all other clauses.
                    # Delete all clauses that contain this literal. They are already satisfied.
                    self.remainingClauses = [c for c in self.remainingClauses if (not clause[0] in c)]

                    # remove the negative literal from the clause if it is contained.
                    self.remainingClauses = [[l for l in c if l != clause[0]*-1] for c in self.remainingClauses]


            # check if there is any UC left
            for c in self.remainingClauses:
                if len(c) == 1:
                    remaining_uc = True
                    break

            # TODO: after this there might still be unassigned vars. those can be set to whatever
            if remaining_uc == False:
                break


        ignoreChildBranches = False
        while True:
            result, variable, value = self.chooseNextAssignment(ignoreChildBranches)
            if result == "UNSAT":
                return self.UNSAT()

            # status = {CONFLICT, SAT, UNDETERMINED}
            status = self.deduce(variable, value)
            ignoreChildBranches = False
            if status == "CONFLICT":
                # we need to inform chooseNextAssignment to ignore the subtree
                # of the current branch and choose a branch beyond that
                # (This operation is called bcktrack)
                # in other words: choose next sibling or ancestor branch => ignore child branches
                ignoreChildBranches = True
                pass
            elif status == "SAT":
                return self.SAT(self.model)
            else:
                # choose another variable
                pass

    def chooseNextAssignment(self, ignoreChildBranches):
        if len(self.assignmentStack) == 0:
            variable = self.remainingVars.pop()
            value = False
            self.assignmentStack.push((variable, value))
            self.model[variable] = value
        else:
            currentVariable, currentValue = self.assignmentStack.top()
            # self.assignmentStack.pop()
            # self.model.pop(variable, None)

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
                self.assignmentStack.pop()
                variable = currentVariable
                value = not currentValue
                self.assignmentStack.push((variable, value))
                self.model[variable] = value
            elif action == "DOWN":
                variable = self.remainingVars.pop()
                value = False
                self.assignmentStack.push((variable, value))
                self.model[variable] = value
            elif action == "UP":
                while len(self.assignmentStack) > 0:
                    var, _ = self.assignmentStack.pop()
                    self.model.pop(var, None)
                    self.remainingVars.append(var)
                    previousVariable, previousValue = self.assignmentStack.top()
                    if previousValue == False: # unflipped
                        break

                if len(self.assignmentStack) == 0:
                    return "UNSAT", None, None

                # Flip the variable on the top of the stack
                previousVariable, previousValue = self.assignmentStack.pop()
                variable = previousVariable
                value = not previousValue
                self.assignmentStack.push((variable, value))
                self.model[variable] = value

                # Unwind the satisfiedClausesStack until it contains len(assignmentStack)-1
                while len(self.satisfiedClausesStack) >= len(self.assignmentStack):
                    clauses = self.satisfiedClausesStack.pop()
                    self.remainingClauses.extend(clauses)
            else:
                raise "Not Implemented"

        return "UNDETERMINED", variable, value

    def deduce(self, variable, value):
        self.metrics.deduce()
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
                return "CONFLICT"
            else:
                localRemainingClauses.append(clause)

        self.satisfiedClausesStack.push(satisfiedClauses)
        self.remainingClauses = localRemainingClauses

        if len(self.remainingClauses) == 0:
            return "SAT"

        return "UNDETERMINED"
