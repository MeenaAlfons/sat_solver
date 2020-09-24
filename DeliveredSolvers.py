#!/usr/bin/env python
"""Provides DeliveredSolvers
"""

import time

from InMemoryMetrics import InMemoryMetrics
from BasicDPLL import BasicDPLL
from dimacs_tools import load_dimacs, save_model_dimacs

from RandomBranchDecision import RandomBranchDecision
from RandomFalseBranchDecision import RandomFalseBranchDecision
from DummyBranchDecision import DummyBranchDecision
from DynamicLargestIndividualSum import DynamicLargestIndividualSum
from DynamicLargestCombinedSum import DynamicLargestCombinedSum
from JeroslowWangOneSided import JeroslowWangOneSided


__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class DeliveredSolvers():
    def execute(self, solverNumber, filename):
        cnf, numOfVars = load_dimacs(filename)
        result, model = self.solve(solverNumber, cnf, numOfVars)
        print("result={}".format(result))
        outputfilename = "{}.out".format(filename)
        save_model_dimacs(model, numOfVars, outputfilename)

    def solve(self, solverNumber, cnf, numOfVars):
        if solverNumber == 1:
            name = "Random"
            timeout = -1
            restarts = 0
            branchDecisionHeuristicFactory = RandomBranchDecision
            pass
        elif solverNumber == 2:
            name = "DynamicLargestIndividualSum(True)"
            timeout = -1
            restarts = 0
            branchDecisionHeuristicFactory = lambda: DynamicLargestIndividualSum(True)
            pass
        elif solverNumber == 3:
            name = "RandomFalse"
            timeout = 5
            restarts = 5
            branchDecisionHeuristicFactory = RandomFalseBranchDecision
            pass
        elif solverNumber == 4:
            name = "DynamicLargestIndividualSum(False)"
            timeout = -1
            restarts = 0
            branchDecisionHeuristicFactory = lambda: DynamicLargestIndividualSum(False)
            pass
        elif solverNumber == 5:
            name = "DynamicLargestCombinedSum"
            timeout = -1
            restarts = 0
            branchDecisionHeuristicFactory = DynamicLargestCombinedSum
            pass
        elif solverNumber == 6:
            name = "JeroslowWangOneSided"
            timeout = -1
            restarts = 0
            branchDecisionHeuristicFactory = JeroslowWangOneSided
            pass
        else:
            raise "Unknown input"

        print("Solver n={} {}".format(solverNumber, name))
        instanceMetrics = InMemoryMetrics()
        before = time.time()
        solver = BasicDPLL(cnf,
            numOfVars,
            branchDecisionHeuristicFactory,
            timeout,
            restarts,
            instanceMetrics
        )
        result, model = solver.solve()
        elapsedTime = time.time()-before
        print("elapsedTime={} seconds".format(elapsedTime))
        return result, model

