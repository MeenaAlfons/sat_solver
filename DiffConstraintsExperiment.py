#!/usr/bin/env python
"""Provides SolverComparisonExperiment
"""

import time
import csv
import argparse


from BasicDPLL import BasicDPLL
from DummyBranchDecision import DummyBranchDecision
from RandomFalseBranchDecision import RandomFalseBranchDecision

from dimacs_tools import load_dimacs, load_sudokus
from InMemoryMetrics import InMemoryMetrics
from tools import save_csv
from SudokuRules import SudokuRules

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class DiffConstraintsExperiment:
    def __init__(self):
        self.rulesCreator = SudokuRules(9)

    def rulesOf(self, rows, cols, blocks):
        name = "r{}_c{}_b{}".format(rows, cols, blocks)

        self.rulesCreator.reset()
        if rows > 0:
            self.rulesCreator.add_alldiff_row_cum(rows)

        if cols > 0:
            self.rulesCreator.add_alldiff_col_cum(cols)

        if blocks > 0:
            self.rulesCreator.add_alldiff_block_cum(blocks)

        return name, self.rulesCreator.getRules()


    def generateRules(self, numOfConstraints):
        rulesDict = {}
        # the following nested loop go throw all the combinations of rows, cols, blocks
        # Where each one of them could have values from 0 to 9
        # However the script only considers combinations which add up to the numOfConstraints
        # Example combinations when numOfConstraints=7:
        # row=0 col=0 blocks=7
        # row=1 col=3 blocks=3
        # row=6 col=0 blocks=1
        for row in range(9+1):
            if row == numOfConstraints:
                name, rules = self.rulesOf(row, 0, 0)
                rulesDict[name] = rules
                break
            for col in range(9+1):
                if row + col == numOfConstraints:
                    name, rules = self.rulesOf(row, col, 0)
                    rulesDict[name] = rules
                    break
                for block in range(9+1):
                    if row + col + block == numOfConstraints:
                        name, rules = self.rulesOf(row, col, block)
                        rulesDict[name] = rules
                        break

        return rulesDict

    def run(self, numOfConstraints, timeout, start = 0, end = 1011):
        decisionHeuristicFactory = lambda:  DummyBranchDecision()#RandomFalseBranchDecision()

        rules, numOfVars = load_dimacs('rules/sudoku_rules_9x9.txt')
        sudokus = load_sudokus('sudokus/1000_sudokus_9x9.txt')[start:end]
        data = []

        rulesDict = self.generateRules(numOfConstraints)

        for i in range(len(sudokus)):
            if i % 10 == 9:
                print(".", end='', flush=True)
            sudoku = sudokus[i]
            sudokuID = i + 1
            for name in rulesDict:
                rules = rulesDict[name]
                cnf = rules + sudoku
                instanceMetrics = InMemoryMetrics()

                before = time.time()
                solver = BasicDPLL(cnf,
                    numOfVars,
                    decisionHeuristicFactory,
                    timeout,
                    5,
                    instanceMetrics
                )
                result, _ = solver.solve()
                totalTime = time.time()-before
                counters = instanceMetrics.getCounters()
                if result == "TIMEOUT":
                    print("T", end='', flush=True)
                data.append((
                    sudokuID,
                    name,
                    numOfConstraints,
                    result,
                    totalTime,
                    counters.get("loop", 0),
                    counters.get("backtrack", 0),
                    counters.get("flip", 0),
                    counters.get("unit", 0),
                ))

        # Save output to csv
        header = ["sudokuID", "name", "numOfConstraints", "result", "totalTime", "loop", "backtrack", "flip", "unit"]
        filename="constraints_{}_{}_{}.csv".format(numOfConstraints, start, end)
        save_csv(filename, header, data)
        print("")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('numOfContraints',
                        metavar='numOfContraints',
                        type=int,
                        help='the number of constraints')
    parser.add_argument('--start',
                        metavar='start',
                        type=int,
                        help='start',
                        default=0)
    parser.add_argument('--end',
                        metavar='end',
                        type=int,
                        help='end',
                        default=1011)
    parser.add_argument('--timeout',
                        metavar='timeout',
                        type=float,
                        help='timeout',
                        default=5)
    args = parser.parse_args()
    numOfContraints = args.numOfContraints
    start = args.start
    end = args.end
    timeout = args.timeout
    print("numOfConstraints={}, timeout={}, start={}, end={}".format(numOfContraints, timeout, start, end))

    before = time.time()
    experiment = DiffConstraintsExperiment()
    experiment.run(numOfContraints, timeout, start, end)
    print("time={} seconds".format(time.time()-before))