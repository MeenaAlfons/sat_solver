#!/usr/bin/env python
"""Provides main function for testing SatSolvers
"""

from SatSolverInterface import SatSolverInterface
from InMemoryMetrics import InMemoryMetrics
from BasicDPLL import BasicDPLL
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
    rules, numOfVars = load_dimacs('rules/sudoku-rules_4x4.txt')
    sudoku = load_sudokus('sudokus/1000_sudokus_4x4.txt')
    cnf = rules + sudoku[0]

    solverSpecs = [{
        "SolverClass": SatSolverInterface,
    },{
        "SolverClass": BasicDPLL,
    }]

    for solverSpec in solverSpecs:
        SolverClass = solverSpec["SolverClass"]
        metrics = InMemoryMetrics()
        solver = SolverClass(cnf, numOfVars, metrics)
        result, model = solver.solve()
        print("result={}, model={}, deduceCount={}".format(result, model, metrics.getDeduceCount()))


if __name__ == "__main__":
    main()
