#!/usr/bin/env python
"""Provides SolverComparisonExperiment
"""

import time
import csv
import argparse


from BasicDPLL import BasicDPLL
from DummyBranchDecision import DummyBranchDecision
from DynamicLargestCombinedSum import DynamicLargestCombinedSum
from DynamicLargestIndividualSum import DynamicLargestIndividualSum
from JeroslowWangOneSided import JeroslowWangOneSided

from dimacs_tools import load_dimacs, load_sudokus
from InMemoryMetrics import InMemoryMetrics
from tools import save_csv

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class SolverComparisonExperiment:
    def run(self, start = 0, end = 1011):
        decisionHeuristicFactories = {
            "DLIS(True)": lambda: DynamicLargestIndividualSum(True),
            "DLIS(False)": lambda: DynamicLargestIndividualSum(False),
            "JW-OS": lambda: JeroslowWangOneSided(),
            "DLCS": lambda: DynamicLargestCombinedSum(),
            "HERO": lambda: DummyBranchDecision(),
        }

        rules, numOfVars = load_dimacs('rules/sudoku_rules_9x9.txt')
        sudokus = load_sudokus('sudokus/1000_sudokus_9x9.txt')[start:end]
        data = []

        for i in range(len(sudokus)):
            if i % 10 == 5:
                print(".", end='', flush=True)
            sudoku = sudokus[i]
            sudokuID = i + 1
            for name in decisionHeuristicFactories:
                decisionHeuristicFactory = decisionHeuristicFactories[name]
                cnf = rules + sudoku
                instanceMetrics = InMemoryMetrics()

                before = time.time()
                solver = BasicDPLL(cnf,
                    numOfVars,
                    decisionHeuristicFactory,
                    -1,
                    0,
                    instanceMetrics
                )
                result, _ = solver.solve()
                totalTime = time.time()-before
                counters = instanceMetrics.getCounters()
                data.append((
                    sudokuID,
                    name,
                    result,
                    totalTime,
                    counters.get("loop", 0),
                    counters.get("backtrack", 0),
                    counters.get("flip", 0),
                    counters.get("unit", 0),
                ))

        # Save output to csv
        header = ["sudokuID","name", "result", "totalTime", "loop", "backtrack", "flip", "unit"]
        filename = "solver_comparison.csv"
        save_csv(filename, header, data)
        print("")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
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
    args = parser.parse_args()
    start = args.start
    end = args.end
    print("start={}, end={}".format(start, end))

    before = time.time()
    experiment = SolverComparisonExperiment()
    experiment.run(start, end)
    print("time={} seconds".format(time.time()-before))