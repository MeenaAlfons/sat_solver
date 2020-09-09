#!/usr/bin/env python
"""Provides main function for testing SatSolvers
"""

from SatSolverInterface import SatSolverInterface
from InMemoryMetrics import InMemoryMetrics
from BasicDPLL import BasicDPLL
from dimacs_tools import load_dimacs, load_sudokus
import tests
import time

from dimacs_tools import load_dimacs, load_sudokus

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
    cnf = rules + sudokus[0]

    solverSpecs = [{
        "SolverClass": BasicDPLL,
    }]

    # cnf = [[1,2,3], [1,-2],[1,-3],[-1,3]]
    # numOfVars = 3

    for solverSpec in solverSpecs:
        SolverClass = solverSpec["SolverClass"]
        metrics = InMemoryMetrics()
        before = time.time()
        solver = SolverClass(cnf, numOfVars, metrics)
        result, model = solver.solve()
        print("time={}".format(time.time()-before))
        print("result={}, model={}".format(result, model))
        valid, someDontCare = tests.validateCnfModel(cnf, model)
        print("valid={}, someDontCare={}".format(valid, someDontCare))
        metrics.print()


if __name__ == "__main__":
    main()
