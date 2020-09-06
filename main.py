#!/usr/bin/env python
"""Provides main function for testing SatSolvers
"""

from SatSolverInterface import SatSolverInterface
from InMemoryMetrics import InMemoryMetrics
from BasicDPLL import BasicDPLL
from math import sqrt

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

def load_sudoku(filename, which):
    """
    Loads a sudoku form a collection and returns the DIMACS format of it.
    Works only for square sudokus.

    :param filename: File with the sudoku collection.
    :param which: The index of the sudoku that is choosen from the collection.
    :return: DIMACS clauses representing the sudoku instance.
    """
    with open(filename) as f:
        # read all sudokus
        sudokus = f.readlines()
        # choose one and trim 'newline'
        sudoku = sudokus[which][:-1]
        size = len(sudoku)

        sudoku_dimacs = []
        position = 0  # counter for position in the string
        for row in range(int(sqrt(size))):
            for col in range(int(sqrt(size))):
                if sudoku[position] != '.':
                    sudoku_dimacs.append([int(str(row+1) + str(col+1) + sudoku[position])])
                position += 1

        return sudoku_dimacs

def main():
    numOfVars = 4*4*4
    rules = load_sudoku_rules('rules/sudoku-rules_4x4.txt')
    sudoku = load_sudoku('sudokus/1000_sudokus_4x4.txt', 0)
    cnf = rules + sudoku

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