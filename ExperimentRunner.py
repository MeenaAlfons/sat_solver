#!/usr/bin/env python
"""Provides ExperimentRunner
"""

import time
import csv
import argparse
import multiprocessing as mp

from BasicDPLL import BasicDPLL
from DummyBranchDecision import DummyBranchDecision
from RandomBranchDecision import RandomBranchDecision
from RandomFalseBranchDecision import RandomFalseBranchDecision
from DynamicLargestCombinedSum import DynamicLargestCombinedSum
from DynamicLargestIndividualSum import DynamicLargestIndividualSum
from JeroslowWangOneSided import JeroslowWangOneSided

from dimacs_tools import  load_dimacs, load_sudokus
from tools import save_csv

from Experiment import processOneSudoku, dataHeader, processOneSudokuWithHeuristic, heuristicDataHeader

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class ExperimentRunner:
    def run(self, experimentName, rulesDict, timeout, start = 0, end = 1011):
        sudokus = load_sudokus('sudokus/1000_sudokus_9x9.txt')[start:end]
        data = []

        inputValues = []
        for i in range(len(sudokus)):
            sudoku = sudokus[i]
            sudokuID = start + i + 1
            inputValues.append((sudokuID, sudoku, rulesDict, timeout))

        print("cpu_count={}".format(mp.cpu_count()))
        pool = mp.Pool(mp.cpu_count())
        results = pool.starmap(processOneSudoku, inputValues)
        pool.close()
        for result in results:
            data.extend(result)

        # Save output to csv
        filename="{}_{}_{}_{}.csv".format(experimentName, start, end, time.time())
        save_csv(filename, dataHeader, data)
        print("")

def DynamicLargestIndividualSumTrueFactory():
    return DynamicLargestIndividualSum(True)


def DynamicLargestIndividualSumFalseFactory():
    return DynamicLargestIndividualSum(False)

def JeroslowWangOneSidedFactory():
    return JeroslowWangOneSided()

def DynamicLargestCombinedSumFactory():
    return DynamicLargestCombinedSum()

def DummyBranchDecisionFactory():
    return DummyBranchDecision()

def RandomFalseBranchDecisionFactory():
    return RandomFalseBranchDecision()

def RandomBranchDecisionFactory():
    return RandomBranchDecision()

class SolverComparisonExperimentRunner:
    def run(self, start = 0, end = 1011):
        rules, _ = load_dimacs('rules/sudoku_rules_9x9.txt')
        sudokus = load_sudokus('sudokus/1000_sudokus_9x9.txt')[start:end]
        data = []

        heuristicDict = {
            "Random": RandomBranchDecisionFactory,
            "DLIS(True)": DynamicLargestIndividualSumTrueFactory,
            "DLIS(False)": DynamicLargestIndividualSumFalseFactory,
            "JW-OS": JeroslowWangOneSidedFactory,
            "DLCS": DynamicLargestCombinedSumFactory,
            "Dummy": DummyBranchDecisionFactory,
            "RandomFalse": RandomFalseBranchDecisionFactory,
        }

        inputValues = []
        for i in range(len(sudokus)):
            sudoku = sudokus[i]
            sudokuID = start + i + 1
            inputValues.append((sudokuID, sudoku, rules, heuristicDict))

        print("cpu_count={}".format(mp.cpu_count()))
        pool = mp.Pool(mp.cpu_count())
        results = pool.starmap(processOneSudokuWithHeuristic, inputValues)
        pool.close()
        for result in results:
            data.extend(result)

        # Save output to csv
        filename="SolverComparison_{}_{}.csv".format(start, end)
        save_csv(filename, heuristicDataHeader, data)
        print("")