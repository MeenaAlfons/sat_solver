#!/usr/bin/env python
"""Provides SatInterface an unified interface for SatSolvers
"""

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class SatSolverInterface:
    def __init__(self, cnf, numOfVars, branchDecisionHeuristic, timeout, restarts, metrics):
        # Assume cnf is an array of arrays
        print("SatInterface constructor not implemented")
        pass

    # Solve tries to find a satisfying assignment for
    # the CNF statement given in the constructor
    def solve(self):
        print("SatInterface.solve() Not implemented")
        return self.UNSAT()

    def SAT(self, model):
        return ("SAT", model)

    def UNSAT(self):
        return ("UNSAT", {})

    def TIMEOUT(self):
        return ("TIMEOUT", {})