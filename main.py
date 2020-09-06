#!/usr/bin/env python
"""Provides main function for testing SatSolvers
"""

from SatSolverInterface import SatSolverInterface
from InMemoryMetrics import InMemoryMetrics
from BasicDPLL import BasicDPLL

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"


def load_sudoku_rules(filename):
    with open(filename) as f:
        rules = f.read()
        # split between clauses and drop las (empty) clause
        rules = rules.split('0')[:-1]

        # trim 'newline'
        rules = [c[1:-1] for c in rules]

        # split clauses and cast to int
        rules = [[int(l) for l in c.split(' ')] for c in rules][:-1]

        return rules

def main():
    cnf = load_sudoku_rules('sudoku-rules.txt')
    numOfVars = 9*9*9

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