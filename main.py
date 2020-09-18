#!/usr/bin/env python
"""Provides main function for testing SatSolvers
"""
import time
import statistics

from SatSolverInterface import SatSolverInterface
from InMemoryMetrics import InMemoryMetrics
from BasicDPLL import BasicDPLL
from dimacs_tools import load_dimacs, load_sudokus
import validation
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


def main():
    rules, numOfVars = load_dimacs('rules/sudoku_rules_9x9.txt')
    sudokus = load_sudokus('sudokus/1000_sudokus_9x9.txt')

    solverSpecs = [{
        "SolverClass": BasicDPLL,
    }]

    # cnf = [[1,2,3], [1,-2],[1,-3],[-1,3]]
    # numOfVars = 3

    for solverSpec in solverSpecs:
        SolverClass = solverSpec["SolverClass"]
        overallMetrics = InMemoryMetrics()
        for sudoku in sudokus:
            cnf = rules + sudoku
            instanceMetrics = InMemoryMetrics()

            before = time.time()
            solver = SolverClass(cnf,
                numOfVars,
                # DynamicLargestIndividualSum(True),
                # JeroslowWangOneSided(),
                # DynamicLargestCombinedSum(),
                DummyBranchDecision(),
                -1,
                0,
                instanceMetrics
            )
            result, model = solver.solve()
            totalTime = time.time()-before

            overallMetrics.observeMany(instanceMetrics.getCounters())
            overallMetrics.observe("totalTime", totalTime)
            overallMetrics.observe("result", result)

            before = time.time()
            validCnf, someDontCare = validation.validateCnfModel(cnf, model)
            validCnfTime = time.time()-before
            overallMetrics.observe("someDontCare", someDontCare)
            overallMetrics.observe("validCnf", validCnf)
            overallMetrics.observe("validCnfTime", validCnfTime)

            before = time.time()
            validSudoku = validation.validateSudoku(model, 9)
            validSudokuTime = time.time()-before
            overallMetrics.observe("validSudoku", validSudoku)
            overallMetrics.observe("validSudokuTime", validSudokuTime)
        overallMetrics.printObservations()

if __name__ == "__main__":
    main()
